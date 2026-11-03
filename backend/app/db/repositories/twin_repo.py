from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.db.models.digital_twin import DigitalTwinNode
from backend.app.db.repositories.base import BaseRepository


class DigitalTwinRepository(BaseRepository[DigitalTwinNode]):
    """Repository managing 3D Digital Twin spatial nodes and zones."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DigitalTwinNode, session)

    async def get_by_node_type(self, node_type: str) -> List[DigitalTwinNode]:
        """Fetch nodes by type ('desk', 'meeting_room', 'avatar', etc.)."""
        result = await self.session.execute(
            select(DigitalTwinNode).filter(DigitalTwinNode.node_type == node_type)
        )
        return list(result.scalars().all())
