"""
PlantMind Platform Composition Root

Constructs and wires the core platform dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.bootstrap_manager import BootstrapManager
from app.core.configuration.configuration_provider import (
    ConfigurationProvider,
)
from app.core.container.service_container import ServiceContainer
from app.core.health import HealthCapability
from app.core.logging.logging_provider import LoggingProvider
from app.core.runtime import Runtime
from app.core.services.service_registry import ServiceRegistry


@dataclass(frozen=True)
class PlatformComposition:
    """Immutable container for core platform dependencies."""

    container: ServiceContainer
    configuration: ConfigurationProvider
    logging: LoggingProvider
    runtime: Runtime
    registry: ServiceRegistry
    bootstrap: BootstrapManager
    health: HealthCapability


class CompositionRoot:
    """Build the PlantMind platform dependency graph."""

    @staticmethod
    def build() -> PlatformComposition:
        container = ServiceContainer()
        configuration = ConfigurationProvider()
        logging = LoggingProvider()
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

        container.register_instance(
            ConfigurationProvider,
            configuration,
        )
        container.register_instance(
            LoggingProvider,
            logging,
        )
        container.register_instance(
            Runtime,
            runtime,
        )
        container.register_instance(
            ServiceRegistry,
            registry,
        )
        container.register_instance(
            BootstrapManager,
            bootstrap,
        )
        container.register_instance(
            HealthCapability,
            health,
        )

        return PlatformComposition(
            container=container,
            configuration=configuration,
            logging=logging,
            runtime=runtime,
            registry=registry,
            bootstrap=bootstrap,
            health=health,
        )


def build_platform_composition() -> PlatformComposition:
    """Backward-compatible platform composition factory."""

    return CompositionRoot.build()
