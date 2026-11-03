import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ingest_single_event(async_client: AsyncClient):
    """Verify single event ingestion and query."""
    payload = {
        "source": "slack",
        "event_type": "standup_note",
        "employee_id": "emp-101",
        "payload": {"message": "Working on digital twin canvas", "blockers": "none"},
    }
    response = await async_client.post("/api/events/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "slack"
    assert data["event_type"] == "standup_note"
    assert data["processed"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_ingest_batch_events(async_client: AsyncClient):
    """Verify batch event ingestion."""
    batch_payload = {
        "events": [
            {
                "source": "github",
                "event_type": "commit",
                "employee_id": "emp-102",
                "payload": {"hash": "c0ffee"},
            },
            {
                "source": "calendar",
                "event_type": "focus_block",
                "employee_id": "emp-102",
                "payload": {"duration": 120},
            },
        ]
    }
    response = await async_client.post("/api/events/batch", json=batch_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ingested_count"] == 2
    assert len(data["event_ids"]) == 2
    assert data["status"] == "success"
