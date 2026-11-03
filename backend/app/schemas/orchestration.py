from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class OrganisationContext(BaseModel):
    organisation_id: str
    name: str | None = None
    industry: str | None = None
    workplace_type: str | None = None
    configuration: dict[str, Any] = Field(default_factory=dict)


class EmployeeContext(BaseModel):
    employee_id: str
    role: str | None = None
    department: str | None = None


class WorkplaceConfiguration(BaseModel):
    workplace_type: str | None = None
    departments: list[str] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)


class ContributionEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    tasks_completed: int | None = Field(default=None, ge=0)
    tasks_assigned: int | None = Field(default=None, ge=0)
    difficulty_score: float | None = Field(default=None, ge=0, le=1)
    quality_score: float | None = Field(default=None, ge=0, le=1)
    review_acceptance_rate: float | None = Field(default=None, ge=0, le=1)
    rework_count: int | None = Field(default=None, ge=0)
    mentoring_count: int | None = Field(default=None, ge=0)
    unblock_count: int | None = Field(default=None, ge=0)
    evidence_refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_task_counts(self) -> "ContributionEvidence":
        if self.tasks_completed is not None and self.tasks_assigned is not None and self.tasks_completed > self.tasks_assigned:
            raise ValueError("tasks_completed cannot exceed tasks_assigned")
        return self


class ContributionDimension(BaseModel):
    name: str
    value: float = Field(ge=0, le=1)
    weight: float = Field(gt=0)
    description: str


class PartialContributionDimension(BaseModel):
    name: str
    available_components: dict[str, int]
    missing_components: list[str]
    explanation: str


class EvidenceReferenceAssessment(BaseModel):
    reference: str
    status: Literal["unverified"] = "unverified"
    explanation: str = "No source verification is implemented; this reference is retained for traceability only."


class ContributionConfidence(BaseModel):
    availability: float = Field(ge=0, le=1)
    required_completeness: float = Field(ge=0, le=1)
    validation: float = Field(ge=0, le=1)
    provenance: float = Field(ge=0, le=1)
    corroboration: float = Field(ge=0, le=1)
    explanation: str


class AgentResult(BaseModel):
    agent_name: str
    organisation_id: str | None = None
    related_event_id: str
    result: dict[str, Any]
    evidence_references: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    execution_status: Literal["completed", "failed", "skipped"]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContributionResult(BaseModel):
    agent_name: str = "contribution"
    target_id: str
    score: float | None = Field(default=None, ge=0, le=1)
    evaluation_status: Literal["evaluated", "insufficient_evidence", "invalid_evidence"]
    rationale: str
    evidence: ContributionEvidence
    dimensions_used: list[ContributionDimension] = Field(default_factory=list)
    dimensions_missing: list[str] = Field(default_factory=list)
    dimensions_partial: list[PartialContributionDimension] = Field(default_factory=list)
    evidence_validation_status: Literal["missing", "valid", "malformed"]
    validation_errors: list[str] = Field(default_factory=list)
    evidence_references: list[EvidenceReferenceAssessment] = Field(default_factory=list)
    confidence_assessment: ContributionConfidence
    confidence: float = Field(ge=0, le=1)


class FairnessFinding(BaseModel):
    finding: str
    evidence: list[str] = Field(default_factory=list)
    insufficient_data: bool = False
    human_review_recommended: bool = True


class CultureFinding(BaseModel):
    finding: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    requires_human_review: bool = True


class EnvironmentFinding(BaseModel):
    metric: str
    observed_value: float | None = None
    status: str
    explanation: str


class RewardRecommendation(BaseModel):
    target_id: str
    proposed_reward: str
    supporting_evidence: list[str] = Field(default_factory=list)
    reason: str
    fairness_checks: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    outstanding_concerns: list[str] = Field(default_factory=list)
    approval_status: Literal["pending", "approved", "rejected"] = "pending"


class HumanApproval(BaseModel):
    id: str
    related_event_id: str
    target_id: str
    action_type: str
    status: Literal["pending", "approved", "rejected"] = "pending"
    reviewer_id: str | None = None
    reviewed_at: datetime | None = None


class DigitalTwinUpdate(BaseModel):
    organization_id: str | None = None
    related_event_id: str
    update_type: str
    employee_or_department_id: str | None = None
    metric_or_status: dict[str, Any] = Field(default_factory=dict)
    summary: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EventOrchestrationRequest(BaseModel):
    event: dict[str, Any] | None = None
    event_id: str | None = None


class ApprovalDecisionRequest(BaseModel):
    decision: Literal["approved", "rejected"]
    reviewer_id: str
    note: str | None = None


class OrchestrationRunRead(BaseModel):
    run_id: str
    event_id: str
    organisation_id: str | None = None
    status: str
    result: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    created_at: datetime
    updated_at: datetime
