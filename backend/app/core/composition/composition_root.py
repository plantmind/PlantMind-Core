"""
PlantMind Platform Composition Root

Constructs and wires the core platform dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.bootstrap_manager import BootstrapManager
from app.core.health import HealthCapability
from app.core.runtime import Runtime
from app.core.services.service_registry import ServiceRegistry


@dataclass(frozen=True)
class PlatformComposition:
    """
    Immutable container for core platform dependencies.
    """

    runtime: Runtime
    registry: ServiceRegistry
    bootstrap: BootstrapManager
    health: HealthCapability


def build_platform_composition() -> PlatformComposition:
    """
    Construct the core PlantMind platform dependency graph.
    """

    runtime = Runtime()
    registry = ServiceRegistry()

    bootstrap = BootstrapManager(
        runtime_instance=runtime,
        registry=registry,
    )

    health = HealthCapability(
        runtime_instance=runtime,
        registry=registry,
    )

    return PlatformComposition(
        runtime=runtime,
        registry=registry,
        bootstrap=bootstrap,
        health=health,
    )