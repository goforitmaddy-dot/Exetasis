from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.repositories.employee_repo import EmployeeRepository
from backend.app.db.repositories.event_repo import EventRepository
from backend.app.db.repositories.metric_repo import MetricRepository
from backend.app.schemas.analytics import DepartmentScore, WorkplaceSummaryResponse


class AnalyticsService:
    """Service computing aggregated workplace intelligence summaries."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.employee_repo = EmployeeRepository(session)
        self.event_repo = EventRepository(session)
        self.metric_repo = MetricRepository(session)

    async def get_summary(self) -> WorkplaceSummaryResponse:
        """Generate high-level workplace score and department summaries."""
        employees = await self.employee_repo.get_all(limit=100)
        events = await self.event_repo.get_all(limit=100)

        total_emp = len(employees)
        total_ev = len(events)

        # STUB: Synthesized baseline summary values
        departments = [
            DepartmentScore(
                department="Engineering",
                headcount=max(1, total_emp // 2),
                activity_score=0.91,
                fairness_score=0.94,
                culture_health=0.88,
            ),
            DepartmentScore(
                department="Product & Design",
                headcount=max(1, total_emp // 3),
                activity_score=0.86,
                fairness_score=0.92,
                culture_health=0.90,
            ),
            DepartmentScore(
                department="Operations & People",
                headcount=max(1, total_emp // 6),
                activity_score=0.89,
                fairness_score=0.95,
                culture_health=0.93,
            ),
        ]

        return WorkplaceSummaryResponse(
            workplace_score=0.89,
            total_employees=total_emp,
            total_events_processed=total_ev,
            average_fairness_index=0.94,
            culture_vibe="High synergy with balanced review distribution",
            department_scores=departments,
            recent_insights=[
                "Code review response times improved by 14% this week",
                "Workload distribution across sprint items is within 95% fairness target",
                "Breakout Pod B utilization peaked during Wednesday sync",
            ],
        )
