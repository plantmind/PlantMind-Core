from __future__ import annotations

from dataclasses import dataclass

from app.core.operational_transition_coordinator import (
    OperationalTransitionCoordinator,
)
from app.core.operational_transition_evidence import (
    OperationalTransitionEvidence,
)
from app.domain.observation import Observation
from app.services.application_facade import ApplicationFacade
from app.services.orchestration.workflow import WorkflowExecution


@dataclass(frozen=True, slots=True)
class OperationalTransitionApplicationResult:
    """Result of one explicit operational-transition application request."""

    workflow_execution: WorkflowExecution
    operational_transition_evidence: OperationalTransitionEvidence


class OperationalTransitionApplicationService:
    """Coordinate the explicit operational-transition application use case."""

    def __init__(
        self,
        application_facade: ApplicationFacade,
        operational_transition_coordinator: OperationalTransitionCoordinator,
    ) -> None:
        self._application_facade = application_facade
        self._operational_transition_coordinator = (
            operational_transition_coordinator
        )

    @property
    def application_facade(self) -> ApplicationFacade:
        """Return the canonical application facade dependency."""
        return self._application_facade

    @property
    def operational_transition_coordinator(
        self,
    ) -> OperationalTransitionCoordinator:
        """Return the canonical operational-transition coordinator."""
        return self._operational_transition_coordinator

    def request_operational(
        self,
        observations: tuple[Observation, ...],
    ) -> OperationalTransitionApplicationResult:
        """Execute workload and explicitly request operational transition."""
        workflow_execution = self._application_facade.analyze(observations)

        transition_evidence = (
            self._operational_transition_coordinator.request_operational(
                workflow_execution.operational_workload_evidence
            )
        )

        return OperationalTransitionApplicationResult(
            workflow_execution=workflow_execution,
            operational_transition_evidence=transition_evidence,
        )
