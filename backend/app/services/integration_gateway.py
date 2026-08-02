"""PlantMind Integration Gateway."""

from __future__ import annotations

from app.domain.observation import Observation
from app.services.orchestration.orchestration_service import (
    OrchestrationService,
)
from app.services.orchestration.workflow import WorkflowExecution


class IntegrationGateway:
    """
    Single entry point for external integrations.

    This gateway isolates external interfaces (API, AI agents,
    PI System, DCS, CLI, etc.) from the internal application
    architecture.
    """

    def __init__(
        self,
        orchestration_service: OrchestrationService | None = None,
    ) -> None:
        self._orchestration_service = (
            orchestration_service or OrchestrationService()
        )

    def execute(
        self,
        observations: tuple[Observation, ...],
    ) -> WorkflowExecution:
        """
        Execute one complete PlantMind workflow.
        """
        return self._orchestration_service.run(
            observations
        )