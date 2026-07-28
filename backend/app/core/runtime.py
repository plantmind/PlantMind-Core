"""
PlantMind Runtime

Central runtime model representing the current state
of the PlantMind platform.
"""

from __future__ import annotations

from app.config import settings


class Runtime:
    """
    Represents the current PlantMind runtime.
    """

    def __init__(self) -> None:
        self.platform_name = settings.APP_NAME
        self.version = settings.VERSION
        self.environment = settings.ENVIRONMENT
        self.deployment = settings.DEPLOYMENT_MODE

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
    def status(self) -> dict:
        """
        Return runtime information.
        """
        return {
            "platform": self.platform_name,
            "version": self.version,
            "environment": self.environment,
            "deployment": self.deployment,
            "ready": self.ready,
        }


runtime = Runtime()