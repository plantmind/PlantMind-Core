from app.core.bootstrap_manager import BootstrapManager
from app.core.composition import CompositionRoot
from app.core.plugins import PluginRegistry
from app.core.plugins.plugin_lifecycle_manager import (
    PluginLifecycleManager,
)


def test_composition_exposes_plugin_infrastructure() -> None:
    platform = CompositionRoot.build()

    assert isinstance(
        platform.plugin_registry,
        PluginRegistry,
    )
    assert isinstance(
        platform.plugin_lifecycle,
        PluginLifecycleManager,
    )


def test_container_resolves_composed_plugin_instances() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.container.resolve(PluginRegistry)
        is platform.plugin_registry
    )
    assert (
        platform.container.resolve(PluginLifecycleManager)
        is platform.plugin_lifecycle
    )


def test_bootstrap_uses_composed_plugin_lifecycle() -> None:
    platform = CompositionRoot.build()

    bootstrap = platform.container.resolve(BootstrapManager)

    assert (
        bootstrap.plugin_lifecycle
        is platform.plugin_lifecycle
    )


def test_bootstrap_uses_composed_configuration() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.bootstrap.configuration
        is platform.configuration
    )


def test_bootstrap_uses_composed_health_capability() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.bootstrap.health
        is platform.health
    )
