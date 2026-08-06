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