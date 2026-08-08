import pytest

from app.core.bootstrap_manager import BootstrapManager
from app.core.plugins import Plugin, PluginRegistry
from app.core.runtime import Runtime
from app.core.runtime_state import RuntimeState
from app.core.services.base_service import BaseService
from app.core.services.service_registry import ServiceRegistry


class RecordingService(BaseService):
    def __init__(
        self,
        name: str,
        events: list[str],
        valid: bool = True,
    ) -> None:
        super().__init__(name)
        self._events = events
        self._valid = valid

    def validate(self) -> bool:
        self._events.append(f"validate:{self.name}")
        return self._valid

    def initialize(self) -> None:
        self._events.append(f"initialize:{self.name}")

    def shutdown(self) -> None:
        self._events.append(f"shutdown:{self.name}")


def test_service_validation_failure_prevents_all_initialization() -> None:
    events: list[str] = []
    registry = ServiceRegistry()
    registry.register(RecordingService("service-a", events))
    registry.register(RecordingService("service-b", events, valid=False))

    manager = BootstrapManager(
        runtime_instance=Runtime(),
        registry=registry,
        plugin_registry=PluginRegistry(),
    )

    with pytest.raises(RuntimeError, match="Service .* failed validation"):
        manager.startup()

    assert events == [
        "validate:service-a",
        "validate:service-b",
    ]

class RecordingPlugin(Plugin):
    def __init__(self, name: str, events: list[str]) -> None:
        self._name = name
        self._events = events

    @property
    def name(self) -> str:
        return self._name

    def activate(self) -> None:
        self._events.append(f"activate:{self.name}")

    def deactivate(self) -> None:
        self._events.append(f"deactivate:{self.name}")


def test_service_validation_failure_prevents_plugin_activation() -> None:
    service_events: list[str] = []
    plugin_events: list[str] = []
    registry = ServiceRegistry()
    plugins = PluginRegistry()

    registry.register(
        RecordingService("service-a", service_events, valid=False),
    )
    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", plugin_events),
    )

    manager = BootstrapManager(
        runtime_instance=Runtime(),
        registry=registry,
        plugin_registry=plugins,
    )

    with pytest.raises(RuntimeError, match="Service .* failed validation"):
        manager.startup()

    assert plugin_events == []

class FailingInitializeService(RecordingService):
    def initialize(self) -> None:
        self._events.append(f"initialize:{self.name}")
        raise RuntimeError(f"Service {self.name} initialization failed.")


def test_service_initialization_failure_stops_subsequent_initialization() -> None:
    events: list[str] = []
    registry = ServiceRegistry()

    registry.register(RecordingService("service-a", events))
    registry.register(FailingInitializeService("service-b", events))
    registry.register(RecordingService("service-c", events))

    manager = BootstrapManager(
        runtime_instance=Runtime(),
        registry=registry,
        plugin_registry=PluginRegistry(),
    )

    with pytest.raises(RuntimeError, match="Service service-b initialization failed"):
        manager.startup()

    assert events == [
        "validate:service-a",
        "validate:service-b",
        "validate:service-c",
        "initialize:service-a",
        "initialize:service-b",
        "shutdown:service-a",
    ]

def test_initialized_services_roll_back_in_reverse_order_after_failure() -> None:
    events: list[str] = []
    registry = ServiceRegistry()

    registry.register(RecordingService("service-a", events))
    registry.register(RecordingService("service-b", events))
    registry.register(FailingInitializeService("service-c", events))

    manager = BootstrapManager(
        runtime_instance=Runtime(),
        registry=registry,
        plugin_registry=PluginRegistry(),
    )

    with pytest.raises(RuntimeError, match="Service service-c initialization failed"):
        manager.startup()

    assert events == [
        "validate:service-a",
        "validate:service-b",
        "validate:service-c",
        "initialize:service-a",
        "initialize:service-b",
        "initialize:service-c",
        "shutdown:service-b",
        "shutdown:service-a",
    ]

class FailingActivationPlugin(RecordingPlugin):
    def activate(self) -> None:
        self._events.append(f"activate:{self.name}")
        raise RuntimeError(f"Plugin {self.name} activation failed.")


def test_plugin_activation_failure_rolls_back_active_plugins_in_reverse_order() -> None:
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
    plugins.register(
        "plugin-c",
        lambda: FailingActivationPlugin("plugin-c", events),
    )

    manager = BootstrapManager(
        runtime_instance=Runtime(),
        registry=ServiceRegistry(),
        plugin_registry=plugins,
    )

    with pytest.raises(RuntimeError, match="Plugin plugin-c activation failed"):
        manager.startup()

    assert events == [
        "activate:plugin-a",
        "activate:plugin-b",
        "activate:plugin-c",
        "deactivate:plugin-b",
        "deactivate:plugin-a",
    ]

def test_plugin_activation_failure_rolls_back_services_after_plugins() -> None:
    events: list[str] = []
    registry = ServiceRegistry()
    plugins = PluginRegistry()

    registry.register(RecordingService("service-a", events))

    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )
    plugins.register(
        "plugin-b",
        lambda: FailingActivationPlugin("plugin-b", events),
    )

    manager = BootstrapManager(
        runtime_instance=Runtime(),
        registry=registry,
        plugin_registry=plugins,
    )

    with pytest.raises(RuntimeError, match="Plugin plugin-b activation failed"):
        manager.startup()

    assert events == [
        "validate:service-a",
        "initialize:service-a",
        "activate:plugin-a",
        "activate:plugin-b",
        "deactivate:plugin-a",
        "shutdown:service-a",
    ]

def test_critical_startup_failure_marks_runtime_failed_and_not_ready() -> None:
    registry = ServiceRegistry()
    runtime = Runtime()

    registry.register(
        RecordingService("service-a", [], valid=False),
    )

    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=registry,
        plugin_registry=PluginRegistry(),
    )

    with pytest.raises(RuntimeError, match="Service .* failed validation"):
        manager.startup()

    assert runtime.state is RuntimeState.FAILED
    assert runtime.is_ready is False

class InjectedFailureService(RecordingService):
    def __init__(
        self,
        name: str,
        events: list[str],
        error: Exception,
    ) -> None:
        super().__init__(name, events)
        self._error = error

    def initialize(self) -> None:
        self._events.append(f"initialize:{self.name}")
        raise self._error


def test_original_startup_exception_is_preserved_after_successful_rollback() -> None:
    events: list[str] = []
    registry = ServiceRegistry()
    original_error = RuntimeError("original startup failure")

    registry.register(RecordingService("service-a", events))
    registry.register(
        InjectedFailureService("service-b", events, original_error),
    )

    manager = BootstrapManager(
        runtime_instance=Runtime(),
        registry=registry,
        plugin_registry=PluginRegistry(),
    )

    with pytest.raises(RuntimeError) as exc_info:
        manager.startup()

    assert exc_info.value is original_error
    assert events[-1] == "shutdown:service-a"

def test_successful_startup_and_shutdown_behavior_remains_unchanged() -> None:
    events: list[str] = []
    registry = ServiceRegistry()
    plugins = PluginRegistry()
    runtime = Runtime()

    registry.register(RecordingService("service-a", events))
    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin("plugin-a", events),
    )

    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=registry,
        plugin_registry=plugins,
    )

    manager.startup()

    assert runtime.state is RuntimeState.READY
    assert runtime.is_ready is True

    manager.shutdown()

    assert events == [
        "validate:service-a",
        "initialize:service-a",
        "activate:plugin-a",
        "deactivate:plugin-a",
        "shutdown:service-a",
    ]
    assert runtime.state is RuntimeState.STOPPED
    assert runtime.is_ready is False
