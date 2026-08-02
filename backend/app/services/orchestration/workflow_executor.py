"""Execute the PlantMind orchestration workflow."""

from __future__ import annotations

from app.domain.observation import Observation
from app.services.orchestration.workflow import (
    WorkflowExecution,
    WorkflowStage,
)
from app.services.reasoning.presentation_service import PresentationService


class WorkflowExecutor:
    """Execute the complete PlantMind workflow."""

    def __init__(
        self,
        presentation_service: PresentationService | None = None,
    ) -> None:
        self._presentation_service = (
            presentation_service or PresentationService()
        )

    def execute(
        self,
        observations: tuple[Observation, ...],
    ) -> WorkflowExecution:
        stages = (
            WorkflowStage.RECEIVED,
            WorkflowStage.REASONING,
            WorkflowStage.PRESENTATION,
            WorkflowStage.COMPLETED,
        )

        result = self._presentation_service.generate(
            observations
        )

        return WorkflowExecution(
            result=result,
            stages=stages,
        )