import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, JSON, String

from backend.app.db.session import Base


class OrchestrationRun(Base):
    """Traceable execution record for event-driven LangGraph runs."""

    __tablename__ = "orchestration_runs"

    id: str = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id: str = Column(String(36), nullable=False, index=True)
    organization_id: str | None = Column(String(36), nullable=True, index=True)
    status: str = Column(String(30), nullable=False, default="pending", index=True)
    result: dict = Column(JSON, nullable=False, default=dict)
    error: str | None = Column(String(500), nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
