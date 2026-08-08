"""
PlantMind Runtime

Central runtime model representing the current state
of the PlantMind platform.
"""

from __future__ import annotations

from app.config import settings
from app.core.readiness import ReadinessEvidence
from app.core.runtime_state import RuntimeState


class Runtime:
    """
    Represents the current PlantMind runtime.
    """

    def __init__(self) -> None:
        self.platform_name = settings.APP_NAME
        self.version = settings.VERSION
        self.environment = settings.ENVIRONMENT
        self.deployment = settings.DEPLOYMENT_MODE

        self.state = RuntimeState.CREATED
        self.ready = False
        self._request_admission_enabled = False

    def request_readiness(self, evidence: ReadinessEvidence) -> None:
        """Validate readiness evidence and enter READY when complete."""
        if not evidence.is_complete:
            self.disable_request_admission()
            raise RuntimeError(
                "Mandatory runtime readiness requirements are not satisfied."
            )

        self.mark_ready()

    def mark_ready(self) -> None:
        """
        Mark the platform runtime as ready.
        """
        self.state = RuntimeState.READY
        self.ready = True

    def mark_not_ready(self) -> None:
        """
        Mark the platform runtime as not ready.
        """
        self.state = RuntimeState.STOPPED
        self.ready = False

    def mark_stopping(self) -> None:
        """Mark the platform runtime as stopping."""
        self.state = RuntimeState.STOPPING
        self.ready = False
        self.disable_request_admission()

    def mark_failed(self) -> None:
        """
        Mark the platform runtime as failed.
        """
        self.state = RuntimeState.FAILED
        self.ready = False
        self.disable_request_admission()

    def enable_request_admission(self) -> None:
        """Enable request admission."""
        self._request_admission_enabled = True

    def disable_request_admission(self) -> None:
        """Disable request admission."""
        self._request_admission_enabled = False

    @property
    def is_request_admission_enabled(self) -> bool:
        """Return whether request admission is enabled."""
        return self._request_admission_enabled

    @property
    def is_ready(self) -> bool:
        """
        Return whether the platform runtime is ready.
        """
        return self.ready

    @property
    def status(self) -> dict[str, object]:
        """
        Return runtime information.
        """
        return {
            "platform": self.platform_name,
            "version": self.version,
            "environment": self.environment,
            "deployment": self.deployment,
            "state": self.state.value,
            "ready": self.ready,
        }


runtime = Runtime()