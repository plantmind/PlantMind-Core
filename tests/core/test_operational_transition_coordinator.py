from __future__ import annotations

from uuid import uuid4

import pytest

from app.core.availability.observation import CapabilityAvailabilityObservation
from app.core.availability.state import CapabilityAvailabilityState
from app.core.capability_coverage import (
    MandatoryCapabilityCoverageResult,
    MandatoryCapabilityCoverageState,
)
from app.core.operational_transition_coordinator import (
    OperationalTransitionCoordinator,
)
from app.core.operational_transition_evidence import OperationalTransitionEvidence
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


def make_observation() -> CapabilityAvailabilityObservation:
    from datetime import UTC, datetime

    return CapabilityAvailabilityObservation(
        capability_name="deployment-capability",
        state=CapabilityAvailabilityState.AVAILABLE,
        observed_at=datetime.now(UTC),
        source_name="deployment-source",
    )


def make_coverage(
    state: MandatoryCapabilityCoverageState,
) -> MandatoryCapabilityCoverageResult:
    if state is MandatoryCapabilityCoverageState.SATISFIED:
        return MandatoryCapabilityCoverageResult(
            state=state,
            required_capabilities=("deployment-capability",),
            satisfied_capabilities=("deployment-capability",),
            missing_capabilities=(),
            unavailable_capabilities=(),
            unknown_capabilities=(),
            ambiguous_capabilities=(),
        )

    return MandatoryCapabilityCoverageResult(
        state=state,
        required_capabilities=("deployment-capability",),
        satisfied_capabilities=(),
        missing_capabilities=("deployment-capability",),
        unavailable_capabilities=(),
        unknown_capabilities=(),
        ambiguous_capabilities=(),
    )


class RecordingObserver:
    def __init__(
        self,
        observations: tuple[CapabilityAvailabilityObservation, ...],
    ) -> None:
        self.observations = observations
        self.calls = 0

    def observe_all(
        self,
    ) -> tuple[CapabilityAvailabilityObservation, ...]:
        self.calls += 1
        return self.observations


class RecordingEvaluator:
    def __init__(
        self,
        result: MandatoryCapabilityCoverageResult,
    ) -> None:
        self.result = result
        self.calls = 0
        self.received_observations: object | None = None

    def evaluate(
        self,
        observations: object,
    ) -> MandatoryCapabilityCoverageResult:
        self.calls += 1
        self.received_observations = observations
        return self.result


class RecordingRuntime:
    def __init__(self) -> None:
        self.calls = 0
        self.received_evidence: OperationalTransitionEvidence | None = None

    def request_operational(
        self,
        evidence: OperationalTransitionEvidence,
    ) -> None:
        self.calls += 1
        self.received_evidence = evidence


class RejectingRuntime(RecordingRuntime):
    def request_operational(
        self,
        evidence: OperationalTransitionEvidence,
    ) -> None:
        super().request_operational(evidence)
        raise RuntimeError("transition rejected")


def make_coordinator(
    runtime: object,
    observer: object,
    evaluator: object,
) -> OperationalTransitionCoordinator:
    return OperationalTransitionCoordinator(
        runtime=runtime,
        availability_observer=observer,
        coverage_evaluator=evaluator,
    )


def test_coordination_observes_availability_exactly_once() -> None:
    observations = (make_observation(),)
    observer = RecordingObserver(observations)
    evaluator = RecordingEvaluator(
        make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    )
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, observer, evaluator)

    coordinator.request_operational(make_workload_evidence())

    assert observer.calls == 1


def test_observation_snapshot_is_forwarded_unchanged() -> None:
    observations = (make_observation(),)
    observer = RecordingObserver(observations)
    evaluator = RecordingEvaluator(
        make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    )
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, observer, evaluator)

    coordinator.request_operational(make_workload_evidence())

    assert evaluator.received_observations is observations


def test_coverage_is_evaluated_exactly_once() -> None:
    observer = RecordingObserver((make_observation(),))
    evaluator = RecordingEvaluator(
        make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    )
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, observer, evaluator)

    coordinator.request_operational(make_workload_evidence())

    assert evaluator.calls == 1


def test_transition_evidence_preserves_workload_and_coverage_identity() -> None:
    workload = make_workload_evidence()
    coverage = make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    observer = RecordingObserver((make_observation(),))
    evaluator = RecordingEvaluator(coverage)
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, observer, evaluator)

    evidence = coordinator.request_operational(workload)

    assert evidence.operational_workload is workload
    assert evidence.mandatory_capability_coverage is coverage


def test_exact_constructed_evidence_is_delegated_and_returned() -> None:
    observer = RecordingObserver((make_observation(),))
    evaluator = RecordingEvaluator(
        make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    )
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, observer, evaluator)

    evidence = coordinator.request_operational(make_workload_evidence())

    assert runtime.calls == 1
    assert runtime.received_evidence is evidence


def test_none_workload_evidence_is_preserved_for_fail_closed_runtime() -> None:
    coverage = make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    observer = RecordingObserver((make_observation(),))
    evaluator = RecordingEvaluator(coverage)
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, observer, evaluator)

    evidence = coordinator.request_operational(None)

    assert evidence.operational_workload is None
    assert evidence.mandatory_capability_coverage is coverage
    assert evidence.is_complete is False
    assert runtime.received_evidence is evidence


def test_unsatisfied_coverage_is_preserved_without_reclassification() -> None:
    coverage = make_coverage(MandatoryCapabilityCoverageState.UNSATISFIED)
    observer = RecordingObserver((make_observation(),))
    evaluator = RecordingEvaluator(coverage)
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, observer, evaluator)

    evidence = coordinator.request_operational(make_workload_evidence())

    assert evidence.mandatory_capability_coverage is coverage
    assert evidence.is_complete is False


def test_runtime_rejection_is_propagated_without_retry() -> None:
    observer = RecordingObserver((make_observation(),))
    evaluator = RecordingEvaluator(
        make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    )
    runtime = RejectingRuntime()
    coordinator = make_coordinator(runtime, observer, evaluator)

    with pytest.raises(RuntimeError, match="transition rejected"):
        coordinator.request_operational(make_workload_evidence())

    assert observer.calls == 1
    assert evaluator.calls == 1
    assert runtime.calls == 1


def test_observation_failure_prevents_runtime_delegation() -> None:
    class FailingObserver:
        def observe_all(self) -> tuple[CapabilityAvailabilityObservation, ...]:
            raise RuntimeError("observation failure")

    evaluator = RecordingEvaluator(
        make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    )
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, FailingObserver(), evaluator)

    with pytest.raises(RuntimeError, match="observation failure"):
        coordinator.request_operational(make_workload_evidence())

    assert evaluator.calls == 0
    assert runtime.calls == 0


def test_coverage_failure_prevents_runtime_delegation() -> None:
    class FailingEvaluator:
        def evaluate(self, observations: object) -> MandatoryCapabilityCoverageResult:
            raise RuntimeError("coverage failure")

    observer = RecordingObserver((make_observation(),))
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, observer, FailingEvaluator())

    with pytest.raises(RuntimeError, match="coverage failure"):
        coordinator.request_operational(make_workload_evidence())

    assert observer.calls == 1
    assert runtime.calls == 0


def test_coordinator_retains_exact_dependency_instances() -> None:
    observer = RecordingObserver((make_observation(),))
    evaluator = RecordingEvaluator(
        make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    )
    runtime = RecordingRuntime()

    coordinator = make_coordinator(runtime, observer, evaluator)

    assert coordinator.runtime is runtime
    assert coordinator.availability_observer is observer
    assert coordinator.coverage_evaluator is evaluator


def test_coordinator_has_no_persistent_transition_evidence_state() -> None:
    observer = RecordingObserver((make_observation(),))
    evaluator = RecordingEvaluator(
        make_coverage(MandatoryCapabilityCoverageState.SATISFIED)
    )
    runtime = RecordingRuntime()
    coordinator = make_coordinator(runtime, observer, evaluator)

    coordinator.request_operational(make_workload_evidence())

    assert not hasattr(coordinator, "last_evidence")
    assert not hasattr(coordinator, "evidence_history")
    assert not hasattr(coordinator, "transition_history")
