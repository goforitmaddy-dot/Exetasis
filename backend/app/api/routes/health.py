from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.core.config import settings
from backend.app.db.session import get_db

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("", response_model=Dict[str, Any])
async def check_health(session: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Check application health, database connectivity, and configured LLM provider."""
    db_status = "healthy"
    try:
        await session.execute(select(1))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": db_status,
        "llm_provider": settings.LLM_PROVIDER,
        "gemini_enabled": settings.GEMINI_ENABLED,
    }
