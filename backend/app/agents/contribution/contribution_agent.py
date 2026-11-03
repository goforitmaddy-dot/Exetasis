from pathlib import Path
from backend.app.core.logging import logger
from backend.app.schemas.agents import ContributionAgentInput, ContributionAgentOutput
from backend.app.services.llm.client import LLMClient

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_system_prompt() -> str:
    """Load the agent's system prompt from external markdown file."""
    prompt_file = PROMPTS_DIR / "system.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "STUB: Contribution Agent default prompt."


class ContributionAgent:
    """STUB: Contribution agent evaluating multi-channel workplace output."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.system_prompt = load_system_prompt()

    async def evaluate(self, input_data: ContributionAgentInput) -> ContributionAgentOutput:
        """STUB: Execute contribution analysis for target subject."""
        logger.debug("[STUB] Executing ContributionAgent for target: %s", input_data.target_id)

        # STUB: Simulated contribution synthesis
        return ContributionAgentOutput(
            target_id=input_data.target_id,
            score=0.88,
            rationale="STUB: High velocity in PR reviews and technical design discussions over the last sprint.",
            findings=[
                "Authored 6 merged PRs and conducted 14 peer reviews",
                "Assisted onboarding of 2 junior engineers in team Slack channel",
            ],
            impact_level="high",
            primary_contributions=["Architecture reviews", "Core backend APIs", "Mentorship"],
            metadata={"stub": True, "timeframe_days": input_data.timeframe_days},
        )
