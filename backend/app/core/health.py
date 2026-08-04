"""
PlantMind Health Capability

Provides a unified view of the operational health
of the PlantMind platform.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.runtime import Runtime, runtime
from app.core.services.service_registry import (
    ServiceRegistry,
    service_registry,
)


@dataclass(frozen=True)
class HealthStatus:
    """
    Immutable snapshot of platform health.
    """

    platform_name: str
    version: str
    environment: str
    runtime_ready: bool
    registered_services: int
    services: list[str]


class HealthCapability:
    """
    Read-only health capability.
    """

    def __init__(
        self,
        runtime_instance: Runtime | None = None,
        registry: ServiceRegistry | None = None,
    ) -> None:
        self.runtime = runtime_instance or runtime
        self.registry = registry or service_registry

    def get_status(self) -> HealthStatus:
        """
        Return current platform health.
        """

        return HealthStatus(
            platform_name=self.runtime.platform_name,
            version=self.runtime.version,
            environment=self.runtime.environment,
            runtime_ready=self.runtime.is_ready,
            registered_services=self.registry.count,
            services=self.registry.registered_services(),
        )


health = HealthCapability()