from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.db.models.employee import Employee
from backend.app.db.repositories.base import BaseRepository


class EmployeeRepository(BaseRepository[Employee]):
    """Repository handling Employee persistence operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Employee, session)

    async def get_by_email(self, email: str) -> Optional[Employee]:
        """Lookup employee by unique email."""
        result = await self.session.execute(select(Employee).filter(Employee.email == email))
        return result.scalars().first()
