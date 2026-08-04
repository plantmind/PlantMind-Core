"""
PlantMind Configuration Provider
"""

from __future__ import annotations

from app.config import Settings, settings


class ConfigurationProvider:
    """
    Central configuration provider.
    """

    def __init__(
        self,
        configuration: Settings | None = None,
    ) -> None:
        self._settings = configuration or settings

    @property
    def settings(self) -> Settings:
        """
        Return the resolved settings.
        """
        return self._settings

    @property
    def environment(self) -> str:
        return self._settings.ENVIRONMENT

    @property
    def deployment(self) -> str:
        return self._settings.DEPLOYMENT_MODE

    def validate(self) -> None:
        """
        Validate mandatory configuration.
        """

        if not self._settings.APP_NAME:
            raise RuntimeError("APP_NAME is required.")

        if not self._settings.VERSION:
            raise RuntimeError("VERSION is required.")

        if not self._settings.ENVIRONMENT:
            raise RuntimeError("ENVIRONMENT is required.")

        if not self._settings.DEPLOYMENT_MODE:
            raise RuntimeError("DEPLOYMENT_MODE is required.")


configuration_provider = ConfigurationProvider()
