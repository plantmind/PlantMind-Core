"""
PlantMind Bootstrap Manager

BOOT-001 — Platform Bootstrap Lifecycle
"""

from app.config import settings
from app.core.logger import get_logger


class BootstrapManager:
    """
    Responsible for platform startup initialization.

    Current Responsibilities:
    - Configuration validation
    - Startup logging
    - Platform startup lifecycle

    Future Responsibilities:
    - Dependency Injection
    - Service Registration
    - Connector Registration
    - Engine Registration
    - Agent Registration
    - Security Initialization
    - Health Verification
    """

    def __init__(self):
        self.logger = get_logger("PlantMind.Bootstrap")

    def initialize(self):
        self.logger.info("=" * 60)
        self.logger.info("PlantMind Enterprise Platform")
        self.logger.info(f"Version      : {settings.VERSION}")
        self.logger.info("Environment  : Development")
        self.logger.info("=" * 60)

        self._validate_configuration()

        self.logger.info("✓ Configuration Loaded")
        self.logger.info("✓ Bootstrap Initialization Complete")
        self.logger.info("Platform Status : READY")
        self.logger.info("=" * 60)

    def _validate_configuration(self):
        """
        Basic configuration validation.

        Additional validation rules will be added
        in future milestones.
        """

        if not settings.APP_NAME:
            raise RuntimeError("APP_NAME is missing.")

        if not settings.VERSION:
            raise RuntimeError("VERSION is missing.")