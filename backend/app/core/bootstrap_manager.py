"""
PlantMind Bootstrap Manager

BOOT-002 — Bootstrap Lifecycle Architecture
"""

from __future__ import annotations

from app.core.runtime import runtime
from app.core.services.base_service import BaseService
from app.core.services.service_registry import service_registry


class BootstrapManager:
    """
    Coordinates the complete startup and shutdown lifecycle
    of the PlantMind platform.
    """

    def __init__(self) -> None:
        self.runtime = runtime
        self.registry = service_registry

    def register(self, service: BaseService) -> None:
        """
        Register a platform service.
        """
        self.registry.register(service)

    def startup(self) -> None:
        """
        Execute platform startup.
        """

        for name in self.registry.registered_services():
            service = self.registry.get(name)

            if service is None:
                continue

            if not service.validate():
                raise RuntimeError(
                    f"Service '{service.name}' failed validation."
                )

            service.initialize()

        self.runtime.mark_ready()

    def shutdown(self) -> None:
        """
        Execute graceful platform shutdown.
        """

        for name in reversed(self.registry.registered_services()):
            service = self.registry.get(name)

            if service is None:
                continue

            service.shutdown()

        self.runtime.mark_not_ready()


bootstrap_manager = BootstrapManager()