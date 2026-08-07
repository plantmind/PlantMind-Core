from dataclasses import FrozenInstanceError

import pytest

from app.core.composition import CompositionRoot, build_platform_composition
from app.core.plugins import Plugin, PluginRegistration, PluginRegistry
from app.core.registry.errors import DuplicateRegistrationError


class NoOpPlugin(Plugin):
    @property
    def name(self) -> str:
        return "noop"

    def activate(self) -> None:
        pass

    def deactivate(self) -> None:
        pass


def test_plugin_registration_is_immutable() -> None:
    registration = PluginRegistration(
        name="alpha",
        factory=NoOpPlugin,
    )

    with pytest.raises(FrozenInstanceError):
        registration.name = "changed"

def test_composition_registers_explicit_plugins() -> None:
    registration = PluginRegistration(
        name="alpha",
        factory=NoOpPlugin,
    )

    platform = CompositionRoot.build(
        plugin_registrations=(registration,),
    )

    assert platform.plugin_registry.registered() == ("alpha",)


def test_composition_factory_forwards_explicit_registrations() -> None:
    registration = PluginRegistration(
        name="alpha",
        factory=NoOpPlugin,
    )

    platform = build_platform_composition(
        plugin_registrations=(registration,),
    )

    assert platform.plugin_registry.registered() == ("alpha",)


def test_composition_does_not_eagerly_create_plugins() -> None:
    created: list[str] = []

    def factory() -> Plugin:
        created.append("created")
        return NoOpPlugin()

    registration = PluginRegistration(
        name="alpha",
        factory=factory,
    )

    platform = CompositionRoot.build(
        plugin_registrations=(registration,),
    )

    assert platform.plugin_registry.registered() == ("alpha",)
    assert created == []


def test_registration_order_uses_existing_registry_semantics() -> None:
    platform = CompositionRoot.build(
        plugin_registrations=(
            PluginRegistration(name="beta", factory=NoOpPlugin),
            PluginRegistration(name="alpha", factory=NoOpPlugin),
        ),
    )

    assert platform.plugin_registry.registered() == (
        "alpha",
        "beta",
    )


def test_duplicate_registration_preserves_registry_error() -> None:
    registration = PluginRegistration(
        name="alpha",
        factory=NoOpPlugin,
    )

    with pytest.raises(DuplicateRegistrationError):
        CompositionRoot.build(
            plugin_registrations=(
                registration,
                registration,
            ),
        )


def test_container_resolves_registry_with_supplied_registrations() -> None:
    registration = PluginRegistration(
        name="alpha",
        factory=NoOpPlugin,
    )

    platform = CompositionRoot.build(
        plugin_registrations=(registration,),
    )

    resolved = platform.container.resolve(PluginRegistry)

    assert resolved is platform.plugin_registry
    assert resolved.registered() == ("alpha",)


def test_bootstrap_activates_plugin_from_composition_boundary() -> None:
    events: list[str] = []

    class RecordingPlugin(Plugin):
        @property
        def name(self) -> str:
            return "alpha"

        def activate(self) -> None:
            events.append("activate:alpha")

        def deactivate(self) -> None:
            events.append("deactivate:alpha")

    platform = CompositionRoot.build(
        plugin_registrations=(
            PluginRegistration(
                name="alpha",
                factory=RecordingPlugin,
            ),
        ),
    )

    assert events == []

    platform.bootstrap.startup()

    assert events == ["activate:alpha"]
    assert platform.plugin_lifecycle.active_plugin_names() == (
        "alpha",
    )

    platform.bootstrap.shutdown()

    assert events == [
        "activate:alpha",
        "deactivate:alpha",
    ]


def test_composition_without_registrations_remains_supported() -> None:
    platform = CompositionRoot.build()

    assert platform.plugin_registry.registered() == ()


def test_backward_compatible_factory_without_registrations() -> None:
    platform = build_platform_composition()

    assert platform.plugin_registry.registered() == ()
