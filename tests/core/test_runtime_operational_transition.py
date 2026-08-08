from __future__ import annotations

from uuid import uuid4

import pytest

from app.core.capability_coverage import (
    MandatoryCapabilityCoverageResult,
    MandatoryCapabilityCoverageState,
)
from app.core.operational_transition_evidence import OperationalTransitionEvidence
from app.core.runtime import Runtime
from app.core.runtime_state import RuntimeState
from app.services.orchestration.workload_evidence import (
    ApplicationFacadeEntryEvidence,
    OperationalWorkloadEvidence,
    WorkflowExecutionStartEvidence,
)


def make_workload_evidence() -> OperationalWorkloadEvidence:
    workload_id = uuid4()
    return OperationalWorkloadEvidence(
        facade_entry=ApplicationFacadeEntryEvidence(
            workload_id=workload_id,
        ),
        execution_start=WorkflowExecutionStartEvidence(
            workload_id=workload_id,
        ),
    )


def make_complete_evidence() -> OperationalTransitionEvidence:
    return OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=MandatoryCapabilityCoverageResult(
            state=MandatoryCapabilityCoverageState.SATISFIED,
            required_capabilities=("pi-system",),
            satisfied_capabilities=("pi-system",),
            missing_capabilities=(),
            unavailable_capabilities=(),
            unknown_capabilities=(),
            ambiguous_capabilities=(),
        ),
    )


def make_incomplete_evidence() -> OperationalTransitionEvidence:
    return OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
    )


def test_runtime_exposes_no_public_mark_operational_bypass() -> None:
    runtime = Runtime()

    assert not hasattr(runtime, "mark_operational")


def test_complete_evidence_cannot_transition_created_runtime() -> None:
    runtime = Runtime()
    evidence = make_complete_evidence()

    with pytest.raises(RuntimeError):
        runtime.request_operational(evidence)

    assert runtime.state is RuntimeState.CREATED
    assert runtime.is_ready is False
    assert runtime.is_request_admission_enabled is False


def test_ready_runtime_requires_request_admission() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    evidence = make_complete_evidence()

    with pytest.raises(RuntimeError):
        runtime.request_operational(evidence)

    assert runtime.state is RuntimeState.READY
    assert runtime.is_ready is True
    assert runtime.is_request_admission_enabled is False


def test_ready_admitting_runtime_requires_complete_external_evidence() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    runtime.enable_request_admission()
    evidence = make_incomplete_evidence()

    with pytest.raises(RuntimeError):
        runtime.request_operational(evidence)

    assert runtime.state is RuntimeState.READY
    assert runtime.is_ready is True
    assert runtime.is_request_admission_enabled is True


def test_complete_operational_transition_enters_operational_state() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    runtime.enable_request_admission()

    runtime.request_operational(make_complete_evidence())

    assert runtime.state is RuntimeState.OPERATIONAL


def test_successful_operational_transition_preserves_readiness_and_admission() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    runtime.enable_request_admission()

    runtime.request_operational(make_complete_evidence())

    assert runtime.is_ready is True
    assert runtime.ready is True
    assert runtime.is_request_admission_enabled is True


def test_successful_transition_preserves_supplied_evidence() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    runtime.enable_request_admission()
    evidence = make_complete_evidence()
    workload = evidence.operational_workload
    coverage = evidence.mandatory_capability_coverage

    runtime.request_operational(evidence)

    assert evidence.operational_workload is workload
    assert evidence.mandatory_capability_coverage is coverage
    assert evidence.is_complete is True


@pytest.mark.parametrize(
    "state",
    (
        RuntimeState.CREATED,
        RuntimeState.BOOTSTRAPPING,
        RuntimeState.INITIALIZING,
        RuntimeState.OPERATIONAL,
        RuntimeState.DEGRADED,
        RuntimeState.STOPPING,
        RuntimeState.STOPPED,
        RuntimeState.FAILED,
    ),
)
def test_operational_transition_rejects_every_non_ready_state(
    state: RuntimeState,
) -> None:
    runtime = Runtime()
    runtime.state = state
    runtime.ready = False
    runtime.enable_request_admission()
    evidence = make_complete_evidence()

    before_state = runtime.state
    before_ready = runtime.is_ready
    before_admission = runtime.is_request_admission_enabled

    with pytest.raises(RuntimeError):
        runtime.request_operational(evidence)

    assert runtime.state is before_state
    assert runtime.is_ready is before_ready
    assert runtime.is_request_admission_enabled is before_admission


def test_repeated_operational_transition_is_rejected_atomically() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    runtime.enable_request_admission()
    evidence = make_complete_evidence()

    runtime.request_operational(evidence)

    with pytest.raises(RuntimeError):
        runtime.request_operational(evidence)

    assert runtime.state is RuntimeState.OPERATIONAL
    assert runtime.is_ready is True
    assert runtime.is_request_admission_enabled is True


def test_runtime_status_reports_operational_after_transition() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    runtime.enable_request_admission()

    runtime.request_operational(make_complete_evidence())

    assert runtime.status["state"] == "operational"
    assert runtime.status["ready"] is True
    assert "operational" not in runtime.status


def test_rejected_transition_does_not_disable_request_admission() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    runtime.enable_request_admission()

    with pytest.raises(RuntimeError):
        runtime.request_operational(make_incomplete_evidence())

    assert runtime.state is RuntimeState.READY
    assert runtime.is_ready is True
    assert runtime.is_request_admission_enabled is True
