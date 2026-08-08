import pytest

from app.core.plugins import Plugin, PluginRegistry
from app.core.plugins.plugin_lifecycle_manager import (
    PluginLifecycleManager,
)


class RecordingPlugin(Plugin):
    def __init__(
        self,
        plugin_name: str,
        events: list[str],
    ) -> None:
        self._name = plugin_name
        self._events = events

    @property
    def name(self) -> str:
        return self._name

    def activate(self) -> None:
        self._events.append(f"activate:{self.name}")

    def deactivate(self) -> None:
        self._events.append(f"deactivate:{self.name}")


class FailingDeactivationPlugin(RecordingPlugin):
    def __init__(
        self,
        plugin_name: str,
        events: list[str],
        error: Exception,
    ) -> None:
        super().__init__(plugin_name, events)
        self._error = error

    def deactivate(self) -> None:
        self._events.append(f"deactivate:{self.name}")
        raise self._error


def test_activate_all_creates_and_activates_plugins() -> None:
    events: list[str] = []
    registry = PluginRegistry()

    registry.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )

    manager = PluginLifecycleManager(registry)
    manager.activate_all()

    assert events == ["activate:plugin-a"]
    assert manager.active_plugin_names() == ("plugin-a",)


def test_deactivate_all_uses_reverse_activation_order() -> None:
    events: list[str] = []
    registry = PluginRegistry()

    registry.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )
    registry.register(
        "plugin-b",
        lambda: RecordingPlugin("plugin-b", events),
    )

    manager = PluginLifecycleManager(registry)
    manager.activate_all()
    manager.deactivate_all()

    assert events == [
        "activate:plugin-a",
        "activate:plugin-b",
        "deactivate:plugin-b",
        "deactivate:plugin-a",
    ]
    assert manager.active_plugin_names() == ()


def test_activate_all_does_not_duplicate_active_plugins() -> None:
    events: list[str] = []
    registry = PluginRegistry()

    registry.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )

    manager = PluginLifecycleManager(registry)
    manager.activate_all()
    manager.activate_all()

    assert events == ["activate:plugin-a"]
    assert manager.active_plugin_names() == ("plugin-a",)

def test_deactivate_all_continues_after_plugin_failure() -> None:
    events: list[str] = []
    registry = PluginRegistry()
    error = RuntimeError("plugin-b deactivation failed")

    registry.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )
    registry.register(
        "plugin-b",
        lambda: FailingDeactivationPlugin(
            "plugin-b",
            events,
            error,
        ),
    )
    registry.register(
        "plugin-c",
        lambda: RecordingPlugin("plugin-c", events),
    )

    manager = PluginLifecycleManager(registry)
    manager.activate_all()
    events.clear()

    with pytest.raises(RuntimeError):
        manager.deactivate_all()

    assert events == [
        "deactivate:plugin-c",
        "deactivate:plugin-b",
        "deactivate:plugin-a",
    ]


def test_deactivate_all_retains_only_plugins_that_failed_deactivation() -> None:
    events: list[str] = []
    registry = PluginRegistry()
    error = RuntimeError("plugin-b deactivation failed")

    registry.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )
    registry.register(
        "plugin-b",
        lambda: FailingDeactivationPlugin(
            "plugin-b",
            events,
            error,
        ),
    )
    registry.register(
        "plugin-c",
        lambda: RecordingPlugin("plugin-c", events),
    )

    manager = PluginLifecycleManager(registry)
    manager.activate_all()

    with pytest.raises(RuntimeError):
        manager.deactivate_all()

    assert manager.active_plugin_names() == ("plugin-b",)


def test_deactivate_all_preserves_single_original_exception() -> None:
    events: list[str] = []
    registry = PluginRegistry()
    original_error = RuntimeError("plugin-a deactivation failed")

    registry.register(
        "plugin-a",
        lambda: FailingDeactivationPlugin(
            "plugin-a",
            events,
            original_error,
        ),
    )

    manager = PluginLifecycleManager(registry)
    manager.activate_all()

    with pytest.raises(RuntimeError) as exc_info:
        manager.deactivate_all()

    assert exc_info.value is original_error


def test_deactivate_all_aggregates_multiple_failures_in_encounter_order() -> None:
    events: list[str] = []
    registry = PluginRegistry()
    error_b = RuntimeError("plugin-b deactivation failed")
    error_c = ValueError("plugin-c deactivation failed")

    registry.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )
    registry.register(
        "plugin-b",
        lambda: FailingDeactivationPlugin(
            "plugin-b",
            events,
            error_b,
        ),
    )
    registry.register(
        "plugin-c",
        lambda: FailingDeactivationPlugin(
            "plugin-c",
            events,
            error_c,
        ),
    )

    manager = PluginLifecycleManager(registry)
    manager.activate_all()
    events.clear()

    with pytest.raises(ExceptionGroup) as exc_info:
        manager.deactivate_all()

    assert events == [
        "deactivate:plugin-c",
        "deactivate:plugin-b",
        "deactivate:plugin-a",
    ]
    assert exc_info.value.exceptions == (
        error_c,
        error_b,
    )
    assert manager.active_plugin_names() == (
        "plugin-b",
        "plugin-c",
    )
