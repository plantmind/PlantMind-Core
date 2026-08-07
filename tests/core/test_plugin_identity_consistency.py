import pytest

from app.core.composition import CompositionRoot
from app.core.registry.errors import (
    DuplicateRegistrationError,
    RegistrationNotFoundError,
)
from app.core.plugins import (
    Plugin,
    PluginIdentityMismatchError,
    PluginLifecycleManager,
    PluginRegistration,
    PluginRegistry,
)


class NamedPlugin(Plugin):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def activate(self) -> None:
        pass

    def deactivate(self) -> None:
        pass


def test_create_rejects_plugin_identity_mismatch() -> None:
    registry = PluginRegistry()
    registry.register(
        "alpha",
        lambda: NamedPlugin("beta"),
    )

    with pytest.raises(PluginIdentityMismatchError):
        registry.create("alpha")


def test_create_accepts_matching_plugin_identity() -> None:
    registry = PluginRegistry()
    registry.register(
        "alpha",
        lambda: NamedPlugin("alpha"),
    )

    plugin = registry.create("alpha")

    assert isinstance(plugin, NamedPlugin)
    assert plugin.name == "alpha"


def test_identity_validation_is_lazy_until_plugin_creation() -> None:
    created: list[str] = []

    def factory() -> Plugin:
        created.append("created")
        return NamedPlugin("beta")

    registry = PluginRegistry()
    registry.register("alpha", factory)

    assert created == []

    with pytest.raises(PluginIdentityMismatchError):
        registry.create("alpha")

    assert created == ["created"]


def test_identity_mismatch_is_rejected_before_activation() -> None:
    events: list[str] = []

    class RecordingPlugin(NamedPlugin):
        def activate(self) -> None:
            events.append("activated")

    registry = PluginRegistry()
    registry.register(
        "alpha",
        lambda: RecordingPlugin("beta"),
    )

    manager = PluginLifecycleManager(registry)

    with pytest.raises(PluginIdentityMismatchError):
        manager.activate_all()

    assert events == []
    assert manager.active_plugin_names() == ()


def test_matching_plugin_preserves_lifecycle_behavior() -> None:
    events: list[str] = []

    class RecordingPlugin(NamedPlugin):
        def activate(self) -> None:
            events.append("activate:alpha")

        def deactivate(self) -> None:
            events.append("deactivate:alpha")

    registry = PluginRegistry()
    registry.register(
        "alpha",
        lambda: RecordingPlugin("alpha"),
    )

    manager = PluginLifecycleManager(registry)
    manager.activate_all()

    assert events == ["activate:alpha"]
    assert manager.active_plugin_names() == ("alpha",)

    manager.deactivate_all()

    assert events == [
        "activate:alpha",
        "deactivate:alpha",
    ]
    assert manager.active_plugin_names() == ()


def test_composed_mismatched_plugin_is_rejected_before_activation() -> None:
    events: list[str] = []

    class RecordingPlugin(NamedPlugin):
        def activate(self) -> None:
            events.append("activated")

    platform = CompositionRoot.build(
        plugin_registrations=(
            PluginRegistration(
                name="alpha",
                factory=lambda: RecordingPlugin("beta"),
            ),
        ),
    )

    assert events == []

    with pytest.raises(PluginIdentityMismatchError):
        platform.bootstrap.startup()

    assert events == []
    assert platform.plugin_lifecycle.active_plugin_names() == ()


def test_duplicate_registration_behavior_remains_unchanged() -> None:
    registry = PluginRegistry()
    registry.register(
        "alpha",
        lambda: NamedPlugin("alpha"),
    )

    with pytest.raises(DuplicateRegistrationError):
        registry.register(
            "alpha",
            lambda: NamedPlugin("alpha"),
        )


def test_registration_not_found_behavior_remains_unchanged() -> None:
    registry = PluginRegistry()

    with pytest.raises(RegistrationNotFoundError):
        registry.create("unknown")


def test_identity_mismatch_error_message_is_deterministic() -> None:
    registry = PluginRegistry()
    registry.register(
        "alpha",
        lambda: NamedPlugin("beta"),
    )

    with pytest.raises(PluginIdentityMismatchError) as exc_info:
        registry.create("alpha")

    assert str(exc_info.value) == (
        "Plugin identity mismatch: registered as 'alpha' "
        "but instance reports 'beta'."
    )


def test_composition_does_not_instantiate_plugin_for_identity_validation() -> None:
    created: list[str] = []

    def factory() -> Plugin:
        created.append("created")
        return NamedPlugin("alpha")

    platform = CompositionRoot.build(
        plugin_registrations=(
            PluginRegistration(
                name="alpha",
                factory=factory,
            ),
        ),
    )

    assert platform.plugin_registry.registered() == ("alpha",)
    assert created == []
