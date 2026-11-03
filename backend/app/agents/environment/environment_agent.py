from pathlib import Path
from backend.app.core.logging import logger
from backend.app.schemas.agents import EnvironmentAgentInput, EnvironmentAgentOutput
from backend.app.services.llm.client import LLMClient

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_system_prompt() -> str:
    """Load the agent's system prompt from external markdown file."""
    prompt_file = PROMPTS_DIR / "system.md"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8")
    return "STUB: Environment Agent default prompt."


class EnvironmentAgent:
    """STUB: Environment agent monitoring workspace ambient comfort and sensory metrics."""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.system_prompt = load_system_prompt()

    async def evaluate(self, input_data: EnvironmentAgentInput) -> EnvironmentAgentOutput:
        """STUB: Execute environmental comfort assessment."""
        logger.debug("[STUB] Executing EnvironmentAgent for target: %s", input_data.target_id)

        # STUB: Simulated ambient evaluation
        return EnvironmentAgentOutput(
            target_id=input_data.target_id,
            score=0.79,
            rationale="STUB: Ambient levels generally comfortable; slight acoustic spike during afternoon scrum in Zone A.",
            findings=[
                "Ambient noise averaged 48 dB (optimal)",
                "Temperature maintained at 22.4°C across all floors",
            ],
            comfort_index=0.82,
            anomalies=["Minor noise spillover between Pod 3 and central hallway at 14:30"],
            metadata={
                "stub": True,
                "noise_db": input_data.noise_level_db,
                "temp_c": input_data.temperature_celsius,
            },
        )
