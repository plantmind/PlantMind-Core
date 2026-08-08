from app.core.runtime import Runtime
from app.core.runtime_state import RuntimeState


def test_runtime_starts_in_created_state() -> None:
    runtime = Runtime()

    assert runtime.state is RuntimeState.CREATED
    assert runtime.is_ready is False


def test_mark_ready_preserves_backward_compatibility() -> None:
    runtime = Runtime()

    runtime.mark_ready()

    assert runtime.is_ready is True
    assert runtime.ready is True


def test_mark_not_ready_preserves_backward_compatibility() -> None:
    runtime = Runtime()
    runtime.mark_ready()

    runtime.mark_not_ready()

    assert runtime.is_ready is False
    assert runtime.ready is False


def test_runtime_status_exposes_state_and_readiness() -> None:
    runtime = Runtime()

    status = runtime.status

    assert status["state"] == "created"
    assert status["ready"] is False
    assert status["platform"] == runtime.platform_name
    assert status["version"] == runtime.version
    assert status["environment"] == runtime.environment
    assert status["deployment"] == runtime.deployment


def test_mark_failed_sets_failed_state_and_not_ready() -> None:
    runtime = Runtime()
    runtime.mark_ready()

    runtime.mark_failed()

    assert runtime.state is RuntimeState.FAILED
    assert runtime.is_ready is False
    assert runtime.ready is False


def test_mark_stopping_sets_stopping_state_and_not_ready() -> None:
    runtime = Runtime()
    runtime.mark_ready()

    runtime.mark_stopping()

    assert runtime.state is RuntimeState.STOPPING
    assert runtime.is_ready is False
    assert runtime.ready is False

def test_request_admission_is_disabled_by_default() -> None:
    runtime = Runtime()

    assert runtime.is_request_admission_enabled is False


def test_request_admission_can_be_enabled() -> None:
    runtime = Runtime()

    runtime.enable_request_admission()

    assert runtime.is_request_admission_enabled is True


def test_request_admission_can_be_disabled() -> None:
    runtime = Runtime()
    runtime.enable_request_admission()

    runtime.disable_request_admission()

    assert runtime.is_request_admission_enabled is False


def test_mark_stopping_disables_request_admission() -> None:
    runtime = Runtime()
    runtime.enable_request_admission()

    runtime.mark_stopping()

    assert runtime.is_request_admission_enabled is False
    assert runtime.state is RuntimeState.STOPPING


def test_mark_failed_disables_request_admission() -> None:
    runtime = Runtime()
    runtime.enable_request_admission()

    runtime.mark_failed()

    assert runtime.is_request_admission_enabled is False
    assert runtime.state is RuntimeState.FAILED
