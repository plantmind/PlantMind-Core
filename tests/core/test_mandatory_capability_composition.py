from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.core.availability.observation import CapabilityAvailabilityObservation
from app.core.availability.observer import CapabilityAvailabilityObserver
from app.core.availability.source import CapabilityAvailabilitySource
from app.core.availability.state import CapabilityAvailabilityState
from app.core.capability_coverage import (
    MandatoryCapabilityCoverageEvaluator,
    MandatoryCapabilityCoverageState,
)
from app.core.capability_policy import (
    MandatoryCapabilityPolicy,
    MandatoryCapabilityPolicyState,
)
from app.core.composition.composition_root import (
    CompositionRoot,
    build_platform_composition,
)
from app.core.operational_transition_evidence import OperationalTransitionEvidence
from app.core.runtime import Runtime


class RecordingSource(CapabilityAvailabilitySource):
    def __init__(
        self,
        capability_name: str,
        source_name: str,
        state: CapabilityAvailabilityState = CapabilityAvailabilityState.AVAILABLE,
    ) -> None:
        self._capability_name = capability_name
        self._source_name = source_name
        self._state = state
        self.observe_calls = 0

    @property
    def capability_name(self) -> str:
        return self._capability_name

    @property
    def source_name(self) -> str:
        return self._source_name

    def observe(self) -> CapabilityAvailabilityObservation:
        self.observe_calls += 1
        return CapabilityAvailabilityObservation(
            capability_name=self.capability_name,
            state=self._state,
            observed_at=datetime.now(UTC),
            source_name=self.source_name,
        )


class FailingSource(CapabilityAvailabilitySource):
    @property
    def capability_name(self) -> str:
        return "deployment-capability"

    @property
    def source_name(self) -> str:
        return "failing-source"

    def observe(self) -> CapabilityAvailabilityObservation:
        raise RuntimeError("source failure")


def configured_policy(
    *capabilities: str,
) -> MandatoryCapabilityPolicy:
    return MandatoryCapabilityPolicy(
        state=MandatoryCapabilityPolicyState.CONFIGURED,
        required_capabilities=tuple(capabilities),
    )


def test_default_composition_preserves_fail_closed_capability_defaults() -> None:
    platform = CompositionRoot.build()

    assert platform.availability_observer._sources == ()
    assert (
        platform.mandatory_capability_policy.state
        is MandatoryCapabilityPolicyState.UNCONFIGURED
    )
    assert platform.mandatory_capability_policy.required_capabilities == ()

    coverage = platform.mandatory_capability_coverage_evaluator.evaluate(
        platform.availability_observer.observe_all()
    )

    assert coverage.state is MandatoryCapabilityCoverageState.UNSATISFIED


def test_explicit_availability_sources_preserve_order_and_identity() -> None:
    first = RecordingSource("capability-a", "source-a")
    second = RecordingSource("capability-b", "source-b")

    platform = CompositionRoot.build(
        capability_availability_sources=(first, second),
    )

    assert platform.availability_observer._sources == (first, second)
    assert platform.availability_observer._sources[0] is first
    assert platform.availability_observer._sources[1] is second


def test_availability_sources_are_not_invoked_during_composition() -> None:
    first = RecordingSource("capability-a", "source-a")
    second = RecordingSource("capability-b", "source-b")

    CompositionRoot.build(
        capability_availability_sources=(first, second),
    )

    assert first.observe_calls == 0
    assert second.observe_calls == 0


def test_explicit_policy_identity_is_preserved_across_composition() -> None:
    policy = configured_policy("deployment-capability")

    platform = CompositionRoot.build(
        mandatory_capability_policy=policy,
    )

    assert platform.mandatory_capability_policy is policy
    assert platform.container.resolve(MandatoryCapabilityPolicy) is policy
    assert platform.mandatory_capability_coverage_evaluator._policy is policy


def test_configured_policy_without_matching_source_is_valid_composition() -> None:
    policy = configured_policy("deployment-capability")

    platform = CompositionRoot.build(
        mandatory_capability_policy=policy,
    )

    coverage = platform.mandatory_capability_coverage_evaluator.evaluate(
        platform.availability_observer.observe_all()
    )

    assert coverage.state is MandatoryCapabilityCoverageState.UNSATISFIED
    assert coverage.missing_capabilities == ("deployment-capability",)


def test_duplicate_capability_sources_are_preserved_for_ambiguity_evaluation() -> None:
    first = RecordingSource("deployment-capability", "source-a")
    second = RecordingSource("deployment-capability", "source-b")
    policy = configured_policy("deployment-capability")

    platform = CompositionRoot.build(
        capability_availability_sources=(first, second),
        mandatory_capability_policy=policy,
    )

    observations = platform.availability_observer.observe_all()
    coverage = platform.mandatory_capability_coverage_evaluator.evaluate(
        observations
    )

    assert platform.availability_observer._sources == (first, second)
    assert coverage.state is MandatoryCapabilityCoverageState.UNSATISFIED
    assert coverage.ambiguous_capabilities == ("deployment-capability",)


def test_source_failures_remain_owned_by_availability_observer() -> None:
    source = FailingSource()
    policy = configured_policy("deployment-capability")

    platform = CompositionRoot.build(
        capability_availability_sources=(source,),
        mandatory_capability_policy=policy,
    )

    observations = platform.availability_observer.observe_all()

    assert len(observations) == 1
    assert observations[0].state is CapabilityAvailabilityState.UNKNOWN


def test_composition_does_not_evaluate_coverage_during_build(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_evaluate(
        self: MandatoryCapabilityCoverageEvaluator,
        observations: object,
    ) -> object:
        raise AssertionError("Composition must not evaluate capability coverage.")

    monkeypatch.setattr(
        MandatoryCapabilityCoverageEvaluator,
        "evaluate",
        forbidden_evaluate,
    )

    CompositionRoot.build(
        mandatory_capability_policy=configured_policy(
            "deployment-capability"
        ),
    )


def test_composition_does_not_request_operational_transition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_request(
        self: Runtime,
        evidence: OperationalTransitionEvidence,
    ) -> None:
        raise AssertionError(
            "Composition must not request an operational transition."
        )

    monkeypatch.setattr(
        Runtime,
        "request_operational",
        forbidden_request,
    )

    CompositionRoot.build(
        mandatory_capability_policy=configured_policy(
            "deployment-capability"
        ),
    )


def test_composition_does_not_register_operational_transition_evidence() -> None:
    platform = CompositionRoot.build()

    assert not platform.container.is_registered(OperationalTransitionEvidence)
    assert not hasattr(platform, "operational_transition_evidence")


def test_explicit_composition_remains_capability_name_agnostic() -> None:
    source = RecordingSource(
        "deployment-capability-alpha",
        "deployment-source-alpha",
    )
    policy = configured_policy("deployment-capability-alpha")

    platform = CompositionRoot.build(
        capability_availability_sources=(source,),
        mandatory_capability_policy=policy,
    )

    observations = platform.availability_observer.observe_all()
    coverage = platform.mandatory_capability_coverage_evaluator.evaluate(
        observations
    )

    assert coverage.state is MandatoryCapabilityCoverageState.SATISFIED
    assert coverage.required_capabilities == ("deployment-capability-alpha",)


def test_no_argument_composition_remains_backward_compatible() -> None:
    platform = CompositionRoot.build()

    assert isinstance(
        platform.availability_observer,
        CapabilityAvailabilityObserver,
    )
    assert isinstance(
        platform.mandatory_capability_coverage_evaluator,
        MandatoryCapabilityCoverageEvaluator,
    )


def test_positional_plugin_registration_argument_remains_backward_compatible() -> None:
    platform = CompositionRoot.build(())

    assert isinstance(
        platform.availability_observer,
        CapabilityAvailabilityObserver,
    )


def test_compatibility_factory_forwards_rfc049_inputs() -> None:
    source = RecordingSource(
        "deployment-capability",
        "deployment-source",
    )
    policy = configured_policy("deployment-capability")

    platform = build_platform_composition(
        capability_availability_sources=(source,),
        mandatory_capability_policy=policy,
    )

    assert platform.availability_observer._sources == (source,)
    assert platform.mandatory_capability_policy is policy
    assert platform.mandatory_capability_coverage_evaluator._policy is policy


def test_composition_exposes_single_observer_and_policy_instances() -> None:
    source = RecordingSource(
        "deployment-capability",
        "deployment-source",
    )
    policy = configured_policy("deployment-capability")

    platform = CompositionRoot.build(
        capability_availability_sources=(source,),
        mandatory_capability_policy=policy,
    )

    assert (
        platform.container.resolve(CapabilityAvailabilityObserver)
        is platform.availability_observer
    )
    assert (
        platform.container.resolve(MandatoryCapabilityPolicy)
        is platform.mandatory_capability_policy
    )
    assert (
        platform.container.resolve(MandatoryCapabilityCoverageEvaluator)
        is platform.mandatory_capability_coverage_evaluator
    )
