"""
PlantMind Bootstrap Manager

BOOT-002 — Bootstrap Lifecycle Architecture
"""

from __future__ import annotations

from app.core.plugins import Plugin, PluginRegistry
from app.core.runtime import Runtime, runtime
from app.core.services.base_service import BaseService
from app.core.services.service_registry import (
    ServiceRegistry,
    service_registry,
)


class BootstrapManager:
    """
    Coordinate platform startup and shutdown.

    Runtime, Service Registry and Plugin Registry
    are injected explicitly.
    """

    def __init__(
        self,
        runtime_instance: Runtime | None = None,
        registry: ServiceRegistry | None = None,
        plugin_registry: PluginRegistry | None = None,
    ) -> None:
        self.runtime = runtime_instance or runtime
        self.registry = registry or service_registry
        self.plugin_registry = plugin_registry or PluginRegistry()
        self._active_plugins: list[Plugin] = []

    def register(self, service: BaseService) -> None:
        """Delegate service registration to the Service Registry."""
        self.registry.register(service)

    def startup(self) -> None:
        """Execute platform startup."""

        for name in self.registry.registered_services():
            service = self.registry.get(name)

            if service is None:
                continue

            if not service.validate():
                raise RuntimeError(
                    f"Service '{service.name}' failed validation."
                )

            service.initialize()

        for name in self.plugin_registry.registered():
            plugin = self.plugin_registry.create(name)
            plugin.activate()
            self._active_plugins.append(plugin)

        self.runtime.mark_ready()

    def shutdown(self) -> None:
        """Execute graceful platform shutdown."""

        for plugin in reversed(self._active_plugins):
            plugin.deactivate()

        self._active_plugins.clear()

        for name in reversed(self.registry.registered_services()):
            service = self.registry.get(name)

            if service is None:
                continue

            service.shutdown()

        self.runtime.mark_not_ready()


bootstrap_manager = BootstrapManager()