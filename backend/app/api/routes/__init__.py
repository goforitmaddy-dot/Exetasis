from backend.app.api.routes.health import health_router
from backend.app.api.routes.events import events_router
from backend.app.api.routes.agents import agents_router
from backend.app.api.routes.analytics import analytics_router
from backend.app.api.routes.digital_twin import digital_twin_router

__all__ = [
    "health_router",
    "events_router",
    "agents_router",
    "analytics_router",
    "digital_twin_router",
]
