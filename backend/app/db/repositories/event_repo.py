from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.db.models.event import WorkplaceEvent
from backend.app.db.repositories.base import BaseRepository


class EventRepository(BaseRepository[WorkplaceEvent]):
    """Repository handling WorkplaceEvent persistence and querying."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(WorkplaceEvent, session)

    async def get_unprocessed(self, limit: int = 50) -> List[WorkplaceEvent]:
        """Fetch unanalyzed workplace events."""
        result = await self.session.execute(
            select(WorkplaceEvent).filter(WorkplaceEvent.processed.is_(False)).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_employee(self, employee_id: str, limit: int = 50) -> List[WorkplaceEvent]:
        """Fetch workplace events associated with a specific employee."""
        result = await self.session.execute(
            select(WorkplaceEvent)
            .filter(WorkplaceEvent.employee_id == employee_id)
            .order_by(WorkplaceEvent.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
