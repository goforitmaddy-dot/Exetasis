from pathlib import Path
from backend.app.core.logging import logger
from backend.app.schemas.agents import RewardAgentInput, RewardAgentOutput
from backend.app.services.llm.client import LLMClient

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_system_prompt() -> str:
    """Load the agent's system prompt from external markdown file."""
    prompt_file = PROMPTS_DIR / "system.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "STUB: Reward Agent default prompt."


class RewardAgent:
    """STUB: Reward agent generating milestone recognitions and kudos."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.system_prompt = load_system_prompt()

    async def evaluate(self, input_data: RewardAgentInput) -> RewardAgentOutput:
        """STUB: Execute recognition and reward analysis."""
        logger.debug("[STUB] Executing RewardAgent for target: %s", input_data.target_id)

        # STUB: Simulated reward recommendation
        return RewardAgentOutput(
            target_id=input_data.target_id,
            score=0.92,
            rationale="STUB: Crucial unblocking work on data migration completed ahead of deadline.",
            findings=[
                "Resolved high-priority Sev-2 incident within 20 minutes",
                "Shared reusable incident playbook with the broader engineering team",
            ],
            recommended_tokens=150,
            kudos_message="Kudos for swift and exemplary teamwork on the database migration!",
            metadata={"stub": True, "milestones_count": len(input_data.milestones_achieved)},
        )
