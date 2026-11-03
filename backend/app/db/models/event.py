import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import relationship

from backend.app.db.session import Base


class WorkplaceEvent(Base):
    """Workplace event captured from communication, version control, or calendar adapters."""

    __tablename__ = "workplace_events"

    id: str = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source: str = Column(String(50), nullable=False, index=True)  # e.g., 'slack', 'github', 'calendar'
    event_type: str = Column(String(100), nullable=False, index=True)  # e.g., 'pr_review', 'standup_message'
    employee_id: str | None = Column(String(36), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True, index=True)
    payload: dict = Column(JSON, nullable=False, default=dict)
    processed: bool = Column(Boolean, default=False, nullable=False, index=True)
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    employee = relationship("Employee", back_populates="events")
    evaluations = relationship("AgentEvaluation", back_populates="event", cascade="all, delete-orphan")
