from pathlib import Path
from typing import Any

from pydantic import ValidationError

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.schemas.agents import ContributionAgentInput, ContributionAgentOutput
from backend.app.schemas.orchestration import (
    ContributionConfidence,
    ContributionDimension,
    ContributionEvidence,
    EvidenceReferenceAssessment,
    PartialContributionDimension,
)
from backend.app.services.llm.client import LLMClient

PROMPTS_DIR = Path(__file__).parent / "prompts"
MINIMUM_SCORE_DIMENSIONS = 2

DIMENSION_DESCRIPTIONS = {
    "task_completion": "Compares completed tasks with assigned tasks; measures delivery against known commitments.",
    "difficulty": "Represents documented task difficulty; prevents counting easy and hard work as equivalent.",
    "quality": "Represents documented work quality; distinguishes completion from a usable outcome.",
    "review_acceptance": "Represents the acceptance rate of reviewed work; indicates whether work meets review criteria.",
    "rework": "Converts rework count to 1 - rework/completed tasks; reflects avoidable correction burden.",
    "mentoring_unblocking": "Normalizes documented mentoring plus unblock counts by four, capped at one.",
}
REQUIRED_COMPLETENESS_DIMENSIONS = {"task_completion", "difficulty", "quality"}
UNVERIFIED_PROVENANCE_FACTOR = 0.5
UNCORROBORATED_FACTOR = 0.75


def load_system_prompt() -> str:
    prompt_file = PROMPTS_DIR / "system.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "Explain only the supplied evidence. Never invent evidence or modify the deterministic score."


class ContributionAgent:
    """Deterministic, evidence-gated contribution scoring with LLM-generated explanation."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.system_prompt = load_system_prompt()

    @staticmethod
    def _dimensions(
        evidence: ContributionEvidence,
    ) -> tuple[dict[str, float], list[str], list[PartialContributionDimension]]:
        values: dict[str, float] = {}
        partial: list[PartialContributionDimension] = []
        if evidence.tasks_completed is not None and evidence.tasks_assigned is not None and evidence.tasks_assigned > 0:
            values["task_completion"] = min(1.0, evidence.tasks_completed / evidence.tasks_assigned)
        if evidence.difficulty_score is not None:
            values["difficulty"] = evidence.difficulty_score
        if evidence.quality_score is not None:
            values["quality"] = evidence.quality_score
        if evidence.review_acceptance_rate is not None:
            values["review_acceptance"] = evidence.review_acceptance_rate
        if evidence.rework_count is not None and evidence.tasks_completed is not None and evidence.tasks_completed > 0:
            values["rework"] = max(0.0, 1.0 - evidence.rework_count / evidence.tasks_completed)
        mentoring_available = evidence.mentoring_count is not None
        unblock_available = evidence.unblock_count is not None
        if mentoring_available and unblock_available:
            values["mentoring_unblocking"] = min(1.0, (evidence.mentoring_count + evidence.unblock_count) / 4.0)
        elif mentoring_available or unblock_available:
            available_components = {
                key: value
                for key, value in {
                    "mentoring_count": evidence.mentoring_count,
                    "unblock_count": evidence.unblock_count,
                }.items()
                if value is not None
            }
            missing_components = [key for key, value in {
                "mentoring_count": evidence.mentoring_count,
                "unblock_count": evidence.unblock_count,
            }.items() if value is None]
            partial.append(PartialContributionDimension(
                name="mentoring_unblocking",
                available_components=available_components,
                missing_components=missing_components,
                explanation="The available count is retained but this combined dimension is not scored until both counts are supplied.",
            ))
        missing = [name for name in DIMENSION_DESCRIPTIONS if name not in values]
        return values, missing, partial

    @staticmethod
    def _confidence(
        dimensions: dict[str, float],
        *,
        validation_status: str,
        partial_dimensions: list[PartialContributionDimension],
    ) -> tuple[float, ContributionConfidence]:
        partial_coverage = sum(
            len(item.available_components) / 2.0
            for item in partial_dimensions
        )
        available_units = len(dimensions) + partial_coverage
        measured = available_units > 0
        availability = min(1.0, available_units / len(DIMENSION_DESCRIPTIONS))
        completeness = len(REQUIRED_COMPLETENESS_DIMENSIONS.intersection(dimensions)) / len(REQUIRED_COMPLETENESS_DIMENSIONS)
        validation = 0.0 if validation_status == "malformed" else 1.0
        provenance = UNVERIFIED_PROVENANCE_FACTOR if measured and validation else 0.0
        corroboration = UNCORROBORATED_FACTOR if measured and validation else 0.0
        confidence = round(availability * completeness * validation * provenance * corroboration, 4)
        explanation = (
            f"Confidence index = availability ({available_units:g}/{len(DIMENSION_DESCRIPTIONS)} dimension equivalents; "
            f"including {partial_coverage:g} partial) × "
            f"required completeness ({len(REQUIRED_COMPLETENESS_DIMENSIONS.intersection(dimensions))}/"
            f"{len(REQUIRED_COMPLETENESS_DIMENSIONS)}) × validation ({validation:.2f}) × "
            f"provenance ({provenance:.2f}; measurements are not source-verified) × "
            f"corroboration ({corroboration:.2f}; independent corroboration is not implemented). "
            "Reference-string count does not affect confidence. This index is an MVP evidence-quality indicator, not a calibrated probability."
        )
        assessment = ContributionConfidence(
            availability=round(availability, 4),
            required_completeness=round(completeness, 4),
            validation=validation,
            provenance=provenance,
            corroboration=corroboration,
            explanation=explanation,
        )
        return confidence, assessment

    async def evaluate(self, input_data: ContributionAgentInput) -> ContributionAgentOutput:
        """Validate evidence, calculate a weighted score, then ask the LLM only for explanation."""
        context = input_data.context
        raw: Any = context.get("evidence", input_data.activity_metrics)
        raw_fields = set(raw) if isinstance(raw, dict) else set()
        measurements = {
            "tasks_completed", "tasks_assigned", "difficulty_score", "quality_score",
            "review_acceptance_rate", "rework_count", "mentoring_count", "unblock_count",
        }
        has_measurement = any(name in raw_fields and raw[name] is not None for name in measurements)
        validation_errors: list[str] = []
        if raw is None or raw == {}:
            evidence = ContributionEvidence()
            validation_status = "missing"
        else:
            try:
                evidence = ContributionEvidence.model_validate(raw)
                validation_status = "valid" if has_measurement else "missing"
            except ValidationError as exc:
                evidence = ContributionEvidence()
                validation_status = "malformed"
                validation_errors = [
                    f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']} ({item['type']})"
                    for item in exc.errors()
                ]
                logger.info("Malformed contribution evidence for target %s: %s", input_data.target_id, validation_errors)

        values, missing, partial = self._dimensions(evidence)
        if validation_status == "malformed":
            evaluation_status = "invalid_evidence"
            score: float | None = None
            values = {}
        elif len(values) < MINIMUM_SCORE_DIMENSIONS:
            evaluation_status = "insufficient_evidence"
            score = None
        else:
            evaluation_status = "evaluated"
            weights = settings.CONTRIBUTION_DIMENSION_WEIGHTS
            total_weight = sum(weights[name] for name in values)
            score = round(sum(value * weights[name] for name, value in values.items()) / total_weight, 4)
            score = min(1.0, max(0.0, score))

        confidence, confidence_assessment = self._confidence(
            values,
            validation_status=validation_status,
            partial_dimensions=partial,
        )
        references = [
            EvidenceReferenceAssessment(reference=reference)
            for reference in evidence.evidence_refs
        ]
        dimensions_used = [
            ContributionDimension(
                name=name,
                value=value,
                weight=settings.CONTRIBUTION_DIMENSION_WEIGHTS[name],
                description=DIMENSION_DESCRIPTIONS[name],
            )
            for name, value in values.items()
        ]

        if evaluation_status == "invalid_evidence":
            rationale = "Evidence validation failed; no contribution score was calculated."
        else:
            prompt_score = "null" if score is None else f"{score:.4f}"
            prompt = (
                "Explain this contribution result using only the supplied facts. Do not add evidence or numbers; "
                "do not recalculate or change the score. "
                f"Target={input_data.target_id}; evaluation_status={evaluation_status}; score={prompt_score}; "
                f"workplace_context={context.get('organization', {})}; role_context={context.get('employee', {})}; "
                f"dimensions_used={[dimension.model_dump() for dimension in dimensions_used]}; "
                f"dimensions_missing={missing}; dimensions_partial={[dimension.model_dump() for dimension in partial]}; "
                f"evidence={evidence.model_dump()}; "
                f"evidence_references={[reference.model_dump() for reference in references]}"
            )
            try:
                rationale = await self.llm_client.generate(prompt, self.system_prompt)
                if not rationale or rationale.startswith("STUB:"):
                    rationale = "Explanation unavailable; the reported score and evidence status come from deterministic Python calculations."
            except Exception as exc:
                logger.warning("Contribution explanation unavailable for %s: %s", input_data.target_id, exc)
                rationale = "Explanation unavailable; the reported score and evidence status come from deterministic Python calculations."

        metadata = {
            "evaluation_status": evaluation_status,
            "evidence_validation_status": validation_status,
            "validation_errors": validation_errors,
            "dimensions_used": [dimension.model_dump() for dimension in dimensions_used],
            "dimensions_missing": missing,
            "dimensions_partial": [dimension.model_dump() for dimension in partial],
            "evidence": evidence.model_dump(),
            "evidence_references": [reference.model_dump() for reference in references],
            "confidence": confidence,
            "confidence_assessment": confidence_assessment.model_dump(),
            "deterministic_score": True,
        }
        impact = "insufficient_evidence" if score is None else "high" if score >= 0.8 else "standard" if score >= 0.4 else "low"
        return ContributionAgentOutput(
            target_id=input_data.target_id,
            score=score,
            evaluation_status=evaluation_status,
            rationale=rationale,
            findings=(
                [f"Used dimension: {name}" for name in values]
                + [f"Missing dimension: {name}" for name in missing]
                + [
                    f"Partial dimension: {item.name}; available={item.available_components}; missing={item.missing_components}."
                    for item in partial
                ]
            ),
            dimensions_used=[dimension.model_dump() for dimension in dimensions_used],
            dimensions_missing=missing,
            dimensions_partial=[dimension.model_dump() for dimension in partial],
            evidence_validation_status=validation_status,
            validation_errors=validation_errors,
            evidence_references=[reference.model_dump() for reference in references],
            confidence=confidence,
            confidence_assessment=confidence_assessment.model_dump(),
            impact_level=impact,
            primary_contributions=[],
            metadata=metadata,
        )
