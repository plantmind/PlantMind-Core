from dataclasses import FrozenInstanceError

import pytest

from app.core.registry.errors import DuplicateRegistrationError

from app.core.composition import CompositionRoot

from app.core.plugins import (
    Plugin,
    PluginIdentityMismatchError,
    PluginLifecycleManager,
    PluginMetadata,
    PluginRegistration,
    PluginRegistry,
)


def test_plugin_metadata_is_immutable() -> None:
    metadata = PluginMetadata(
        plugin_version="2.0.0",
    )

    with pytest.raises(FrozenInstanceError):
        metadata.plugin_version = "3.0.0"


def test_plugin_metadata_declares_immutable_contract_version() -> None:
    metadata = PluginMetadata(
        plugin_version="2.0.0",
    )

    assert metadata.contract_version == "1.0"

    with pytest.raises(FrozenInstanceError):
        metadata.contract_version = "2.0"


def test_plugin_registration_remains_backward_compatible_without_metadata() -> None:
    factory = lambda: object()

    registration = PluginRegistration(
        name="alpha",
        factory=factory,
    )

    assert registration.name == "alpha"
    assert registration.factory is factory


def test_plugin_registration_can_carry_metadata() -> None:
    metadata = PluginMetadata(
        plugin_version="2.0.0",
    )

    registration = PluginRegistration(
        name="alpha",
        factory=lambda: object(),
        metadata=metadata,
    )

    assert registration.metadata is metadata


def test_plugin_registry_exposes_metadata_without_creating_plugin() -> None:
    creation_count = 0

    def factory():
        nonlocal creation_count
        creation_count += 1
        raise AssertionError("Plugin factory must remain lazy.")

    metadata = PluginMetadata(
        plugin_version="2.0.0",
    )
    registry = PluginRegistry()

    registry.register(
        "alpha",
        factory,
        metadata=metadata,
    )

    assert registry.metadata("alpha") is metadata
    assert creation_count == 0


def test_composition_forwards_plugin_metadata_without_instantiation() -> None:
    creation_count = 0

    def factory():
        nonlocal creation_count
        creation_count += 1
        raise AssertionError("Composition must not instantiate plugins.")

    metadata = PluginMetadata(
        plugin_version="2.0.0",
    )

    composition = CompositionRoot.build(
        plugin_registrations=(
            PluginRegistration(
                name="alpha",
                factory=factory,
                metadata=metadata,
            ),
        ),
    )

    assert composition.plugin_registry.metadata("alpha") is metadata
    assert creation_count == 0


def test_plugin_registry_clear_removes_associated_metadata() -> None:
    metadata = PluginMetadata(
        plugin_version="2.0.0",
    )
    registry = PluginRegistry()

    registry.register(
        "alpha",
        lambda: object(),
        metadata=metadata,
    )

    registry.clear()

    assert registry.metadata("alpha") is None
    assert registry.registered() == ()


def test_duplicate_registration_does_not_corrupt_plugin_metadata() -> None:
    original_metadata = PluginMetadata(
        plugin_version="2.0.0",
    )
    replacement_metadata = PluginMetadata(
        plugin_version="3.0.0",
    )
    registry = PluginRegistry()

    registry.register(
        "alpha",
        lambda: object(),
        metadata=original_metadata,
    )

    with pytest.raises(DuplicateRegistrationError):
        registry.register(
            "alpha",
            lambda: object(),
            metadata=replacement_metadata,
        )

    assert registry.metadata("alpha") is original_metadata


def test_plugin_metadata_preserves_identity_validation_before_activation() -> None:
    events: list[str] = []

    class RecordingPlugin(Plugin):
        @property
        def name(self) -> str:
            return "beta"

        def activate(self) -> None:
            events.append("activated")

        def deactivate(self) -> None:
            pass

    metadata = PluginMetadata(
        plugin_version="2.0.0",
    )
    registry = PluginRegistry()
    registry.register(
        "alpha",
        RecordingPlugin,
        metadata=metadata,
    )
    manager = PluginLifecycleManager(registry)

    with pytest.raises(PluginIdentityMismatchError):
        manager.activate_all()

    assert events == []
    assert manager.active_plugin_names() == ()
    assert registry.metadata("alpha") is metadata


def test_plugin_version_is_explicit_and_independent_from_app_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.core.constants.APP_VERSION",
        "999.0.0",
    )

    metadata = PluginMetadata(
        plugin_version="2.0.0",
    )

    assert metadata.plugin_version == "2.0.0"

    with pytest.raises(TypeError):
        PluginMetadata()
