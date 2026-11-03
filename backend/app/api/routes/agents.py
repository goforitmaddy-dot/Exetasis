from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.agents.accountability import AccountabilityAgent
from backend.app.agents.contribution import ContributionAgent
from backend.app.agents.culture import CultureAgent
from backend.app.agents.environment import EnvironmentAgent
from backend.app.agents.fairness import FairnessAgent
from backend.app.agents.reward import RewardAgent
from backend.app.agents.workplace_architect import WorkplaceArchitectAgent
from backend.app.agents.workplace_configuration import WorkplaceConfigurationAgent
from backend.app.orchestration.graph import execute_workplace_pipeline
from backend.app.schemas.agents import (
    AccountabilityAgentInput,
    AgentEvaluationRequest,
    AgentMetadataResponse,
    BaseAgentOutput,
    ContributionAgentInput,
    CultureAgentInput,
    EnvironmentAgentInput,
    FairnessAgentInput,
    OrchestrationRunRequest,
    OrchestrationRunResponse,
    RewardAgentInput,
    WorkplaceArchitectInput,
    WorkplaceConfigurationInput,
)
from backend.app.services.llm.factory import get_llm_client
from backend.app.db.session import get_db
from backend.app.schemas.orchestration import EventOrchestrationRequest, OrchestrationRunRead
from backend.app.services.orchestration_service import OrchestrationService
from backend.app.db.models.metric import AgentEvaluation
from backend.app.schemas.orchestration import ApprovalDecisionRequest

agents_router = APIRouter(prefix="", tags=["Agents & Orchestration"])

REGISTERED_AGENTS: List[AgentMetadataResponse] = [
    AgentMetadataResponse(
        agent_id="workplace_architect",
        name="Workplace Architect",
        description="Analyzes floor plan density, zone topologies, and spatial layout efficiency.",
        capabilities=["spatial_analysis", "capacity_forecasting", "zone_topology"],
    ),
    AgentMetadataResponse(
        agent_id="workplace_configuration",
        name="Workplace Configuration",
        description="Evaluates seating allocations, team adjacency, and physical accessibility compliance.",
        capabilities=["seating_allocation", "adjacency_compliance", "relocation_diffs"],
    ),
    AgentMetadataResponse(
        agent_id="contribution",
        name="Contribution Agent",
        description="Synthesizes code review depth, PR activity, and peer mentorship indicators.",
        capabilities=["code_review_metrics", "output_velocity", "mentorship_tracking"],
    ),
    AgentMetadataResponse(
        agent_id="fairness",
        name="Fairness Agent",
        description="Monitors task equity, on-call distribution, and systemic review toil.",
        capabilities=["equity_analysis", "toil_distribution", "bias_mitigation"],
    ),
    AgentMetadataResponse(
        agent_id="culture",
        name="Culture Agent",
        description="Measures sentiment patterns, camaraderie health, and psychological safety.",
        capabilities=["sentiment_trends", "camaraderie_index", "silo_detection"],
    ),
    AgentMetadataResponse(
        agent_id="environment",
        name="Environment Agent",
        description="Tracks ambient sensory metrics (noise, temp, lux) and focus interruptions.",
        capabilities=["acoustic_monitoring", "comfort_index", "focus_block_protection"],
    ),
    AgentMetadataResponse(
        agent_id="reward",
        name="Reward Agent",
        description="Recognizes milestones and formulates equitable kudos token rewards.",
        capabilities=["milestone_recognition", "kudos_issuance", "enablement_rewards"],
    ),
    AgentMetadataResponse(
        agent_id="accountability",
        name="Accountability Agent",
        description="Tracks deliverables, action items, and blameless delivery reliability.",
        capabilities=["action_item_tracking", "reliability_index", "dependency_visibility"],
    ),
]


@agents_router.get("/agents", response_model=List[AgentMetadataResponse])
async def list_agents() -> List[AgentMetadataResponse]:
    """List all registered workplace intelligence agents."""
    return REGISTERED_AGENTS


@agents_router.post("/agents/{agent_id}/evaluate", response_model=BaseAgentOutput)
async def evaluate_agent(
    payload: AgentEvaluationRequest,
    agent_id: str = Path(..., description="ID of the agent to execute"),
) -> BaseAgentOutput:
    """Trigger evaluation for an individual agent (STUB)."""
    client = get_llm_client()

    if agent_id == "workplace_architect":
        agent = WorkplaceArchitectAgent(client)
        return await agent.evaluate(WorkplaceArchitectInput(target_id=payload.target_id, context=payload.context))
    elif agent_id == "workplace_configuration":
        agent_config = WorkplaceConfigurationAgent(client)
        return await agent_config.evaluate(WorkplaceConfigurationInput(target_id=payload.target_id, context=payload.context))
    elif agent_id == "contribution":
        agent_contrib = ContributionAgent(client)
        return await agent_contrib.evaluate(ContributionAgentInput(target_id=payload.target_id, context=payload.context))
    elif agent_id == "fairness":
        agent_fair = FairnessAgent(client)
        return await agent_fair.evaluate(FairnessAgentInput(target_id=payload.target_id, context=payload.context))
    elif agent_id == "culture":
        agent_cult = CultureAgent(client)
        return await agent_cult.evaluate(CultureAgentInput(target_id=payload.target_id, context=payload.context))
    elif agent_id == "environment":
        agent_env = EnvironmentAgent(client)
        return await agent_env.evaluate(EnvironmentAgentInput(target_id=payload.target_id, context=payload.context))
    elif agent_id == "reward":
        agent_rew = RewardAgent(client)
        return await agent_rew.evaluate(RewardAgentInput(target_id=payload.target_id, context=payload.context))
    elif agent_id == "accountability":
        agent_acc = AccountabilityAgent(client)
        return await agent_acc.evaluate(AccountabilityAgentInput(target_id=payload.target_id, context=payload.context))
    else:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found.")


@agents_router.post("/orchestration/run", response_model=OrchestrationRunResponse)
async def run_orchestration(payload: OrchestrationRunRequest) -> OrchestrationRunResponse:
    """Trigger the multi-agent LangGraph workflow across all workplace agents (STUB)."""
    return await execute_workplace_pipeline(
        target_id=payload.target_id,
        event_ids=payload.event_ids,
        parameters=payload.parameters,
    )


@agents_router.post("/orchestration/events", response_model=OrchestrationRunRead)
async def run_event_orchestration(
    payload: EventOrchestrationRequest,
    session: AsyncSession = Depends(get_db),
) -> OrchestrationRunRead:
    """Ingest or process one normalized source event through conditional LangGraph routing."""
    try:
        return await OrchestrationService(session).run_event(event_id=payload.event_id, event=payload.event)
    except (ValueError, LookupError) as exc:
        raise HTTPException(status_code=404 if isinstance(exc, LookupError) else 422, detail=str(exc)) from exc


@agents_router.get("/orchestration/runs/{run_id}", response_model=OrchestrationRunRead)
async def get_orchestration_run(run_id: str, session: AsyncSession = Depends(get_db)) -> OrchestrationRunRead:
    run = await OrchestrationService(session).get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Orchestration run not found.")
    return run


@agents_router.get("/organizations/{organization_id}/agent-results")
async def get_organization_agent_results(
    organization_id: str,
    limit: int = 50,
    session: AsyncSession = Depends(get_db),
) -> list[dict]:
    runs = await OrchestrationService(session).list_runs(organization_id, limit=min(max(limit, 1), 200))
    return [item.model_dump(mode="json") for item in runs]


@agents_router.get("/approvals/pending")
async def list_pending_approvals(session: AsyncSession = Depends(get_db)) -> list[dict]:
    """List persisted findings that explicitly require human review."""
    result = await session.execute(select(AgentEvaluation).where(AgentEvaluation.agent_id.in_(["reward", "culture", "accountability"])))
    pending = []
    for row in result.scalars().all():
        data = row.metadata_json or {}
        status = data.get("approval_status")
        requires_review = data.get("requires_human_review") or data.get("requires_approval")
        if status == "pending" or requires_review:
            pending.append({"id": row.id, "agent_id": row.agent_id, "event_id": row.event_id,
                            "target_id": row.target_id, "status": "pending", "result": data})
    return pending


@agents_router.post("/approvals/{approval_id}")
async def decide_approval(approval_id: str, payload: ApprovalDecisionRequest) -> dict:
    """Fail closed until a trusted reviewer identity/permission provider is configured."""
    raise HTTPException(status_code=403, detail="Approval actions are disabled: this application has no authentication or reviewer permission system configured.")
