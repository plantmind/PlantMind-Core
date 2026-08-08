import pytest

from app.core.bootstrap_manager import BootstrapManager
from app.core.health import HealthCapability
from app.core.plugins import Plugin, PluginRegistry
from app.core.readiness import ReadinessEvidence
from app.core.runtime import Runtime
from app.core.runtime_state import RuntimeState
from app.core.services.base_service import BaseService
from app.core.services.service_registry import ServiceRegistry


class RecordingConfiguration:
    def __init__(
        self,
        events: list[str],
        error: Exception | None = None,
    ) -> None:
        self._events = events
        self._error = error

    def validate(self) -> None:
        self._events.append("configuration:validate")

        if self._error is not None:
            raise self._error


class RecordingService(BaseService):
    def __init__(self, events: list[str]) -> None:
        super().__init__("service-a")
        self._events = events

    def validate(self) -> bool:
        self._events.append("service:validate")
        return True

    def initialize(self) -> None:
        self._events.append("service:initialize")

    def shutdown(self) -> None:
        self._events.append("service:shutdown")


class RecordingPlugin(Plugin):
    def __init__(self, events: list[str]) -> None:
        self._events = events

    @property
    def name(self) -> str:
        return "plugin-a"

    def activate(self) -> None:
        self._events.append("plugin:activate")

    def deactivate(self) -> None:
        self._events.append("plugin:deactivate")


class RecordingRuntime(Runtime):
    def __init__(
        self,
        events: list[str],
        reject_readiness: bool = False,
    ) -> None:
        super().__init__()
        self._events = events
        self._reject_readiness = reject_readiness
        self.readiness_evidence: ReadinessEvidence | None = None

    def request_readiness(
        self,
        evidence: ReadinessEvidence,
    ) -> None:
        self._events.append("runtime:request_readiness")
        self.readiness_evidence = evidence

        if self._reject_readiness:
            raise RuntimeError("Runtime readiness rejected.")

        super().request_readiness(evidence)

    def enable_request_admission(self) -> None:
        self._events.append("admission:enabled")
        super().enable_request_admission()


def build_manager(
    events: list[str],
    *,
    configuration_error: Exception | None = None,
    reject_readiness: bool = False,
) -> tuple[BootstrapManager, RecordingRuntime]:
    runtime = RecordingRuntime(
        events,
        reject_readiness=reject_readiness,
    )
    registry = ServiceRegistry()
    registry.register(RecordingService(events))

    plugins = PluginRegistry()
    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin(events),
    )

    configuration = RecordingConfiguration(
        events,
        error=configuration_error,
    )
    health = HealthCapability(
        runtime_instance=runtime,
        registry=registry,
    )

    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=registry,
        plugin_registry=plugins,
        configuration=configuration,
        health=health,
    )

    return manager, runtime


def test_configuration_validation_precedes_service_validation() -> None:
    events: list[str] = []
    manager, _ = build_manager(events)

    manager.startup()

    assert events.index("configuration:validate") < events.index(
        "service:validate"
    )


def test_configuration_failure_prevents_remaining_startup() -> None:
    events: list[str] = []
    error = RuntimeError("Configuration validation failed.")
    manager, runtime = build_manager(
        events,
        configuration_error=error,
    )

    with pytest.raises(RuntimeError) as exc_info:
        manager.startup()

    assert exc_info.value is error
    assert events == ["configuration:validate"]
    assert runtime.state is RuntimeState.FAILED
    assert runtime.is_ready is False
    assert runtime.is_request_admission_enabled is False


def test_bootstrap_requests_readiness_before_admission() -> None:
    events: list[str] = []
    manager, runtime = build_manager(events)

    manager.startup()

    assert events == [
        "configuration:validate",
        "service:validate",
        "service:initialize",
        "plugin:activate",
        "runtime:request_readiness",
        "admission:enabled",
    ]
    assert runtime.state is RuntimeState.READY
    assert runtime.is_request_admission_enabled is True


def test_bootstrap_supplies_complete_readiness_evidence() -> None:
    events: list[str] = []
    manager, runtime = build_manager(events)

    manager.startup()

    evidence = runtime.readiness_evidence

    assert evidence is not None
    assert evidence.is_complete is True
    assert evidence.configuration_validated is True
    assert evidence.runtime_created is True
    assert evidence.bootstrap_completed is True
    assert evidence.required_services_initialized is True
    assert evidence.required_services_validated is True
    assert evidence.service_registry_operational is True
    assert evidence.health_capability_initialized is True
    assert evidence.runtime_metadata_available is True


def test_readiness_rejection_rolls_back_plugins_and_services() -> None:
    events: list[str] = []
    manager, runtime = build_manager(
        events,
        reject_readiness=True,
    )

    with pytest.raises(
        RuntimeError,
        match="Runtime readiness rejected",
    ):
        manager.startup()

    assert events == [
        "configuration:validate",
        "service:validate",
        "service:initialize",
        "plugin:activate",
        "runtime:request_readiness",
        "plugin:deactivate",
        "service:shutdown",
    ]
    assert runtime.state is RuntimeState.FAILED
    assert runtime.is_ready is False
    assert runtime.is_request_admission_enabled is False


class ObservationOnlyHealth(HealthCapability):
    def get_status(self):
        raise AssertionError(
            "HealthCapability must not decide Runtime readiness."
        )


def test_health_capability_is_not_used_for_readiness_decision() -> None:
    events: list[str] = []
    runtime = RecordingRuntime(events)
    registry = ServiceRegistry()
    registry.register(RecordingService(events))

    plugins = PluginRegistry()
    plugins.register(
        "plugin-a",
        lambda: RecordingPlugin(events),
    )

    health = ObservationOnlyHealth(
        runtime_instance=runtime,
        registry=registry,
    )

    manager = BootstrapManager(
        runtime_instance=runtime,
        registry=registry,
        plugin_registry=plugins,
        configuration=RecordingConfiguration(events),
        health=health,
    )

    manager.startup()

    assert runtime.state is RuntimeState.READY
    assert runtime.is_request_admission_enabled is True

