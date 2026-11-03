from pathlib import Path
from backend.app.core.logging import logger
from backend.app.schemas.agents import WorkplaceArchitectInput, WorkplaceArchitectOutput
from backend.app.services.llm.client import LLMClient

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_system_prompt() -> str:
    """Load the agent's system prompt from external markdown file."""
    prompt_file = PROMPTS_DIR / "system.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "STUB: Workplace Architect default prompt."


class WorkplaceArchitectAgent:
    """STUB: Workplace Architect agent evaluating spatial layout and capacity distribution."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.system_prompt = load_system_prompt()

    async def evaluate(self, input_data: WorkplaceArchitectInput) -> WorkplaceArchitectOutput:
        """STUB: Execute architecture analysis on target layout or capacity."""
        logger.debug("[STUB] Executing WorkplaceArchitectAgent for target: %s", input_data.target_id)

        # STUB: Placeholder logic simulating architectural space evaluation
        return WorkplaceArchitectOutput(
            target_id=input_data.target_id,
            score=0.82,
            rationale="STUB: Space utilization balanced across engineering and product clusters.",
            findings=[
                "Focus pod utilization at 78% capacity",
                "Meeting rooms in Zone B experience peak contention from 2-4 PM",
            ],
            recommended_zones=["Focus Pod Alpha", "Collaboration Commons Beta"],
            space_utilization_ratio=0.78,
            metadata={"stub": True, "evaluated_zones_count": 4},
        )
