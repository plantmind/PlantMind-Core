from app.core.bootstrap_manager import BootstrapManager
from app.core.plugins import Plugin, PluginRegistry
from app.core.runtime import Runtime
from app.core.services.service_registry import ServiceRegistry


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


def build_manager(
    plugin_registry: PluginRegistry,
) -> BootstrapManager:
    return BootstrapManager(
        runtime_instance=Runtime(),
        registry=ServiceRegistry(),
        plugin_registry=plugin_registry,
    )


def test_startup_activates_registered_plugins() -> None:
    events: list[str] = []
    plugins = PluginRegistry()

    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )

    manager = build_manager(plugins)
    manager.startup()

    assert events == ["activate:plugin-a"]
    assert manager.runtime.is_ready is True


def test_shutdown_deactivates_active_plugins() -> None:
    events: list[str] = []
    plugins = PluginRegistry()

    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )

    manager = build_manager(plugins)
    manager.startup()
    manager.shutdown()

    assert events == [
        "activate:plugin-a",
        "deactivate:plugin-a",
    ]
    assert manager.runtime.is_ready is False


def test_shutdown_deactivates_plugins_in_reverse_order() -> None:
    events: list[str] = []
    plugins = PluginRegistry()

    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )
    plugins.register(
        "plugin-b",
        lambda: RecordingPlugin("plugin-b", events),
    )

    manager = build_manager(plugins)
    manager.startup()
    manager.shutdown()

    assert events == [
        "activate:plugin-a",
        "activate:plugin-b",
        "deactivate:plugin-b",
        "deactivate:plugin-a",
    ]