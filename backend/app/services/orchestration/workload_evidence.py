from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ApplicationFacadeEntryEvidence:
    """Evidence that a workload entered through the canonical application facade."""

    workload_id: UUID


@dataclass(frozen=True, slots=True)
class WorkflowExecutionStartEvidence:
    """Evidence that a correlated workload reached concrete execution start."""

    workload_id: UUID


@dataclass(frozen=True, slots=True)
class OperationalWorkloadEvidence:
    """Correlated evidence for canonical operational workload execution."""

    facade_entry: ApplicationFacadeEntryEvidence
    execution_start: WorkflowExecutionStartEvidence

    def __post_init__(self) -> None:
        if self.facade_entry.workload_id != self.execution_start.workload_id:
            raise ValueError(
                "Operational workload evidence requires matching workload identities."
            )
