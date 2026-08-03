from app.core.runtime_state import RuntimeState


def test_runtime_state_contains_required_states() -> None:
    expected = {
        "CREATED",
        "BOOTSTRAPPING",
        "INITIALIZING",
        "READY",
        "OPERATIONAL",
        "DEGRADED",
        "STOPPING",
        "STOPPED",
        "FAILED",
    }

    assert {state.name for state in RuntimeState} == expected


def test_runtime_state_values_are_unique() -> None:
    values = [state.value for state in RuntimeState]

    assert len(values) == len(set(values))