from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class WorkplaceGraphState(TypedDict, total=False):
    """LangGraph shared state passed across workplace intelligence agents."""

    target_id: str
    event_ids: List[str]
    parameters: Dict[str, Any]

    # Individual Agent Results
    architect_output: Optional[Dict[str, Any]]
    configuration_output: Optional[Dict[str, Any]]
    contribution_output: Optional[Dict[str, Any]]
    fairness_output: Optional[Dict[str, Any]]
    culture_output: Optional[Dict[str, Any]]
    environment_output: Optional[Dict[str, Any]]
    reward_output: Optional[Dict[str, Any]]
    accountability_output: Optional[Dict[str, Any]]

    # Synthesis
    overall_score: Optional[float]
    summary: str
    errors: List[str]
