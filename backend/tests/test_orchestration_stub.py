import pytest
from httpx import AsyncClient
from backend.app.orchestration.graph import execute_workplace_pipeline


@pytest.mark.asyncio
async def test_execute_workplace_pipeline_direct():
    """Verify that the compiled LangGraph pipeline executes all 8 stub agents cleanly."""
    result = await execute_workplace_pipeline(target_id="employee-42", event_ids=["ev-1", "ev-2"])

    assert result.status == "completed"
    assert result.target_id == "employee-42"
    assert len(result.agent_results) == 8
    assert "fairness" in result.agent_results
    assert "contribution" in result.agent_results
    assert "workplace_architect" in result.agent_results
    assert result.overall_score > 0.0


@pytest.mark.asyncio
async def test_list_agents_api(async_client: AsyncClient):
    """Verify registered agent metadata endpoint."""
    response = await async_client.get("/api/agents")
    assert response.status_code == 200
    agents = response.json()
    assert len(agents) == 8
    agent_ids = {a["agent_id"] for a in agents}
    assert "workplace_architect" in agent_ids
    assert "fairness" in agent_ids
    assert "accountability" in agent_ids


@pytest.mark.asyncio
async def test_evaluate_single_agent_api(async_client: AsyncClient):
    """Verify single agent evaluation endpoint."""
    payload = {"target_id": "team-engineering", "context": {"sprint": 12}}
    response = await async_client.post("/api/agents/fairness/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["agent_id"] == "fairness"
    assert data["target_id"] == "team-engineering"
    assert "score" in data
    assert "rationale" in data


@pytest.mark.asyncio
async def test_orchestration_run_api(async_client: AsyncClient):
    """Verify multi-agent pipeline execution over REST API."""
    payload = {
        "target_id": "employee-007",
        "event_ids": ["ev-101"],
        "parameters": {},
    }
    response = await async_client.post("/api/orchestration/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["target_id"] == "employee-007"
    assert len(data["agent_results"]) == 8
