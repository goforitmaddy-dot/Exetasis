import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from backend.app.db.session import Base


class Employee(Base):
    """Employee entity representing an organization member."""

    __tablename__ = "employees"

    id: str = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: str = Column(String(120), nullable=False)
    email: str = Column(String(255), unique=True, nullable=False, index=True)
    role: str = Column(String(100), nullable=False)
    department: str = Column(String(100), nullable=False, index=True)
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    events = relationship("WorkplaceEvent", back_populates="employee", cascade="all, delete-orphan")
