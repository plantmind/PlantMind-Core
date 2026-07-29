"""
PlantMind Bootstrap Manager

Coordinates the complete startup and shutdown lifecycle
of the PlantMind platform.
"""

from __future__ import annotations

from app.core.runtime import runtime
from app.core.services.service_registry import ServiceRegistry
from app.core.services.base_service import BaseService


class BootstrapManager:
    """
    Coordinates platform startup and shutdown.
    """

    def __init__(self) -> None:
        self.runtime = runtime
        self.registry = ServiceRegistry()

    def register(self, service: BaseService) -> None:
        """
        Register a platform service.
        """

        self.registry.register(service)

    def startup(self) -> None:
        """
        Start the PlantMind platform.
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
        Gracefully shutdown the PlantMind platform.
        """

        for name in reversed(self.registry.registered_services()):
            service = self.registry.get(name)

            if service is None:
                continue

            service.shutdown()

        self.runtime.mark_not_ready()


bootstrap_manager = BootstrapManager()