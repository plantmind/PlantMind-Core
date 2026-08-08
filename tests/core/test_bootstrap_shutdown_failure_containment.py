import pytest

from app.core.bootstrap_manager import BootstrapManager
from app.core.plugins import Plugin, PluginRegistry
from app.core.runtime import Runtime
from app.core.runtime_state import RuntimeState
from app.core.services.base_service import BaseService
from app.core.services.service_registry import ServiceRegistry


class RecordingPlugin(Plugin):
    def __init__(
        self,
        name: str,
        events: list[str],
        deactivate_error: Exception | None = None,
    ) -> None:
        self._name = name
        self._events = events
        self._deactivate_error = deactivate_error

    @property
    def name(self) -> str:
        return self._name

    def activate(self) -> None:
        self._events.append(f"activate:{self.name}")

    def deactivate(self) -> None:
        self._events.append(f"deactivate:{self.name}")

        if self._deactivate_error is not None:
            raise self._deactivate_error


class RecordingService(BaseService):
    def __init__(
        self,
        name: str,
        events: list[str],
        shutdown_error: Exception | None = None,
    ) -> None:
        super().__init__(name)
        self._events = events
        self._shutdown_error = shutdown_error

    def validate(self) -> bool:
        return True

    def initialize(self) -> None:
        self._events.append(f"initialize:{self.name}")

    def shutdown(self) -> None:
        self._events.append(f"shutdown:{self.name}")

        if self._shutdown_error is not None:
            raise self._shutdown_error


def test_plugin_failure_does_not_prevent_service_shutdown() -> None:
    events: list[str] = []
    plugin_error = RuntimeError("plugin-a deactivation failed")
    plugins = PluginRegistry()
    services = ServiceRegistry()

    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin(
            "plugin-a",
            events,
            plugin_error,
        ),
    )
    services.register(RecordingService("service-a", events))

    runtime = Runtime()
    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=services,
        plugin_registry=plugins,
    )

    manager.startup()
    events.clear()

    with pytest.raises(RuntimeError) as exc_info:
        manager.shutdown()

    assert exc_info.value is plugin_error
    assert events == [
        "deactivate:plugin-a",
        "shutdown:service-a",
    ]
    assert runtime.state is RuntimeState.FAILED
    assert runtime.is_ready is False


def test_service_failure_does_not_prevent_remaining_service_shutdown() -> None:
    events: list[str] = []
    service_error = RuntimeError("service-z shutdown failed")
    services = ServiceRegistry()

    services.register(RecordingService("service-a", events))
    services.register(
        RecordingService(
            "service-z",
            events,
            service_error,
        )
    )

    runtime = Runtime()
    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=services,
        plugin_registry=PluginRegistry(),
    )

    manager.startup()
    events.clear()

    with pytest.raises(RuntimeError) as exc_info:
        manager.shutdown()

    assert exc_info.value is service_error
    assert events == [
        "shutdown:service-z",
        "shutdown:service-a",
    ]
    assert runtime.state is RuntimeState.FAILED
    assert runtime.is_ready is False


def test_failed_shutdown_never_transitions_runtime_to_stopped() -> None:
    events: list[str] = []
    service_error = RuntimeError("service-a shutdown failed")
    services = ServiceRegistry()

    services.register(
        RecordingService(
            "service-a",
            events,
            service_error,
        )
    )

    runtime = Runtime()
    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=services,
        plugin_registry=PluginRegistry(),
    )

    manager.startup()

    with pytest.raises(RuntimeError):
        manager.shutdown()

    assert runtime.state is RuntimeState.FAILED
    assert runtime.state is not RuntimeState.STOPPED
    assert runtime.is_ready is False


def test_multiple_shutdown_failures_are_flattened_in_encounter_order() -> None:
    events: list[str] = []
    plugin_a_error = RuntimeError("plugin-a deactivation failed")
    plugin_b_error = ValueError("plugin-b deactivation failed")
    service_error = LookupError("service-z shutdown failed")

    plugins = PluginRegistry()
    services = ServiceRegistry()

    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin(
            "plugin-a",
            events,
            plugin_a_error,
        ),
    )
    plugins.register(
        "plugin-b",
        lambda: RecordingPlugin(
            "plugin-b",
            events,
            plugin_b_error,
        ),
    )
    services.register(
        RecordingService(
            "service-z",
            events,
            service_error,
        )
    )

    runtime = Runtime()
    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=services,
        plugin_registry=plugins,
    )

    manager.startup()
    events.clear()

    with pytest.raises(ExceptionGroup) as exc_info:
        manager.shutdown()

    assert events == [
        "deactivate:plugin-b",
        "deactivate:plugin-a",
        "shutdown:service-z",
    ]
    assert exc_info.value.exceptions == (
        plugin_b_error,
        plugin_a_error,
        service_error,
    )
    assert runtime.state is RuntimeState.FAILED
    assert runtime.is_ready is False


def test_failed_shutdown_leaves_request_admission_disabled() -> None:
    runtime = Runtime()
    services = ServiceRegistry()
    shutdown_error = RuntimeError("service-a shutdown failed")

    services.register(
        RecordingService(
            "service-a",
            [],
            shutdown_error,
        )
    )

    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=services,
        plugin_registry=PluginRegistry(),
    )

    manager.startup()

    assert runtime.is_request_admission_enabled is True

    with pytest.raises(RuntimeError):
        manager.shutdown()

    assert runtime.is_request_admission_enabled is False
    assert runtime.state is RuntimeState.FAILED
