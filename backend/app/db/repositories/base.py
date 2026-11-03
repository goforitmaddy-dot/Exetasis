from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic base async repository for database operations."""

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, item_id: str) -> Optional[ModelType]:
        """Fetch an entity by primary key."""
        result = await self.session.execute(select(self.model).filter(self.model.id == item_id))
        return result.scalars().first()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """Fetch multiple entities with limit and offset."""
        result = await self.session.execute(select(self.model).offset(offset).limit(limit))
        return list(result.scalars().all())

    async def create(self, entity: ModelType) -> ModelType:
        """Add and commit a new entity."""
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity: ModelType) -> None:
        """Delete an entity."""
        await self.session.delete(entity)
        await self.session.flush()
