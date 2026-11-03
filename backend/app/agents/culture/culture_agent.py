from pathlib import Path
from backend.app.core.logging import logger
from backend.app.schemas.agents import CultureAgentInput, CultureAgentOutput
from backend.app.services.llm.client import LLMClient

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_system_prompt() -> str:
    """Load the agent's system prompt from external markdown file."""
    prompt_file = PROMPTS_DIR / "system.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "STUB: Culture Agent default prompt."


class CultureAgent:
    """STUB: Culture agent evaluating organizational sentiment and collaborative camaraderie."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.system_prompt = load_system_prompt()

    async def evaluate(self, input_data: CultureAgentInput) -> CultureAgentOutput:
        """STUB: Execute culture and vibe assessment."""
        logger.debug("[STUB] Executing CultureAgent for target: %s", input_data.target_id)

        # STUB: Simulated culture analysis
        return CultureAgentOutput(
            target_id=input_data.target_id,
            score=0.85,
            rationale="STUB: High psychological safety and frequent informal recognition observed.",
            findings=[
                "Cross-functional shoutouts up 22% compared to last week",
                "Constructive critique norms respected during PR code reviews",
            ],
            vibe_descriptor="energized and collaborative",
            collaboration_health=0.87,
            metadata={"stub": True, "collaboration_edges": input_data.collaboration_edges_count},
        )
