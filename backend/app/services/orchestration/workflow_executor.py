"""Execute the PlantMind orchestration workflow."""

from __future__ import annotations

from app.domain.observation import Observation
from app.services.orchestration.workflow import (
    WorkflowExecution,
    WorkflowStage,
)
from app.services.orchestration.workload_evidence import (
    ApplicationFacadeEntryEvidence,
    OperationalWorkloadEvidence,
    WorkflowExecutionStartEvidence,
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
        facade_entry_evidence: ApplicationFacadeEntryEvidence | None = None,
    ) -> WorkflowExecution:
        stages = (
            WorkflowStage.RECEIVED,
            WorkflowStage.REASONING,
            WorkflowStage.PRESENTATION,
            WorkflowStage.COMPLETED,
        )

        operational_workload_evidence = None

        if facade_entry_evidence is not None:
            execution_start = WorkflowExecutionStartEvidence(
                workload_id=facade_entry_evidence.workload_id
            )
            operational_workload_evidence = OperationalWorkloadEvidence(
                facade_entry=facade_entry_evidence,
                execution_start=execution_start,
            )

        result = self._presentation_service.generate(
            observations
        )

        return WorkflowExecution(
            result=result,
            stages=stages,
            operational_workload_evidence=operational_workload_evidence,
        )
