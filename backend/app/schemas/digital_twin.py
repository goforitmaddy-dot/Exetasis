from datetime import datetime, timezone
from typing import Any, Dict, List, Literal
from pydantic import BaseModel, Field


class Vector3D(BaseModel):
    """3D Cartesian coordinates."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class DigitalTwinNodeSchema(BaseModel):
    """Spatial node in the 3D twin."""

    id: str
    node_type: Literal["desk", "meeting_room", "breakout_zone", "employee_avatar"]
    label: str
    position: Vector3D
    status: Literal["idle", "active", "collaborating", "alert", "focused"] = "idle"
    state_metadata: Dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DigitalTwinSnapshotResponse(BaseModel):
    """Full snapshot of the current 3D digital twin world state."""

    office_name: str
    grid_size: Vector3D
    nodes: List[DigitalTwinNodeSchema]
    zones: List[Dict[str, Any]]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TwinClientMessage(BaseModel):
    """Client message sent over WebSocket."""

    action: Literal["subscribe", "ping", "focus_node"]
    node_id: str | None = None


class TwinServerUpdateMessage(BaseModel):
    """Server delta or event pulse broadcasted to 3D twin clients."""

    event_type: Literal["node_update", "pulse", "metric_alert", "pong"]
    node_id: str | None = None
    delta: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
