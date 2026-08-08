"""
PlantMind Platform Composition Root

Constructs and wires the core platform dependencies.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.core.availability import CapabilityAvailabilityObserver
from app.core.bootstrap_manager import BootstrapManager
from app.core.capability_policy import (
    MandatoryCapabilityPolicy,
    MandatoryCapabilityPolicyState,
)
from app.core.configuration.configuration_provider import (
    ConfigurationProvider,
)
from app.core.container.service_container import ServiceContainer
from app.core.health import HealthCapability
from app.core.logging.logging_provider import LoggingProvider
from app.core.plugins import PluginRegistration, PluginRegistry
from app.core.plugins.plugin_lifecycle_manager import (
    PluginLifecycleManager,
)
from app.core.runtime import Runtime
from app.core.services.service_registry import ServiceRegistry
from app.services.application_facade import ApplicationFacade
from app.services.integration_gateway import IntegrationGateway
from app.services.orchestration.orchestration_service import (
    OrchestrationService,
)
from app.services.orchestration.workflow_executor import WorkflowExecutor


@dataclass(frozen=True)
class PlatformComposition:
    """Immutable container for core platform dependencies."""

    container: ServiceContainer
    configuration: ConfigurationProvider
    logging: LoggingProvider
    runtime: Runtime
    registry: ServiceRegistry
    plugin_registry: PluginRegistry
    plugin_lifecycle: PluginLifecycleManager
    bootstrap: BootstrapManager
    health: HealthCapability
    availability_observer: CapabilityAvailabilityObserver
    mandatory_capability_policy: MandatoryCapabilityPolicy
    workflow_executor: WorkflowExecutor
    orchestration_service: OrchestrationService
    integration_gateway: IntegrationGateway
    application_facade: ApplicationFacade


class CompositionRoot:
    """Build the PlantMind platform dependency graph."""

    @staticmethod
    def build(
        plugin_registrations: Sequence[PluginRegistration] = (),
    ) -> PlatformComposition:
        container = ServiceContainer()
        configuration = ConfigurationProvider()
        logging = LoggingProvider()
        runtime = Runtime()
        registry = ServiceRegistry()
        plugin_registry = PluginRegistry()

        for registration in plugin_registrations:
            plugin_registry.register(
                registration.name,
                registration.factory,
                metadata=registration.metadata,
            )

        plugin_lifecycle = PluginLifecycleManager(
            plugin_registry
        )

        health = HealthCapability(
            runtime_instance=runtime,
            registry=registry,
        )

        availability_observer = CapabilityAvailabilityObserver(
            sources=(),
        )

        mandatory_capability_policy = MandatoryCapabilityPolicy(
            state=MandatoryCapabilityPolicyState.UNCONFIGURED,
            required_capabilities=(),
        )

        bootstrap = BootstrapManager(
            runtime_instance=runtime,
            registry=registry,
            plugin_registry=plugin_registry,
            plugin_lifecycle=plugin_lifecycle,
            configuration=configuration,
            health=health,
        )

        workflow_executor = WorkflowExecutor()
        orchestration_service = OrchestrationService(
            executor=workflow_executor,
        )
        integration_gateway = IntegrationGateway(
            orchestration_service=orchestration_service,
        )
        application_facade = ApplicationFacade(
            gateway=integration_gateway,
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
            PluginRegistry,
            plugin_registry,
        )
        container.register_instance(
            PluginLifecycleManager,
            plugin_lifecycle,
        )
        container.register_instance(
            BootstrapManager,
            bootstrap,
        )
        container.register_instance(
            HealthCapability,
            health,
        )

        container.register_instance(
            CapabilityAvailabilityObserver,
            availability_observer,
        )

        container.register_instance(
            MandatoryCapabilityPolicy,
            mandatory_capability_policy,
        )
        container.register_instance(
            WorkflowExecutor,
            workflow_executor,
        )
        container.register_instance(
            OrchestrationService,
            orchestration_service,
        )
        container.register_instance(
            IntegrationGateway,
            integration_gateway,
        )
        container.register_instance(
            ApplicationFacade,
            application_facade,
        )

        return PlatformComposition(
            container=container,
            configuration=configuration,
            logging=logging,
            runtime=runtime,
            registry=registry,
            plugin_registry=plugin_registry,
            plugin_lifecycle=plugin_lifecycle,
            bootstrap=bootstrap,
            health=health,
            availability_observer=availability_observer,
            mandatory_capability_policy=mandatory_capability_policy,
            workflow_executor=workflow_executor,
            orchestration_service=orchestration_service,
            integration_gateway=integration_gateway,
            application_facade=application_facade,
        )

def build_platform_composition(
    plugin_registrations: Sequence[PluginRegistration] = (),
) -> PlatformComposition:
    """Backward-compatible platform composition factory."""

    return CompositionRoot.build(
        plugin_registrations=plugin_registrations,
    )
