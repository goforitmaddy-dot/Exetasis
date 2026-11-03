from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.logging import logger
from backend.app.db.models.event import WorkplaceEvent
from backend.app.db.repositories.event_repo import EventRepository
from backend.app.schemas.events import (
    EventBatchIngestRequest,
    EventIngestResponse,
    WorkplaceEventCreate,
    WorkplaceEventRead,
)


class EventService:
    """Service orchestrating workplace event ingestion and retrieval."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = EventRepository(session)

    async def ingest_single(self, event_in: WorkplaceEventCreate) -> WorkplaceEventRead:
        """Persist a single workplace event."""
        logger.info("Ingesting event: source=%s, type=%s", event_in.source, event_in.event_type)
        if event_in.source_identifier:
            existing = await self.repo.get_by_source_identifier(event_in.source, event_in.source_identifier)
            if existing:
                return WorkplaceEventRead.model_validate(existing)
        db_event = WorkplaceEvent(
            source=event_in.source,
            event_type=event_in.event_type,
            organization_id=event_in.organization_id,
            source_identifier=event_in.source_identifier,
            employee_id=event_in.employee_id,
            payload=event_in.payload,
            processed=False,
        )
        created = await self.repo.create(db_event)
        return WorkplaceEventRead.model_validate(created)

    async def ingest_batch(self, batch_in: EventBatchIngestRequest) -> EventIngestResponse:
        """Persist a batch of workplace events."""
        event_ids: List[str] = []
        for item in batch_in.events:
            db_event = WorkplaceEvent(
                source=item.source,
                event_type=item.event_type,
                organization_id=item.organization_id,
                source_identifier=item.source_identifier,
                employee_id=item.employee_id,
                payload=item.payload,
                processed=False,
            )
            created = await self.repo.create(db_event)
            event_ids.append(created.id)

        return EventIngestResponse(
            ingested_count=len(event_ids),
            event_ids=event_ids,
            status="success",
        )

    async def list_events(self, limit: int = 50, offset: int = 0) -> List[WorkplaceEventRead]:
        """Query historical workplace events."""
        events = await self.repo.get_all(limit=limit, offset=offset)
        return [WorkplaceEventRead.model_validate(e) for e in events]
