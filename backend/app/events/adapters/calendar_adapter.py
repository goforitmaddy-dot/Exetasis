from typing import Any, Dict, List
from backend.app.core.logging import logger
from backend.app.schemas.events import WorkplaceEventCreate


class CalendarAdapter:
    """STUB: Adapter for ingesting meeting schedule and focus block events."""

    def __init__(self, service_account: str = "mock-calendar-sa") -> None:
        self.service_account = service_account

    async def fetch_scheduled_meetings(self, user_email: str) -> List[WorkplaceEventCreate]:
        """STUB: Fetch mock meeting events for a given user."""
        logger.debug("[STUB] CalendarAdapter fetching events for user: %s", user_email)

        # STUB: Simulated normalized event records
        return [
            WorkplaceEventCreate(
                source="calendar",
                event_type="meeting_attended",
                employee_id="emp-001",
                payload={
                    "summary": "Sprint Retro & Planning",
                    "attendee_count": 8,
                    "duration_minutes": 45,
                    "focus_time_remaining_hours": 3.5,
                },
            )
        ]
