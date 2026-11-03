from datetime import datetime, timezone
from typing import Dict, List
from pydantic import BaseModel, Field


class DepartmentScore(BaseModel):
    department: str
    headcount: int
    activity_score: float
    fairness_score: float
    culture_health: float


class WorkplaceSummaryResponse(BaseModel):
    """Aggregate workplace analytics summary."""

    workplace_score: float = Field(..., ge=0.0, le=1.0, description="Overall health score (0-1)")
    total_employees: int
    total_events_processed: int
    average_fairness_index: float
    culture_vibe: str
    department_scores: List[DepartmentScore]
    recent_insights: List[str]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
