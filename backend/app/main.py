from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import (
    agents_router,
    analytics_router,
    digital_twin_router,
    events_router,
    health_router,
)
from backend.app.core.config import settings
from backend.app.core.logging import logger, setup_logging
from backend.app.db.session import init_db
from backend.app.websocket.routes import ws_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context: initialize database tables and resources."""
    setup_logging()
    logger.info("Initializing %s v0.1.0 in %s mode...", settings.APP_NAME, settings.APP_ENV)
    await init_db()
    logger.info("Database schema verified.")
    yield
    logger.info("Shutting down %s...", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-agent workplace intelligence platform with 3D digital twin visualization.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount REST API Routers
app.include_router(health_router, prefix="/api")
app.include_router(events_router, prefix="/api")
app.include_router(agents_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(digital_twin_router, prefix="/api")

# Mount WebSocket Router
app.include_router(ws_router)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "docs": "/docs",
        "api": "/api",
    }
