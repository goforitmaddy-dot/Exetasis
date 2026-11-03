from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models.digital_twin import DigitalTwinNode
from backend.app.db.repositories.twin_repo import DigitalTwinRepository
from backend.app.schemas.digital_twin import (
    DigitalTwinNodeSchema,
    DigitalTwinSnapshotResponse,
    Vector3D,
)


class TwinService:
    """Service projecting workplace spatial entities into 3D digital twin coordinates."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = DigitalTwinRepository(session)

    async def get_snapshot(self) -> DigitalTwinSnapshotResponse:
        """Fetch current digital twin snapshot. Seeds default layout if empty."""
        db_nodes = await self.repo.get_all(limit=100)

        # STUB: If no nodes exist in DB yet, return default structured floorplan
        if not db_nodes:
            sample_nodes = [
                DigitalTwinNodeSchema(
                    id="desk-eng-01",
                    node_type="desk",
                    label="Eng Desk 1 (Lead)",
                    position=Vector3D(x=-3.0, y=0.5, z=-2.0),
                    status="active",
                    state_metadata={"occupant": "Alice Chen", "department": "Engineering"},
                ),
                DigitalTwinNodeSchema(
                    id="desk-eng-02",
                    node_type="desk",
                    label="Eng Desk 2 (Backend)",
                    position=Vector3D(x=-3.0, y=0.5, z=0.0),
                    status="focused",
                    state_metadata={"occupant": "Bob Smith", "department": "Engineering"},
                ),
                DigitalTwinNodeSchema(
                    id="desk-prod-01",
                    node_type="desk",
                    label="Product Desk 1",
                    position=Vector3D(x=3.0, y=0.5, z=-2.0),
                    status="collaborating",
                    state_metadata={"occupant": "Elena Rostova", "department": "Product"},
                ),
                DigitalTwinNodeSchema(
                    id="room-sync-01",
                    node_type="meeting_room",
                    label="Meeting Room Apex",
                    position=Vector3D(x=0.0, y=1.0, z=-5.0),
                    status="active",
                    state_metadata={"capacity": 8, "in_meeting": True},
                ),
                DigitalTwinNodeSchema(
                    id="breakout-lounge-01",
                    node_type="breakout_zone",
                    label="Café & Breakout Commons",
                    position=Vector3D(x=0.0, y=0.2, z=4.0),
                    status="idle",
                    state_metadata={"noise_db": 42.0},
                ),
            ]
        else:
            sample_nodes = [
                DigitalTwinNodeSchema(
                    id=n.id,
                    node_type=n.node_type,  # type: ignore
                    label=n.label,
                    position=Vector3D(x=n.position_x, y=n.position_y, z=n.position_z),
                    status=n.status,  # type: ignore
                    state_metadata=n.state_metadata,
                    updated_at=n.updated_at,
                )
                for n in db_nodes
            ]

        zones = [
            {"id": "zone-eng", "name": "Engineering Bay", "color": "#3B82F6", "bounds": {"min_x": -6, "max_x": -1, "min_z": -4, "max_z": 2}},
            {"id": "zone-prod", "name": "Product & Design", "color": "#10B981", "bounds": {"min_x": 1, "max_x": 6, "min_z": -4, "max_z": 2}},
            {"id": "zone-collab", "name": "Collaboration Commons", "color": "#8B5CF6", "bounds": {"min_x": -4, "max_x": 4, "min_z": 2, "max_z": 6}},
        ]

        return DigitalTwinSnapshotResponse(
            office_name="Exetasis Headquarters - Floor 3",
            grid_size=Vector3D(x=20.0, y=4.0, z=20.0),
            nodes=sample_nodes,
            zones=zones,
        )
