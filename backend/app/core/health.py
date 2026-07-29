"""
PlantMind Health Capability

Provides a unified view of the operational health of the platform.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.core.runtime import runtime
from app.core.services.service_registry import service_registry


@dataclass(frozen=True)
class HealthStatus:
    """
    Immutable snapshot of the current platform health.
    """

    platform_name: str
    version: str
    environment: str
    runtime_ready: bool
    registered_services: int
    services: List[str]


class HealthCapability:
    """
    Provides health information for the PlantMind platform.
    """

    def get_status(self) -> HealthStatus:
        """
        Return the current platform health snapshot.
        """

        return HealthStatus(
            platform_name=runtime.platform_name,
            version=runtime.version,
            environment=runtime.environment,
            runtime_ready=runtime.is_ready,
            registered_services=service_registry.count,
            services=service_registry.registered_services(),
        )


health = HealthCapability()