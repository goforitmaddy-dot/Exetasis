from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.events import (
    EventBatchIngestRequest,
    EventIngestResponse,
    WorkplaceEventCreate,
    WorkplaceEventRead,
)
from backend.app.services.event_service import EventService

events_router = APIRouter(prefix="/events", tags=["Events"])


def get_event_service(session: AsyncSession = Depends(get_db)) -> EventService:
    """Dependency provider for EventService."""
    return EventService(session)


@events_router.post("/ingest", response_model=WorkplaceEventRead)
async def ingest_event(
    event_in: WorkplaceEventCreate,
    service: EventService = Depends(get_event_service),
) -> WorkplaceEventRead:
    """Ingest a single workplace event."""
    return await service.ingest_single(event_in)


@events_router.post("/batch", response_model=EventIngestResponse)
async def ingest_event_batch(
    batch_in: EventBatchIngestRequest,
    service: EventService = Depends(get_event_service),
) -> EventIngestResponse:
    """Ingest a batch of workplace events."""
    return await service.ingest_batch(batch_in)


@events_router.get("", response_model=List[WorkplaceEventRead])
async def list_events(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: EventService = Depends(get_event_service),
) -> List[WorkplaceEventRead]:
    """Retrieve historical workplace events with pagination."""
    return await service.list_events(limit=limit, offset=offset)
