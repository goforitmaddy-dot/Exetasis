import uuid
from typing import Any, Dict
from langgraph.graph import END, START, StateGraph

from backend.app.agents.accountability import AccountabilityAgent
from backend.app.agents.contribution import ContributionAgent
from backend.app.agents.culture import CultureAgent
from backend.app.agents.environment import EnvironmentAgent
from backend.app.agents.fairness import FairnessAgent
from backend.app.agents.reward import RewardAgent
from backend.app.agents.workplace_architect import WorkplaceArchitectAgent
from backend.app.agents.workplace_configuration import WorkplaceConfigurationAgent
from backend.app.core.logging import logger
from backend.app.orchestration.state import WorkplaceGraphState
from backend.app.schemas.agents import (
    AccountabilityAgentInput,
    BaseAgentOutput,
    ContributionAgentInput,
    CultureAgentInput,
    EnvironmentAgentInput,
    FairnessAgentInput,
    OrchestrationRunResponse,
    RewardAgentInput,
    WorkplaceArchitectInput,
    WorkplaceConfigurationInput,
)
from backend.app.services.llm.factory import get_llm_client


async def node_architect(state: WorkplaceGraphState) -> Dict[str, Any]:
    """Node running WorkplaceArchitectAgent."""
    client = get_llm_client()
    agent = WorkplaceArchitectAgent(client)
    res = await agent.evaluate(
        WorkplaceArchitectInput(target_id=state["target_id"], event_ids=state.get("event_ids", []))
    )
    return {"architect_output": res.model_dump()}


async def node_configuration(state: WorkplaceGraphState) -> Dict[str, Any]:
    """Node running WorkplaceConfigurationAgent."""
    client = get_llm_client()
    agent = WorkplaceConfigurationAgent(client)
    res = await agent.evaluate(
        WorkplaceConfigurationInput(target_id=state["target_id"], event_ids=state.get("event_ids", []))
    )
    return {"configuration_output": res.model_dump()}


async def node_contribution(state: WorkplaceGraphState) -> Dict[str, Any]:
    """Node running ContributionAgent."""
    client = get_llm_client()
    agent = ContributionAgent(client)
    res = await agent.evaluate(
        ContributionAgentInput(target_id=state["target_id"], event_ids=state.get("event_ids", []))
    )
    return {"contribution_output": res.model_dump()}


async def node_fairness(state: WorkplaceGraphState) -> Dict[str, Any]:
    """Node running FairnessAgent."""
    client = get_llm_client()
    agent = FairnessAgent(client)
    res = await agent.evaluate(
        FairnessAgentInput(target_id=state["target_id"], event_ids=state.get("event_ids", []))
    )
    return {"fairness_output": res.model_dump()}


async def node_culture(state: WorkplaceGraphState) -> Dict[str, Any]:
    """Node running CultureAgent."""
    client = get_llm_client()
    agent = CultureAgent(client)
    res = await agent.evaluate(
        CultureAgentInput(target_id=state["target_id"], event_ids=state.get("event_ids", []))
    )
    return {"culture_output": res.model_dump()}


async def node_environment(state: WorkplaceGraphState) -> Dict[str, Any]:
    """Node running EnvironmentAgent."""
    client = get_llm_client()
    agent = EnvironmentAgent(client)
    res = await agent.evaluate(
        EnvironmentAgentInput(target_id=state["target_id"], event_ids=state.get("event_ids", []))
    )
    return {"environment_output": res.model_dump()}


async def node_reward(state: WorkplaceGraphState) -> Dict[str, Any]:
    """Node running RewardAgent."""
    client = get_llm_client()
    agent = RewardAgent(client)
    res = await agent.evaluate(
        RewardAgentInput(target_id=state["target_id"], event_ids=state.get("event_ids", []))
    )
    return {"reward_output": res.model_dump()}


async def node_accountability(state: WorkplaceGraphState) -> Dict[str, Any]:
    """Node running AccountabilityAgent."""
    client = get_llm_client()
    agent = AccountabilityAgent(client)
    res = await agent.evaluate(
        AccountabilityAgentInput(target_id=state["target_id"], event_ids=state.get("event_ids", []))
    )
    return {"accountability_output": res.model_dump()}


async def node_synthesizer(state: WorkplaceGraphState) -> Dict[str, Any]:
    """Synthesizer node aggregating all agent scores and generating summary."""
    keys = [
        "architect_output",
        "configuration_output",
        "contribution_output",
        "fairness_output",
        "culture_output",
        "environment_output",
        "reward_output",
        "accountability_output",
    ]
    scores = []
    for k in keys:
        out = state.get(k)
        if out and isinstance(out, dict) and isinstance(out.get("score"), (int, float)):
            scores.append(float(out["score"]))

    overall = round(sum(scores) / len(scores), 2) if scores else None
    if overall is None:
        summary = (
            f"Multi-agent workplace evaluation completed for target '{state.get('target_id')}'. "
            "Overall health index unavailable because no valid agent scores were returned."
        )
    else:
        summary = (
            f"Multi-agent workplace evaluation completed for target '{state.get('target_id')}'. "
            f"Overall health index is {overall:.2f} across {len(scores)} evaluated dimensions."
        )
    return {"overall_score": overall, "summary": summary}


def build_workplace_graph():
    """Build and compile the LangGraph multi-agent StateGraph."""
    workflow = StateGraph(WorkplaceGraphState)

    workflow.add_node("architect", node_architect)
    workflow.add_node("configuration", node_configuration)
    workflow.add_node("contribution", node_contribution)
    workflow.add_node("fairness", node_fairness)
    workflow.add_node("culture", node_culture)
    workflow.add_node("environment", node_environment)
    workflow.add_node("reward", node_reward)
    workflow.add_node("accountability", node_accountability)
    workflow.add_node("synthesizer", node_synthesizer)

    workflow.add_edge(START, "architect")
    workflow.add_edge("architect", "configuration")
    workflow.add_edge("configuration", "contribution")
    workflow.add_edge("contribution", "fairness")
    workflow.add_edge("fairness", "culture")
    workflow.add_edge("culture", "environment")
    workflow.add_edge("environment", "reward")
    workflow.add_edge("reward", "accountability")
    workflow.add_edge("accountability", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()


compiled_workplace_graph = build_workplace_graph()


async def execute_workplace_pipeline(
    target_id: str,
    event_ids: list[str] | None = None,
    parameters: dict[str, Any] | None = None,
) -> OrchestrationRunResponse:
    """Execute the multi-agent graph pipeline and return typed response."""
    initial_state: WorkplaceGraphState = {
        "target_id": target_id,
        "event_ids": event_ids or [],
        "parameters": parameters or {},
        "errors": [],
    }

    final_state = await compiled_workplace_graph.ainvoke(initial_state)

    agent_results: dict[str, BaseAgentOutput] = {}
    mapping = {
        "workplace_architect": "architect_output",
        "workplace_configuration": "configuration_output",
        "contribution": "contribution_output",
        "fairness": "fairness_output",
        "culture": "culture_output",
        "environment": "environment_output",
        "reward": "reward_output",
        "accountability": "accountability_output",
    }

    for agent_id, state_key in mapping.items():
        data = final_state.get(state_key)
        if data and isinstance(data, dict):
            agent_results[agent_id] = BaseAgentOutput(**data)

    return OrchestrationRunResponse(
        run_id=str(uuid.uuid4()),
        target_id=target_id,
        status="completed",
        agent_results=agent_results,
        overall_score=final_state.get("overall_score"),
        summary=final_state.get("summary", "Analysis completed; overall score unavailable."),
    )
