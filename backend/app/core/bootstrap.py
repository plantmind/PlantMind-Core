"""
PlantMind Bootstrap Manager

BOOT-002 — Bootstrap Lifecycle Architecture
"""

from __future__ import annotations

from app.config import settings
from app.core.logger import get_logger


class BootstrapManager:
    """
    Coordinates platform startup.

    Responsibilities:

    - Validate configuration
    - Emit startup logs
    - Coordinate platform initialization

    Bootstrap does not own Runtime,
    Service Registry, or Health.
    """

    def __init__(self) -> None:
        self.logger = get_logger("PlantMind.Bootstrap")

    def initialize(self) -> None:
        """
        Execute the bootstrap sequence.
        """

        self._log_startup()

        self._validate_configuration()

        self.logger.info("✓ Configuration Loaded")
        self.logger.info("✓ Bootstrap Initialization Complete")

    def _log_startup(self) -> None:
        """
        Emit platform startup banner.
        """

        self.logger.info("=" * 60)
        self.logger.info(settings.APP_NAME)
        self.logger.info(f"Version      : {settings.VERSION}")
        self.logger.info(
            f"Environment  : {settings.ENVIRONMENT}"
        )
        self.logger.info("=" * 60)

    def _validate_configuration(self) -> None:
        """
        Validate required configuration.
        """

        if not settings.APP_NAME:
            raise RuntimeError("APP_NAME is missing.")

        if not settings.VERSION:
            raise RuntimeError("VERSION is missing.")