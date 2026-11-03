from pathlib import Path
from backend.app.core.logging import logger
from backend.app.schemas.agents import (
    AccountabilityAgentInput,
    AccountabilityAgentOutput,
)
from backend.app.services.llm.client import LLMClient

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_system_prompt() -> str:
    """Load the agent's system prompt from external markdown file."""
    prompt_file = PROMPTS_DIR / "system.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "STUB: Accountability Agent default prompt."


class AccountabilityAgent:
    """STUB: Accountability agent tracking commitments and delivery reliability."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.system_prompt = load_system_prompt()

    async def evaluate(self, input_data: AccountabilityAgentInput) -> AccountabilityAgentOutput:
        """STUB: Execute commitment accountability assessment."""
        logger.debug("[STUB] Executing AccountabilityAgent for target: %s", input_data.target_id)

        # STUB: Simulated accountability tracking
        return AccountabilityAgentOutput(
            target_id=input_data.target_id,
            score=0.95,
            rationale="STUB: 100% of sprint action items resolved or proactively re-scoped with stakeholder buy-in.",
            findings=[
                "Zero unresolved retro action items older than 14 days",
                "Dependencies communicated proactively > 48h prior to sprint freeze",
            ],
            reliability_index=0.98,
            pending_followups=[],
            metadata={"stub": True, "tracked_commitments": len(input_data.commitments_tracked)},
        )
