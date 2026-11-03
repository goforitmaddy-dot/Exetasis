from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.digital_twin import DigitalTwinSnapshotResponse
from backend.app.services.twin_service import TwinService

digital_twin_router = APIRouter(prefix="/digital-twin", tags=["Digital Twin"])


def get_twin_service(session: AsyncSession = Depends(get_db)) -> TwinService:
    """Dependency provider for TwinService."""
    return TwinService(session)


@digital_twin_router.get("/state", response_model=DigitalTwinSnapshotResponse)
async def get_digital_twin_state(
    service: TwinService = Depends(get_twin_service),
) -> DigitalTwinSnapshotResponse:
    """Retrieve full spatial snapshot (nodes, zones, metrics) of the workplace digital twin."""
    return await service.get_snapshot()
