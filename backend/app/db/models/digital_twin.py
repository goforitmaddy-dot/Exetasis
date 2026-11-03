import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, JSON, String

from backend.app.db.session import Base


class DigitalTwinNode(Base):
    """Spatial node representation for the 3D Digital Twin visualization."""

    __tablename__ = "digital_twin_nodes"

    id: str = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    node_type: str = Column(String(50), nullable=False)  # 'desk', 'meeting_room', 'breakout_zone', 'avatar'
    label: str = Column(String(100), nullable=False)
    position_x: float = Column(Float, nullable=False, default=0.0)
    position_y: float = Column(Float, nullable=False, default=0.0)
    position_z: float = Column(Float, nullable=False, default=0.0)
    status: str = Column(String(50), nullable=False, default="idle")  # 'idle', 'active', 'collaborating', 'alert'
    state_metadata: dict = Column(JSON, nullable=False, default=dict)
    updated_at: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
