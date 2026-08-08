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
