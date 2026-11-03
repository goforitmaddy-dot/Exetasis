from typing import Any, Dict, List
from backend.app.core.logging import logger
from backend.app.schemas.events import WorkplaceEventCreate


class SlackAdapter:
    """STUB: Adapter for ingesting Slack message and reaction events."""

    def __init__(self, bot_token: str = "mock-slack-token") -> None:
        self.bot_token = bot_token

    async def fetch_recent_messages(self, channel_id: str, limit: int = 10) -> List[WorkplaceEventCreate]:
        """STUB: Fetch mock recent Slack communication events."""
        logger.debug("[STUB] SlackAdapter fetching messages for channel: %s", channel_id)

        # STUB: Simulated normalized event records
        return [
            WorkplaceEventCreate(
                source="slack",
                event_type="channel_message",
                employee_id="emp-001",
                payload={
                    "channel": channel_id,
                    "text": "Huge thank you to the team for fixing the release pipeline!",
                    "reactions": [{"name": "clap", "count": 4}],
                },
            ),
            WorkplaceEventCreate(
                source="slack",
                event_type="huddle_participated",
                employee_id="emp-002",
                payload={
                    "channel": channel_id,
                    "duration_minutes": 18,
                },
            ),
        ]
