"""PlantMind application facade."""

from __future__ import annotations

from uuid import uuid4

from app.domain.observation import Observation
from app.services.integration_gateway import IntegrationGateway
from app.services.orchestration.workflow import WorkflowExecution
from app.services.orchestration.workload_evidence import (
    ApplicationFacadeEntryEvidence,
)


class ApplicationFacade:
    """Stable application-level entry point.

    External interfaces should use this facade instead of depending
    directly on internal orchestration or reasoning services.
    """

    def __init__(
        self,
        gateway: IntegrationGateway | None = None,
    ) -> None:
        self._gateway = gateway or IntegrationGateway()

    def analyze(
        self,
        observations: tuple[Observation, ...],
    ) -> WorkflowExecution:
        """Run one complete PlantMind analysis workflow."""
        facade_entry_evidence = ApplicationFacadeEntryEvidence(
            workload_id=uuid4()
        )

        return self._gateway.execute(
            observations,
            facade_entry_evidence=facade_entry_evidence,
        )
