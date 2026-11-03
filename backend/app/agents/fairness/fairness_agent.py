from pathlib import Path
from backend.app.core.logging import logger
from backend.app.schemas.agents import FairnessAgentInput, FairnessAgentOutput
from backend.app.services.llm.client import LLMClient

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_system_prompt() -> str:
    """Load the agent's system prompt from external markdown file."""
    prompt_file = PROMPTS_DIR / "system.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "STUB: Fairness Agent default prompt."


class FairnessAgent:
    """STUB: Fairness agent assessing workload equity and task allocation balance."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.system_prompt = load_system_prompt()

    async def evaluate(self, input_data: FairnessAgentInput) -> FairnessAgentOutput:
        """STUB: Execute fairness evaluation across peer cohort."""
        logger.debug("[STUB] Executing FairnessAgent for target: %s", input_data.target_id)

        # STUB: Simulated equity audit
        return FairnessAgentOutput(
            target_id=input_data.target_id,
            score=0.94,
            rationale="STUB: Workload and review distribution is well-balanced across the squad.",
            findings=[
                "On-call rotation shifts evenly distributed over past 60 days",
                "PR review turnaround times exhibit no statistical variance across seniority levels",
            ],
            disparity_detected=False,
            fairness_index=0.96,
            metadata={"stub": True, "peers_analyzed": len(input_data.peer_group_ids)},
        )
