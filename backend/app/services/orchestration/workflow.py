"""PlantMind orchestration workflow models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class WorkflowStage(StrEnum):
    """Execution stages for the PlantMind orchestration pipeline."""

    RECEIVED = "received"
    REASONING = "reasoning"
    PRESENTATION = "presentation"
    COMPLETED = "completed"


@dataclass(frozen=True, slots=True)
class WorkflowExecution:
    """Represents one completed orchestration workflow."""

    result: dict[str, object]
    stages: tuple[WorkflowStage, ...]

    @property
    def is_complete(self) -> bool:
        """Return True when the workflow reached the final stage."""
        return (
            len(self.stages) > 0
            and self.stages[-1] is WorkflowStage.COMPLETED
        )