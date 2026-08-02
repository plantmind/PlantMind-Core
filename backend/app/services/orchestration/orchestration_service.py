"""Unified PlantMind orchestration entry point."""

from __future__ import annotations

from app.domain.observation import Observation
from app.services.orchestration.workflow import WorkflowExecution
from app.services.orchestration.workflow_executor import WorkflowExecutor


class OrchestrationService:
    """Public entry point for PlantMind orchestration."""

    def __init__(
        self,
        executor: WorkflowExecutor | None = None,
    ) -> None:
        self._executor = executor or WorkflowExecutor()

    def run(
        self,
        observations: tuple[Observation, ...],
    ) -> WorkflowExecution:
        """Run the complete PlantMind workflow."""
        return self._executor.execute(observations)