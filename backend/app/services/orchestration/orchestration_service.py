"""Unified PlantMind orchestration entry point."""

from __future__ import annotations

from app.domain.observation import Observation
from app.services.orchestration.workflow import WorkflowExecution
from app.services.orchestration.workflow_executor import WorkflowExecutor
from app.domain.operational_workload_evidence import (
    ApplicationFacadeEntryEvidence,
)


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
        facade_entry_evidence: ApplicationFacadeEntryEvidence | None = None,
    ) -> WorkflowExecution:
        """Run the complete PlantMind workflow."""
        return self._executor.execute(
            observations,
            facade_entry_evidence=facade_entry_evidence,
        )
