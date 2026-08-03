"""
PlantMind Runtime

Central runtime model representing the current state
of the PlantMind platform.
"""

from __future__ import annotations

from app.config import settings
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

    def mark_ready(self) -> None:
        """
        Mark the platform runtime as ready.
        """
        self.ready = True

    def mark_not_ready(self) -> None:
        """
        Mark the platform runtime as not ready.
        """
        self.ready = False

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