from typing import Any, Dict, List
from backend.app.core.logging import logger
from backend.app.schemas.events import WorkplaceEventCreate


class GitHubAdapter:
    """STUB: Adapter for ingesting GitHub PR, review, and commit activities."""

    def __init__(self, api_token: str = "mock-github-token") -> None:
        self.api_token = api_token

    @staticmethod
    def normalize_merged_pull_request(
        payload: Dict[str, Any], organization_id: str, employee_id: str | None = None
    ) -> WorkplaceEventCreate:
        """Normalize an authorized GitHub merged-PR webhook payload without inferring activity."""
        pr = payload.get("pull_request") or {}
        if payload.get("action") != "closed" or pr.get("merged") is not True:
            raise ValueError("Only merged pull requests can be normalized as pull_request_merged events.")
        author = pr.get("user") or {}
        merged_by = pr.get("merged_by") or {}
        repository = payload.get("repository") or {}
        return WorkplaceEventCreate(
            source="github",
            source_identifier=str(pr.get("node_id") or pr.get("id") or f"{repository.get('full_name', '')}#{pr.get('number', '')}"),
            organization_id=organization_id,
            event_type="pull_request_merged",
            # GitHub logins are not Exetasis employee IDs; require an explicit trusted mapping.
            employee_id=employee_id,
            payload={
                "repository": repository.get("full_name"),
                "pr_number": pr.get("number"),
                "title": pr.get("title"),
                "author_login": author.get("login"),
                "merged_by_login": merged_by.get("login"),
                "merged": True,
                # GitHub's merge payload does not provide task quality or mentorship evidence.
                "evidence": {},
            },
        )

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
