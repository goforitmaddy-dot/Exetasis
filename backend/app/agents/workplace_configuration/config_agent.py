from pathlib import Path
from backend.app.core.logging import logger
from backend.app.schemas.agents import (
    WorkplaceConfigurationInput,
    WorkplaceConfigurationOutput,
)
from backend.app.services.llm.client import LLMClient

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_system_prompt() -> str:
    """Load the agent's system prompt from external markdown file."""
    prompt_file = PROMPTS_DIR / "system.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "STUB: Workplace Configuration default prompt."


class WorkplaceConfigurationAgent:
    """STUB: Workplace Configuration agent managing zoning rules and spatial compliance."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.system_prompt = load_system_prompt()

    async def evaluate(self, input_data: WorkplaceConfigurationInput) -> WorkplaceConfigurationOutput:
        """STUB: Execute configuration and layout compliance check."""
        logger.debug("[STUB] Executing WorkplaceConfigurationAgent for target: %s", input_data.target_id)

        # STUB: Simulated layout configuration validation
        return WorkplaceConfigurationOutput(
            target_id=input_data.target_id,
            score=0.91,
            rationale="STUB: Workplace configuration satisfies 91% of team adjacency guidelines.",
            findings=[
                "Engineering squad desks aligned adjacent to QA test bench",
                "Distance between Design and Product pods is within optimal range (< 15m)",
            ],
            configuration_diff={"relocations_needed": 0, "desk_status": "optimal"},
            compliance_score=0.95,
            metadata={"stub": True, "applied_rules_count": len(input_data.rules_applied)},
        )
