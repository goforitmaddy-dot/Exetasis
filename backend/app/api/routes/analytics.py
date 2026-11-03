from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.analytics import WorkplaceSummaryResponse
from backend.app.services.analytics_service import AnalyticsService

analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_analytics_service(session: AsyncSession = Depends(get_db)) -> AnalyticsService:
    """Dependency provider for AnalyticsService."""
    return AnalyticsService(session)


@analytics_router.get("/summary", response_model=WorkplaceSummaryResponse)
async def get_workplace_summary(
    service: AnalyticsService = Depends(get_analytics_service),
) -> WorkplaceSummaryResponse:
    """Retrieve high-level workplace score, fairness index, and department metrics."""
    return await service.get_summary()
