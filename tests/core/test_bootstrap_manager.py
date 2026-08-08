from app.core.bootstrap_manager import BootstrapManager
from app.core.plugins import Plugin, PluginRegistry
from app.core.runtime import Runtime
from app.core.services.base_service import BaseService
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


class RecordingRuntime(Runtime):
    def __init__(self, events: list[str]) -> None:
        super().__init__()
        self._events = events

    def mark_stopping(self) -> None:
        self._events.append("runtime:stopping")
        super().mark_stopping()

    def mark_not_ready(self) -> None:
        super().mark_not_ready()
        self._events.append("runtime:stopped")


class RecordingService(BaseService):
    def __init__(self, name: str, events: list[str]) -> None:
        super().__init__(name)
        self._events = events

    def validate(self) -> bool:
        return True

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._events.append(f"shutdown:{self.name}")


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

def test_shutdown_transitions_runtime_around_component_shutdown() -> None:
    events: list[str] = []
    plugins = PluginRegistry()
    registry = ServiceRegistry()

    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )
    registry.register(RecordingService("service-a", events))

    runtime = RecordingRuntime(events)
    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=registry,
        plugin_registry=plugins,
    )

    manager.startup()
    events.clear()

    manager.shutdown()

    assert events == [
        "runtime:stopping",
        "deactivate:plugin-a",
        "shutdown:service-a",
        "runtime:stopped",
    ]

def test_shutdown_services_follow_reverse_registry_enumeration_order() -> None:
    events: list[str] = []
    registry = ServiceRegistry()

    registry.register(RecordingService("service-z", events))
    registry.register(RecordingService("service-a", events))

    manager = BootstrapManager(
        runtime_instance=Runtime(),
        registry=registry,
        plugin_registry=PluginRegistry(),
    )

    manager.startup()
    manager.shutdown()

    assert events == [
        "shutdown:service-z",
        "shutdown:service-a",
    ]


class AdmissionRecordingRuntime(Runtime):
    def __init__(self, events: list[str]) -> None:
        super().__init__()
        self._admission_events = events

    def mark_ready(self) -> None:
        self._admission_events.append("runtime:ready")
        super().mark_ready()

    def enable_request_admission(self) -> None:
        self._admission_events.append("admission:enabled")
        super().enable_request_admission()

    def disable_request_admission(self) -> None:
        self._admission_events.append("admission:disabled")
        super().disable_request_admission()

    def mark_stopping(self) -> None:
        self._admission_events.append("runtime:stopping")
        super().mark_stopping()


def test_startup_enables_request_admission_after_ready() -> None:
    events: list[str] = []
    runtime = AdmissionRecordingRuntime(events)

    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=ServiceRegistry(),
        plugin_registry=PluginRegistry(),
    )

    manager.startup()

    assert events == [
        "runtime:ready",
        "admission:enabled",
    ]
    assert runtime.is_ready is True
    assert runtime.is_request_admission_enabled is True


def test_shutdown_disables_request_admission_before_stopping() -> None:
    events: list[str] = []
    runtime = AdmissionRecordingRuntime(events)

    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=ServiceRegistry(),
        plugin_registry=PluginRegistry(),
    )

    manager.startup()
    events.clear()

    manager.shutdown()

    assert events[:2] == [
        "admission:disabled",
        "runtime:stopping",
    ]
    assert runtime.is_request_admission_enabled is False
