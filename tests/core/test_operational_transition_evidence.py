from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest

from app.core.availability import CapabilityAvailabilityObserver
from app.core.capability_coverage import (
    MandatoryCapabilityCoverageEvaluator,
    MandatoryCapabilityCoverageResult,
    MandatoryCapabilityCoverageState,
)
from app.core.composition import CompositionRoot
from app.core.operational_transition_evidence import (
    OperationalTransitionEvidence,
)
from app.core.runtime import Runtime
from app.domain.operational_workload_evidence import (
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


def make_coverage(
    state: MandatoryCapabilityCoverageState,
) -> MandatoryCapabilityCoverageResult:
    if state is MandatoryCapabilityCoverageState.SATISFIED:
        return MandatoryCapabilityCoverageResult(
            state=state,
            required_capabilities=("pi-system",),
            satisfied_capabilities=("pi-system",),
            missing_capabilities=(),
            unavailable_capabilities=(),
            unknown_capabilities=(),
            ambiguous_capabilities=(),
        )

    return MandatoryCapabilityCoverageResult(
        state=state,
        required_capabilities=("pi-system",),
        satisfied_capabilities=(),
        missing_capabilities=("pi-system",),
        unavailable_capabilities=(),
        unknown_capabilities=(),
        ambiguous_capabilities=(),
    )


def test_operational_transition_evidence_is_immutable() -> None:
    evidence = OperationalTransitionEvidence()

    with pytest.raises(FrozenInstanceError):
        evidence.operational_workload = make_workload_evidence()


def test_supplied_evidence_objects_are_preserved_by_identity() -> None:
    workload = make_workload_evidence()
    coverage = make_coverage(
        MandatoryCapabilityCoverageState.SATISFIED
    )

    evidence = OperationalTransitionEvidence(
        operational_workload=workload,
        mandatory_capability_coverage=coverage,
    )

    assert evidence.operational_workload is workload
    assert evidence.mandatory_capability_coverage is coverage


def test_both_evidence_categories_absent_fails_closed() -> None:
    evidence = OperationalTransitionEvidence()

    assert evidence.is_complete is False


def test_missing_operational_workload_evidence_fails_closed() -> None:
    evidence = OperationalTransitionEvidence(
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.SATISFIED
        ),
    )

    assert evidence.is_complete is False


def test_missing_mandatory_capability_coverage_fails_closed() -> None:
    evidence = OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
    )

    assert evidence.is_complete is False


def test_unsatisfied_mandatory_capability_coverage_fails_closed() -> None:
    evidence = OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.UNSATISFIED
        ),
    )

    assert evidence.is_complete is False


def test_complete_external_evidence_requires_workload_and_satisfied_coverage() -> None:
    evidence = OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.SATISFIED
        ),
    )

    assert evidence.is_complete is True


def test_completeness_is_deterministic() -> None:
    evidence = OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.SATISFIED
        ),
    )

    first = evidence.is_complete
    second = evidence.is_complete
    third = evidence.is_complete

    assert first is True
    assert second is first
    assert third is first


def test_completeness_does_not_depend_on_runtime_state() -> None:
    evidence = OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.SATISFIED
        ),
    )
    runtime = Runtime()

    before = evidence.is_complete
    runtime.mark_ready()
    after = evidence.is_complete

    assert before is True
    assert after is True


def test_completeness_does_not_depend_on_request_admission() -> None:
    evidence = OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.SATISFIED
        ),
    )
    runtime = Runtime()

    before = evidence.is_complete
    runtime.enable_request_admission()
    after = evidence.is_complete

    assert before is True
    assert after is True


def test_aggregate_construction_does_not_mutate_workload_evidence() -> None:
    workload = make_workload_evidence()
    facade_entry = workload.facade_entry
    execution_start = workload.execution_start

    OperationalTransitionEvidence(
        operational_workload=workload,
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.SATISFIED
        ),
    )

    assert workload.facade_entry is facade_entry
    assert workload.execution_start is execution_start


def test_aggregate_construction_does_not_mutate_capability_coverage() -> None:
    coverage = make_coverage(
        MandatoryCapabilityCoverageState.SATISFIED
    )
    required = coverage.required_capabilities
    satisfied = coverage.satisfied_capabilities

    OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=coverage,
    )

    assert coverage.required_capabilities is required
    assert coverage.satisfied_capabilities is satisfied


def test_completeness_does_not_observe_or_evaluate_capabilities(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_observe(*args: object, **kwargs: object) -> object:
        raise AssertionError("Availability observation must not occur.")

    def fail_evaluate(*args: object, **kwargs: object) -> object:
        raise AssertionError("Coverage evaluation must not occur.")

    monkeypatch.setattr(
        CapabilityAvailabilityObserver,
        "observe_all",
        fail_observe,
    )
    monkeypatch.setattr(
        MandatoryCapabilityCoverageEvaluator,
        "evaluate",
        fail_evaluate,
    )

    evidence = OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.SATISFIED
        ),
    )

    assert evidence.is_complete is True


def test_external_evidence_does_not_modify_runtime_lifecycle() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    initial_state = runtime.state

    evidence = OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.SATISFIED
        ),
    )

    assert evidence.is_complete is True
    assert runtime.state is initial_state


def test_external_evidence_does_not_modify_request_admission() -> None:
    runtime = Runtime()
    runtime.mark_ready()
    runtime.enable_request_admission()
    initial_admission = runtime.is_request_admission_enabled

    evidence = OperationalTransitionEvidence(
        operational_workload=make_workload_evidence(),
        mandatory_capability_coverage=make_coverage(
            MandatoryCapabilityCoverageState.SATISFIED
        ),
    )

    assert evidence.is_complete is True
    assert runtime.is_request_admission_enabled is initial_admission


def test_operational_transition_evidence_has_no_lifecycle_authority() -> None:
    runtime = Runtime()
    evidence = OperationalTransitionEvidence()

    assert not hasattr(runtime, "mark_operational")
    assert not hasattr(evidence, "request_operational")


def test_composition_has_no_global_operational_transition_evidence() -> None:
    platform = CompositionRoot.build()

    assert not hasattr(platform, "operational_transition_evidence")
