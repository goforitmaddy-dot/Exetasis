from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.agents.contribution import ContributionAgent
from backend.app.db.models.event import WorkplaceEvent
from backend.app.db.models.metric import AgentEvaluation
from backend.app.db.models.employee import Employee
from backend.app.db.models.organization import Organization
from backend.app.db.repositories.metric_repo import MetricRepository
from backend.app.schemas.agents import ContributionAgentInput
from backend.app.schemas.orchestration import ContributionResult, DigitalTwinUpdate
from backend.app.services.llm.client import LLMClient


class EventGraphState(TypedDict, total=False):
    event: dict[str, Any]
    contribution: dict[str, Any]
    status: str
    error: str
    update: dict[str, Any]
    employee_context: dict[str, Any]
    organization_context: dict[str, Any]
    context_error: str


def build_event_graph(session: AsyncSession, db_event: WorkplaceEvent, llm: LLMClient):
    """Build a small event-driven graph around existing persistence and WebSocket services."""

    async def validate(state: EventGraphState) -> dict[str, Any]:
        event = state["event"]
        if not event.get("id") or not event.get("event_type") or not event.get("source"):
            return {"status": "failed", "error": "Event is missing required identifiers or type."}
        return {"status": "validated"}

    async def load_context(state: EventGraphState) -> dict[str, Any]:
        organization_context: dict[str, Any] = {}
        organization_id = state["event"].get("organization_id")
        if organization_id:
            organization = await session.get(Organization, organization_id)
            if organization:
                organization_context = {
                    "organization_id": organization.id,
                    "name": organization.name,
                    "industry": organization.industry,
                    "workplace_type": organization.workplace_type,
                    "configuration": organization.configuration or {},
                    "available": True,
                }
            else:
                organization_context = {"organization_id": organization_id, "available": False, "missing_record": True}
        else:
            organization_context = {"available": False, "missing_record": True}
        employee_id = state["event"].get("employee_id")
        if not employee_id:
            if not (state["event"].get("payload") or {}).get("team_id"):
                return {"organization_context": organization_context, "employee_context": {}, "context_error": "No employee or team identifier is present."}
            return {"organization_context": organization_context, "employee_context": {"team_id": state["event"]["payload"]["team_id"]}}
        employee = await session.get(Employee, employee_id)
        if not employee:
            return {"organization_context": organization_context, "employee_context": {"missing_employee_record": True}, "context_error": f"Employee record '{employee_id}' was not found."}
        if db_event.organization_id and employee.organization_id and db_event.organization_id != employee.organization_id:
            return {"organization_context": organization_context, "employee_context": {"organization_mismatch": True}, "context_error": "Event and employee organization identifiers do not match."}
        return {
            "organization_context": organization_context,
            "employee_context": {"employee_id": employee.id, "role": employee.role, "department": employee.department},
        }

    def route(state: EventGraphState) -> str:
        event = state["event"]
        payload = event.get("payload") or {}
        is_merged_pr = (
            event.get("source") == "github"
            and event.get("event_type") in {"pull_request_merged", "pull_request"}
            and (event.get("event_type") == "pull_request_merged" or payload.get("merged") is True)
        )
        return "load_context" if is_merged_pr else "persist_skipped"

    async def contribution(state: EventGraphState) -> dict[str, Any]:
        event = state["event"]
        payload = event.get("payload") or {}
        target_id = event.get("employee_id") or payload["team_id"]
        evidence = payload.get("evidence", {})
        agent = ContributionAgent(llm)
        output = await agent.evaluate(ContributionAgentInput(target_id=target_id, context={
            "evidence": evidence,
            "organization": state.get("organization_context", {}),
            "employee": state.get("employee_context", {}),
        }))
        structured = ContributionResult(
            target_id=target_id,
            score=output.score,
            evaluation_status=output.evaluation_status,
            rationale=output.rationale,
            evidence=output.metadata.get("evidence", {}),
            dimensions_used=output.dimensions_used,
            dimensions_missing=output.dimensions_missing,
            dimensions_partial=output.dimensions_partial,
            evidence_validation_status=output.evidence_validation_status,
            validation_errors=output.validation_errors,
            evidence_references=output.evidence_references,
            confidence_assessment=output.confidence_assessment,
            confidence=output.confidence,
        )
        return {"contribution": structured.model_dump(mode="json"), "status": "completed"}

    async def context_failure(state: EventGraphState) -> dict[str, Any]:
        return {"status": "failed", "error": state["context_error"]}

    async def persist_result(state: EventGraphState) -> dict[str, Any]:
        result = state.get("contribution")
        if result:
            existing = await MetricRepository(session).get_by_event_and_agent(db_event.id, "contribution")
            if not existing:
                session.add(AgentEvaluation(
                    agent_id="contribution",
                    event_id=db_event.id,
                    target_id=result["target_id"],
                    score=result["score"],
                    score_compat=result["score"] if result["score"] is not None else 0.0,
                    evaluation_status=result["evaluation_status"],
                    rationale=result["rationale"],
                    metadata_json=result,
                ))
        db_event.processed = True
        await session.flush()
        return {"status": "completed" if result else "skipped"}

    async def publish_update(state: EventGraphState) -> dict[str, Any]:
        result = state.get("contribution")
        if not result:
            return {}
        update = DigitalTwinUpdate(
            organization_id=db_event.organization_id,
            related_event_id=db_event.id,
            update_type="contribution_result",
            employee_or_department_id=result["target_id"],
            metric_or_status=(
                {"score": result["score"], "status": result["evaluation_status"]}
                if result["score"] is not None
                else {"status": result["evaluation_status"]}
            ),
            summary=(
                f"Contribution analysis completed with score {result['score']:.2f}."
                if result["score"] is not None
                else f"Contribution analysis status: {result['evaluation_status']}; no score assigned."
            ),
        )
        return {"update": update.model_dump(mode="json")}

    graph = StateGraph(EventGraphState)
    graph.add_node("validate", validate)
    graph.add_node("load_context", load_context)
    graph.add_node("contribution", contribution)
    graph.add_node("persist", persist_result)
    graph.add_node("publish", publish_update)
    graph.add_node("persist_skipped", persist_result)
    graph.add_node("context_failure", context_failure)
    graph.add_edge(START, "validate")
    graph.add_node("route", lambda s: {})
    graph.add_conditional_edges("validate", lambda s: "route" if s.get("status") == "validated" else "stop", {"route": "route", "stop": END})
    graph.add_conditional_edges("route", route, {"load_context": "load_context", "persist_skipped": "persist_skipped"})
    graph.add_conditional_edges("load_context", lambda s: "fail" if s.get("context_error") else "contribution", {"contribution": "contribution", "fail": "context_failure"})
    graph.add_edge("context_failure", END)
    graph.add_edge("contribution", "persist")
    graph.add_edge("persist", "publish")
    graph.add_edge("publish", END)
    graph.add_edge("persist_skipped", END)
    return graph.compile()
