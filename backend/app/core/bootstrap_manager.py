"""
PlantMind Bootstrap Manager

BOOT-002 — Bootstrap Lifecycle Architecture
"""

from __future__ import annotations

from app.core.plugins import PluginRegistry
from app.core.plugins.plugin_lifecycle_manager import (
    PluginLifecycleManager,
)
from app.core.runtime import Runtime, runtime
from app.core.services.base_service import BaseService
from app.core.services.service_registry import (
    ServiceRegistry,
    service_registry,
)


class BootstrapManager:
    """
    Coordinate platform startup and shutdown.

    Runtime, Service Registry and Plugin Lifecycle Manager
    are injected explicitly.
    """

    def __init__(
        self,
        runtime_instance: Runtime | None = None,
        registry: ServiceRegistry | None = None,
        plugin_registry: PluginRegistry | None = None,
        plugin_lifecycle: PluginLifecycleManager | None = None,
    ) -> None:
        self.runtime = runtime_instance or runtime
        self.registry = registry or service_registry

        resolved_plugin_registry = (
            plugin_registry or PluginRegistry()
        )

        self.plugin_lifecycle = (
            plugin_lifecycle
            or PluginLifecycleManager(
                resolved_plugin_registry
            )
        )

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
                self.runtime.mark_failed()
                raise RuntimeError(
                    f"Service '{service.name}' failed validation."
                )

        initialized_services: list[BaseService] = []

        try:
            for name in self.registry.registered_services():
                service = self.registry.get(name)

                if service is None:
                    continue

                service.initialize()
                initialized_services.append(service)
        except Exception:
            for service in reversed(initialized_services):
                service.shutdown()

            self.runtime.mark_failed()
            raise

        try:
            self.plugin_lifecycle.activate_all()
        except Exception:
            self.plugin_lifecycle.deactivate_all()

            for service in reversed(initialized_services):
                service.shutdown()

            self.runtime.mark_failed()
            raise

        self.runtime.mark_ready()

    def shutdown(self) -> None:
        """Execute graceful platform shutdown."""

        self.runtime.mark_stopping()

        failures: list[Exception] = []

        try:
            self.plugin_lifecycle.deactivate_all()
        except ExceptionGroup as exc:
            failures.extend(exc.exceptions)
        except Exception as exc:
            failures.append(exc)

        for name in reversed(
            self.registry.registered_services()
        ):
            service = self.registry.get(name)

            if service is None:
                continue

            try:
                service.shutdown()
            except ExceptionGroup as exc:
                failures.extend(exc.exceptions)
            except Exception as exc:
                failures.append(exc)

        if failures:
            self.runtime.mark_failed()

            if len(failures) == 1:
                raise failures[0]

            raise ExceptionGroup(
                "Managed shutdown failures",
                failures,
            )

        self.runtime.mark_not_ready()


bootstrap_manager = BootstrapManager()