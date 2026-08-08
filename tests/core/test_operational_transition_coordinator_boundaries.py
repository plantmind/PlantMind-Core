from __future__ import annotations

import pytest

from app.core.availability import CapabilityAvailabilityObserver
from app.core.availability.observation import CapabilityAvailabilityObservation
from app.core.availability.source import CapabilityAvailabilitySource
from app.core.capability_coverage import (
    MandatoryCapabilityCoverageEvaluator,
    MandatoryCapabilityCoverageState,
)
from app.core.capability_policy import (
    MandatoryCapabilityPolicy,
    MandatoryCapabilityPolicyState,
)
from app.core.composition import CompositionRoot
from app.core.operational_transition_coordinator import (
    OperationalTransitionCoordinator,
)
from app.core.operational_transition_evidence import OperationalTransitionEvidence
from app.services.orchestration.workflow import WorkflowExecution, WorkflowStage


class CaptureRuntime:
    def __init__(self) -> None:
        self.evidence: OperationalTransitionEvidence | None = None

    def request_operational(
        self,
        evidence: OperationalTransitionEvidence,
    ) -> None:
        self.evidence = evidence


class FailingSource(CapabilityAvailabilitySource):
    @property
    def capability_name(self) -> str:
        return "deployment-capability"

    @property
    def source_name(self) -> str:
        return "failing-source"

    def observe(self) -> CapabilityAvailabilityObservation:
        raise RuntimeError("source failure")


def test_coordinator_rejects_workflow_execution_as_input() -> None:
    policy = MandatoryCapabilityPolicy(
        state=MandatoryCapabilityPolicyState.UNCONFIGURED,
        required_capabilities=(),
    )
    coordinator = OperationalTransitionCoordinator(
        runtime=CaptureRuntime(),
        availability_observer=CapabilityAvailabilityObserver(),
        coverage_evaluator=MandatoryCapabilityCoverageEvaluator(policy),
    )
    execution = WorkflowExecution(
        result={},
        stages=(WorkflowStage.COMPLETED,),
    )

    with pytest.raises(TypeError):
        coordinator.request_operational(execution)


def test_source_failure_flows_through_observer_as_unknown() -> None:
    policy = MandatoryCapabilityPolicy(
        state=MandatoryCapabilityPolicyState.CONFIGURED,
        required_capabilities=("deployment-capability",),
    )
    runtime = CaptureRuntime()
    coordinator = OperationalTransitionCoordinator(
        runtime=runtime,
        availability_observer=CapabilityAvailabilityObserver(
            sources=(FailingSource(),),
        ),
        coverage_evaluator=MandatoryCapabilityCoverageEvaluator(policy),
    )

    evidence = coordinator.request_operational(None)

    coverage = evidence.mandatory_capability_coverage
    assert coverage is not None
    assert coverage.state is MandatoryCapabilityCoverageState.UNSATISFIED
    assert coverage.unknown_capabilities == ("deployment-capability",)
    assert runtime.evidence is evidence


def test_bootstrap_does_not_execute_operational_transition_coordination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_request(
        self: OperationalTransitionCoordinator,
        workload_evidence: object,
    ) -> object:
        raise AssertionError(
            "Bootstrap must not execute operational transition coordination."
        )

    monkeypatch.setattr(
        OperationalTransitionCoordinator,
        "request_operational",
        forbidden_request,
    )

    platform = CompositionRoot.build()
    platform.bootstrap.startup()


def test_application_facade_does_not_execute_operational_transition_coordination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_request(
        self: OperationalTransitionCoordinator,
        workload_evidence: object,
    ) -> object:
        raise AssertionError(
            "ApplicationFacade must not execute operational transition coordination."
        )

    monkeypatch.setattr(
        OperationalTransitionCoordinator,
        "request_operational",
        forbidden_request,
    )

    platform = CompositionRoot.build()
    platform.application_facade.analyze(())


def test_coordinator_has_no_independent_lifecycle_authority() -> None:
    platform = CompositionRoot.build()
    coordinator = platform.operational_transition_coordinator

    assert not hasattr(coordinator, "mark_operational")
    assert not hasattr(coordinator, "state")
    assert not hasattr(coordinator, "is_ready")
    assert not hasattr(coordinator, "is_request_admission_enabled")
