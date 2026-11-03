from typing import Any, Dict, List
from backend.app.core.logging import logger
from backend.app.schemas.events import WorkplaceEventCreate


class GitHubAdapter:
    """STUB: Adapter for ingesting GitHub PR, review, and commit activities."""

    def __init__(self, api_token: str = "mock-github-token") -> None:
        self.api_token = api_token

    async def fetch_repository_events(self, repo: str, limit: int = 10) -> List[WorkplaceEventCreate]:
        """STUB: Fetch mock recent GitHub development events."""
        logger.debug("[STUB] GitHubAdapter fetching events for repo: %s", repo)

        # STUB: Simulated normalized event records
        return [
            WorkplaceEventCreate(
                source="github",
                event_type="pull_request_reviewed",
                employee_id="emp-001",
                payload={
                    "repo": repo,
                    "pr_number": 42,
                    "state": "approved",
                    "comments_count": 5,
                },
            ),
            WorkplaceEventCreate(
                source="github",
                event_type="commit_pushed",
                employee_id="emp-003",
                payload={
                    "repo": repo,
                    "branch": "feature/digital-twin",
                    "commit_hash": "a1b2c3d",
                },
            ),
        ]
