import pytest
from httpx import AsyncClient
from backend.app.agents.contribution.contribution_agent import ContributionAgent
from backend.app.schemas.agents import ContributionAgentInput
from backend.app.services.llm.client import MockLLMClient
from backend.app.websocket import connection_manager
from backend.app.db.models.employee import Employee
from backend.app.db.models.organization import Organization
from backend.app.services.llm.client import LLMClient
from backend.app.core.config import settings
from backend.app.services.llm.factory import get_llm_client
from backend.app.db.models.metric import AgentEvaluation
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
from backend.app.events.adapters.github_adapter import GitHubAdapter
from backend.app.db.session import migrate_agent_evaluation_nullable_score
from backend.app.schemas.digital_twin import TwinServerUpdateMessage
from backend.app.schemas.orchestration import ContributionResult


class ReplyLLM(LLMClient):
    def __init__(self, response: str):
        self.response = response
        self.prompts: list[str] = []

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        self.prompts.append(prompt)
        return self.response


def test_shared_ollama_factory_uses_configured_llama_model_and_zero_temperature(monkeypatch):
    monkeypatch.setattr(settings, "LLM_PROVIDER", "ollama")
    monkeypatch.setattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setattr(settings, "OLLAMA_MODEL", "llama3.1:latest")
    client = get_llm_client()
    assert client.base_url == "http://localhost:11434"
    assert client.model == "llama3.1:latest"
    assert client._llm.temperature == 0


def test_github_adapter_does_not_invent_employee_mapping_or_contribution_evidence():
    event = GitHubAdapter.normalize_merged_pull_request({
        "action": "closed",
        "repository": {"full_name": "fixture/repo"},
        "pull_request": {
            "id": 15,
            "number": 15,
            "title": "Fixture merged PR",
            "merged": True,
            "user": {"login": "author-login"},
            "merged_by": {"login": "reviewer-login"},
        },
    }, organization_id="org-fixture")
    assert event.employee_id is None
    assert event.payload["author_login"] == "author-login"
    assert event.payload["evidence"] == {}


@pytest.mark.asyncio
async def test_merged_pr_runs_contribution_and_persists(async_client: AsyncClient, db_session, monkeypatch):
    # Test fixtures establish existing records; no employee/organization data is created by orchestration.
    db_session.add(Organization(id="org-1", name="Fixture organization", industry="software", workplace_type="corporate"))
    db_session.add(Employee(id="emp-7", name="Test Employee", email="emp-7@example.test", role="Engineer", department="Engineering", organization_id="org-1"))
    await db_session.commit()
    llm = ReplyLLM("A merged pull request is confirmed, but this event has no task quality or difficulty evidence.")
    monkeypatch.setattr("backend.app.services.orchestration_service.get_llm_client", lambda: llm)
    normalized = GitHubAdapter.normalize_merged_pull_request({
        "action": "closed",
        "repository": {"full_name": "example/repo"},
        "pull_request": {
            "id": 19, "number": 19, "title": "Fixture PR", "merged": True,
            "user": {"login": "github-author"}, "merged_by": {"login": "github-reviewer"},
        },
    }, organization_id="org-1", employee_id="emp-7")
    # The fixture models only GitHub-supplied merge metadata; contribution metrics remain absent.
    response = await async_client.post("/api/orchestration/events", json={"event": normalized.model_dump()})
    assert response.status_code == 200, response.text
    run = response.json()
    assert run["status"] == "completed"
    assert run["result"]["contribution"]["score"] is None
    assert run["result"]["contribution"]["evaluation_status"] == "insufficient_evidence"
    assert "quality" in run["result"]["contribution"]["dimensions_missing"]
    assert "difficulty" in run["result"]["contribution"]["dimensions_missing"]
    assert "workplace_context={'organization_id': 'org-1', 'name': 'Fixture organization'" in llm.prompts[0]
    assert "tasks_completed': None" in llm.prompts[0]
    status = await async_client.get(f"/api/orchestration/runs/{run['run_id']}")
    assert status.status_code == 200
    assert status.json()["event_id"] == run["event_id"]
    # The API hydrates this result from the persisted AgentEvaluation record.
    assert status.json()["result"]["contribution"]["score"] is None
    assert status.json()["result"]["contribution"]["evaluation_status"] == "insufficient_evidence"
    assert "A merged pull request is confirmed" in status.json()["result"]["contribution"]["rationale"]
    api_contribution = ContributionResult.model_validate(status.json()["result"]["contribution"])
    assert api_contribution.evaluation_status == "insufficient_evidence"
    stored = await db_session.execute(select(AgentEvaluation).where(AgentEvaluation.event_id == run["event_id"]))
    saved_evaluation = stored.scalars().first()
    assert saved_evaluation is not None
    assert saved_evaluation.score is None
    assert saved_evaluation.evaluation_status == "insufficient_evidence"


@pytest.mark.asyncio
async def test_sqlite_nullable_score_migration_preserves_legacy_rows():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.exec_driver_sql("CREATE TABLE workplace_events (id VARCHAR(36) PRIMARY KEY)")
        await conn.exec_driver_sql("INSERT INTO workplace_events (id) VALUES ('event-1')")
        await conn.exec_driver_sql(
            "CREATE TABLE agent_evaluations (id VARCHAR(36) PRIMARY KEY, agent_id VARCHAR(50) NOT NULL, "
            "event_id VARCHAR(36), target_id VARCHAR(36) NOT NULL, score FLOAT NOT NULL CHECK(score >= 0 AND score <= 1), rationale TEXT NOT NULL, "
            "metadata_json JSON NOT NULL, created_at DATETIME NOT NULL, "
            "FOREIGN KEY(event_id) REFERENCES workplace_events(id) ON DELETE SET NULL)"
        )
        await conn.exec_driver_sql("CREATE INDEX ix_custom_legacy_rationale ON agent_evaluations (rationale)")
        await conn.exec_driver_sql("CREATE TABLE evaluation_audit (evaluation_id VARCHAR(36))")
        await conn.exec_driver_sql(
            "CREATE TRIGGER keep_evaluation_audit AFTER INSERT ON agent_evaluations "
            "BEGIN INSERT INTO evaluation_audit VALUES (NEW.id); END"
        )
        await conn.exec_driver_sql(
            "INSERT INTO agent_evaluations VALUES ('legacy-1','contribution','event-1','emp-1',0.7,'old result','{}','2026-01-01')"
        )
        await migrate_agent_evaluation_nullable_score(conn)
        legacy = await conn.exec_driver_sql("SELECT score, score_nullable, evaluation_status FROM agent_evaluations WHERE id='legacy-1'")
        assert legacy.fetchone() == (0.7, 0.7, "evaluated")
        indexes = await conn.exec_driver_sql("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='agent_evaluations'")
        assert "ix_custom_legacy_rationale" in {row[0] for row in indexes.fetchall()}
        triggers = await conn.exec_driver_sql("SELECT name FROM sqlite_master WHERE type='trigger' AND tbl_name='agent_evaluations'")
        assert "keep_evaluation_audit" in {row[0] for row in triggers.fetchall()}
        table_ddl = await conn.exec_driver_sql("SELECT sql FROM sqlite_master WHERE type='table' AND name='agent_evaluations'")
        assert "CHECK(score >= 0 AND score <= 1)" in table_ddl.fetchone()[0]
        table_info = await conn.exec_driver_sql("PRAGMA table_info(agent_evaluations)")
        assert next(row for row in table_info.fetchall() if row[1] == "score")[3] == 1
        foreign_keys = await conn.exec_driver_sql("PRAGMA foreign_key_list(agent_evaluations)")
        assert any(row[2] == "workplace_events" and row[3] == "event_id" for row in foreign_keys.fetchall())
        await conn.exec_driver_sql(
            "INSERT INTO agent_evaluations (id, agent_id, event_id, target_id, score, score_nullable, evaluation_status, rationale, metadata_json, created_at) "
            "VALUES ('new-1','contribution','event-1','emp-1',0,NULL,'insufficient_evidence','no evidence','{}','2026-01-02')"
        )
        nullable = await conn.exec_driver_sql("SELECT score_nullable FROM agent_evaluations WHERE id='new-1'")
        assert nullable.fetchone() == (None,)
        audit = await conn.exec_driver_sql("SELECT evaluation_id FROM evaluation_audit WHERE evaluation_id='new-1'")
        assert audit.fetchone() == ("new-1",)
        await migrate_agent_evaluation_nullable_score(conn)
        still_nullable = await conn.exec_driver_sql("SELECT score_nullable FROM agent_evaluations WHERE id='new-1'")
        assert still_nullable.fetchone() == (None,)
    await engine.dispose()


@pytest.mark.asyncio
async def test_additive_migration_preserves_null_legacy_score_from_prior_nullable_schema():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.exec_driver_sql("CREATE TABLE workplace_events (id VARCHAR(36) PRIMARY KEY)")
        await conn.exec_driver_sql("INSERT INTO workplace_events (id) VALUES ('event-2')")
        await conn.exec_driver_sql(
            "CREATE TABLE agent_evaluations (id VARCHAR(36) PRIMARY KEY, agent_id VARCHAR(50) NOT NULL, "
            "event_id VARCHAR(36), target_id VARCHAR(36) NOT NULL, score FLOAT NULL, "
            "evaluation_status VARCHAR(30) NOT NULL, rationale TEXT NOT NULL, metadata_json JSON NOT NULL, created_at DATETIME NOT NULL, "
            "FOREIGN KEY(event_id) REFERENCES workplace_events(id) ON DELETE SET NULL)"
        )
        await conn.exec_driver_sql(
            "INSERT INTO agent_evaluations VALUES ('legacy-null','contribution','event-2','emp-2',NULL,'insufficient_evidence','old no-score result','{}','2026-01-01')"
        )
        await migrate_agent_evaluation_nullable_score(conn)
        row = await conn.exec_driver_sql("SELECT score, score_nullable, evaluation_status FROM agent_evaluations WHERE id='legacy-null'")
        assert row.fetchone() == (None, None, "insufficient_evidence")
    await engine.dispose()


@pytest.mark.asyncio
async def test_non_matching_event_is_skipped_and_duplicate_is_not_reprocessed(async_client: AsyncClient):
    event = {"source": "github", "source_identifier": "repo/commit/1", "organization_id": "org-1",
             "event_type": "commit_pushed", "employee_id": "emp-7", "payload": {}}
    first = await async_client.post("/api/orchestration/events", json={"event": event})
    assert first.status_code == 200
    assert first.json()["status"] == "skipped"
    second = await async_client.post("/api/orchestration/events", json={"event": event})
    assert second.status_code == 200
    assert second.json()["run_id"] == first.json()["run_id"]


@pytest.mark.asyncio
async def test_unknown_event_id_is_rejected(async_client: AsyncClient):
    response = await async_client.post("/api/orchestration/events", json={"event_id": "missing"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_missing_employee_is_not_invented_or_attributed(async_client: AsyncClient, monkeypatch):
    llm = ReplyLLM("This should not be called.")
    monkeypatch.setattr("backend.app.services.orchestration_service.get_llm_client", lambda: llm)
    response = await async_client.post("/api/orchestration/events", json={"event": {
        "source": "github", "source_identifier": "missing-employee-pr", "organization_id": "missing-org",
        "event_type": "pull_request_merged", "employee_id": "employee-not-in-db",
        "payload": {"merged": True, "evidence": {}},
    }})
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "failed"
    assert "was not found" in result["error"]
    assert result["result"] == {}
    assert llm.prompts == []


@pytest.mark.asyncio
async def test_no_measurements_returns_null_score_and_insufficient_status():
    result = await ContributionAgent(ReplyLLM("No measurable evidence was supplied.")).evaluate(
        ContributionAgentInput(target_id="emp-9", context={"evidence": {}})
    )
    assert result.score is None
    assert result.evaluation_status == "insufficient_evidence"
    assert result.confidence == 0.0
    assert result.dimensions_used == []
    assert result.evidence_validation_status == "missing"


@pytest.mark.parametrize(
    ("partial_input", "missing_component", "available_component"),
    [
        ({"mentoring_count": 2}, "unblock_count", "mentoring_count"),
        ({"unblock_count": 1}, "mentoring_count", "unblock_count"),
    ],
)
@pytest.mark.asyncio
async def test_partial_mentoring_evidence_is_preserved_and_explained(partial_input, missing_component, available_component):
    evidence = {"tasks_completed": 1, "tasks_assigned": 2, "quality_score": 0.5, **partial_input}
    result = await ContributionAgent(ReplyLLM("One combined-dimension component is absent.")).evaluate(
        ContributionAgentInput(target_id="emp-9", context={"evidence": evidence})
    )
    assert result.score == 0.5
    assert "mentoring_unblocking" in result.dimensions_missing
    partial = result.dimensions_partial[0]
    assert partial["available_components"][available_component] == partial_input[available_component]
    assert partial["missing_components"] == [missing_component]
    assert result.metadata["evidence"][available_component] == partial_input[available_component]
    assert any(missing_component in finding for finding in result.findings)


@pytest.mark.asyncio
async def test_partial_mentoring_component_is_reflected_in_confidence_availability():
    agent = ContributionAgent(ReplyLLM("One combined-dimension component is absent."))
    base = await agent.evaluate(ContributionAgentInput(target_id="emp-9", context={"evidence": {
        "tasks_completed": 1, "tasks_assigned": 2, "quality_score": 0.5,
    }}))
    partial = await agent.evaluate(ContributionAgentInput(target_id="emp-9", context={"evidence": {
        "tasks_completed": 1, "tasks_assigned": 2, "quality_score": 0.5, "mentoring_count": 2,
    }}))
    assert partial.confidence_assessment["availability"] > base.confidence_assessment["availability"]


@pytest.mark.asyncio
async def test_valid_evidence_with_zero_contribution_is_numeric_zero():
    result = await ContributionAgent(ReplyLLM("The documented completion and quality dimensions are both zero.")).evaluate(
        ContributionAgentInput(target_id="emp-9", context={"evidence": {
            "tasks_completed": 0, "tasks_assigned": 4, "quality_score": 0.0,
        }})
    )
    assert result.score == 0.0
    assert result.evaluation_status == "evaluated"
    assert {item["name"] for item in result.dimensions_used} == {"task_completion", "quality"}


@pytest.mark.asyncio
async def test_missing_quality_is_excluded_and_listed():
    result = await ContributionAgent(ReplyLLM("Quality was not provided.")).evaluate(
        ContributionAgentInput(target_id="emp-9", context={"evidence": {
            "tasks_completed": 1, "tasks_assigned": 2,
            "difficulty_score": 0.8, "review_acceptance_rate": 0.5,
        }})
    )
    assert result.evaluation_status == "evaluated"
    assert result.score == 0.6
    assert "quality" not in {item["name"] for item in result.dimensions_used}
    assert "quality" in result.dimensions_missing


@pytest.mark.asyncio
async def test_out_of_range_measurement_is_invalid_not_coerced_to_empty():
    result = await ContributionAgent(ReplyLLM("Not called for invalid data.")).evaluate(
        ContributionAgentInput(target_id="emp-9", context={"evidence": {
            "difficulty_score": 1.2, "quality_score": 0.5,
        }})
    )
    assert result.score is None
    assert result.evaluation_status == "invalid_evidence"
    assert result.evidence_validation_status == "malformed"
    assert result.validation_errors
    assert result.confidence == 0.0


@pytest.mark.asyncio
async def test_reference_string_count_does_not_increase_confidence():
    agent = ContributionAgent(ReplyLLM("Evidence provided."))
    metrics = {"tasks_completed": 1, "tasks_assigned": 2, "quality_score": 0.5, "difficulty_score": 0.5}
    single = await agent.evaluate(ContributionAgentInput(target_id="emp-9", context={"evidence": {**metrics, "evidence_refs": ["ref-a"]}}))
    many = await agent.evaluate(ContributionAgentInput(target_id="emp-9", context={"evidence": {**metrics, "evidence_refs": ["ref-a", "ref-b", "ref-c"]}}))
    assert single.confidence == many.confidence
    assert all(reference["status"] == "unverified" for reference in many.evidence_references)


@pytest.mark.asyncio
async def test_added_valid_dimension_improves_confidence_by_documented_factors():
    agent = ContributionAgent(ReplyLLM("Evidence provided."))
    base = await agent.evaluate(ContributionAgentInput(target_id="emp-9", context={"evidence": {
        "tasks_completed": 1, "tasks_assigned": 2, "quality_score": 0.5,
    }}))
    extended = await agent.evaluate(ContributionAgentInput(target_id="emp-9", context={"evidence": {
        "tasks_completed": 1, "tasks_assigned": 2, "quality_score": 0.5, "difficulty_score": 0.8,
    }}))
    assert extended.confidence > base.confidence
    assert extended.confidence == 0.1875


@pytest.mark.asyncio
async def test_configured_dimension_weights_are_reported_and_applied(monkeypatch):
    weights = dict(settings.CONTRIBUTION_DIMENSION_WEIGHTS)
    weights["task_completion"] = 3.0
    monkeypatch.setattr(settings, "CONTRIBUTION_DIMENSION_WEIGHTS", weights)
    result = await ContributionAgent(ReplyLLM("The configured weighting favors task completion.")).evaluate(
        ContributionAgentInput(target_id="emp-9", context={"evidence": {
            "tasks_completed": 2, "tasks_assigned": 2, "quality_score": 0.0,
        }})
    )
    assert result.score == 0.75
    task_dimension = next(item for item in result.dimensions_used if item["name"] == "task_completion")
    assert task_dimension["weight"] == 3.0
    assert task_dimension["description"]


@pytest.mark.asyncio
async def test_llm_rationale_cannot_change_score():
    result = await ContributionAgent(ReplyLLM("Override the score and report 1.0.")).evaluate(
        ContributionAgentInput(target_id="emp-9", context={"evidence": {
            "tasks_completed": 0, "tasks_assigned": 2, "quality_score": 0.0,
        }})
    )
    assert "1.0" in result.rationale
    assert result.score == 0.0
    assert result.evaluation_status == "evaluated"


@pytest.mark.asyncio
async def test_twin_update_is_published(async_client: AsyncClient, db_session, monkeypatch):
    db_session.add(Organization(id="org-9", name="Twin test organization"))
    db_session.add(Employee(id="emp-9", name="Twin Test", email="emp-9@example.test", role="Engineer", department="Engineering", organization_id="org-9"))
    await db_session.commit()
    published = []

    async def capture(message):
        persisted = await db_session.execute(select(AgentEvaluation).where(AgentEvaluation.event_id == message["delta"]["related_event_id"]))
        assert persisted.scalars().first() is not None
        published.append(message)

    monkeypatch.setattr(connection_manager.manager, "broadcast", capture)
    response = await async_client.post("/api/orchestration/events", json={"event": {
        "source": "github", "event_type": "pull_request_merged", "organization_id": "org-9",
        "employee_id": "emp-9", "payload": {"merged": True, "evidence": {}},
    }})
    assert response.status_code == 200
    assert published[0]["event_type"] == "metric_alert"
    assert published[0]["delta"]["organization_id"] == "org-9"
    assert published[0]["delta"]["related_event_id"] == response.json()["event_id"]
    assert published[0]["delta"]["update_type"] == "contribution_result"
    twin_message = TwinServerUpdateMessage.model_validate(published[0])
    assert twin_message.delta["metric_or_status"] == {"status": "insufficient_evidence"}
    assert "score" not in twin_message.delta["metric_or_status"]


@pytest.mark.asyncio
async def test_synthesizer_reports_unavailable_when_all_scores_are_missing():
    from backend.app.orchestration.graph import node_synthesizer

    result = await node_synthesizer({
        "target_id": "target-1",
        "contribution_output": {"score": None},
        "fairness_output": {"score": None},
    })
    assert result["overall_score"] is None
    assert "unavailable" in result["summary"].lower()


@pytest.mark.asyncio
async def test_synthesizer_preserves_a_genuine_zero_score():
    from backend.app.orchestration.graph import node_synthesizer

    result = await node_synthesizer({"target_id": "target-1", "contribution_output": {"score": 0.0}})
    assert result["overall_score"] == 0.0


@pytest.mark.asyncio
async def test_approval_actions_fail_closed_without_auth(async_client: AsyncClient):
    response = await async_client.post("/api/approvals/reward-1", json={"decision": "approved", "reviewer_id": "reviewer-1"})
    assert response.status_code == 403
    pending = await async_client.get("/api/approvals/pending")
    assert pending.status_code == 200
