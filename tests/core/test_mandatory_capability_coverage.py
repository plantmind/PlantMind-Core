from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from app.core.availability import (
    CapabilityAvailabilityObservation,
    CapabilityAvailabilityState,
)
from app.core.capability_coverage import (
    MandatoryCapabilityCoverageEvaluator,
    MandatoryCapabilityCoverageResult,
    MandatoryCapabilityCoverageState,
)
from app.core.capability_policy import (
    MandatoryCapabilityPolicy,
    MandatoryCapabilityPolicyState,
)
from app.core.composition import CompositionRoot


def make_observation(
    capability_name: str,
    state: CapabilityAvailabilityState,
    source_name: str | None = None,
) -> CapabilityAvailabilityObservation:
    return CapabilityAvailabilityObservation(
        capability_name=capability_name,
        state=state,
        observed_at=datetime.now(UTC),
        source_name=source_name or f"{capability_name}-source",
    )


def configured_policy(
    *capabilities: str,
) -> MandatoryCapabilityPolicy:
    return MandatoryCapabilityPolicy(
        state=MandatoryCapabilityPolicyState.CONFIGURED,
        required_capabilities=capabilities,
    )


def test_coverage_state_has_exact_semantics() -> None:
    assert MandatoryCapabilityCoverageState.SATISFIED.value == "satisfied"
    assert MandatoryCapabilityCoverageState.UNSATISFIED.value == "unsatisfied"


def test_coverage_result_is_immutable() -> None:
    result = MandatoryCapabilityCoverageResult(
        state=MandatoryCapabilityCoverageState.SATISFIED,
        required_capabilities=("pi-system",),
        satisfied_capabilities=("pi-system",),
        missing_capabilities=(),
        unavailable_capabilities=(),
        unknown_capabilities=(),
        ambiguous_capabilities=(),
    )

    with pytest.raises(FrozenInstanceError):
        result.state = MandatoryCapabilityCoverageState.UNSATISFIED


def test_unconfigured_policy_fails_closed() -> None:
    policy = MandatoryCapabilityPolicy(
        state=MandatoryCapabilityPolicyState.UNCONFIGURED,
        required_capabilities=(),
    )
    evaluator = MandatoryCapabilityCoverageEvaluator(policy)

    result = evaluator.evaluate(
        (
            make_observation(
                "pi-system",
                CapabilityAvailabilityState.AVAILABLE,
            ),
        )
    )

    assert result.state is MandatoryCapabilityCoverageState.UNSATISFIED
    assert result.required_capabilities == ()
    assert result.satisfied_capabilities == ()
    assert result.missing_capabilities == ()
    assert result.unavailable_capabilities == ()
    assert result.unknown_capabilities == ()
    assert result.ambiguous_capabilities == ()


def test_all_required_available_is_satisfied() -> None:
    policy = configured_policy("pi-system", "ai-model")
    evaluator = MandatoryCapabilityCoverageEvaluator(policy)

    result = evaluator.evaluate(
        (
            make_observation(
                "pi-system",
                CapabilityAvailabilityState.AVAILABLE,
            ),
            make_observation(
                "ai-model",
                CapabilityAvailabilityState.AVAILABLE,
            ),
        )
    )

    assert result.state is MandatoryCapabilityCoverageState.SATISFIED
    assert result.required_capabilities == ("pi-system", "ai-model")
    assert result.satisfied_capabilities == ("pi-system", "ai-model")
    assert result.missing_capabilities == ()
    assert result.unavailable_capabilities == ()
    assert result.unknown_capabilities == ()
    assert result.ambiguous_capabilities == ()


def test_missing_required_capability_fails_closed() -> None:
    evaluator = MandatoryCapabilityCoverageEvaluator(
        configured_policy("pi-system", "ai-model")
    )

    result = evaluator.evaluate(
        (
            make_observation(
                "pi-system",
                CapabilityAvailabilityState.AVAILABLE,
            ),
        )
    )

    assert result.state is MandatoryCapabilityCoverageState.UNSATISFIED
    assert result.satisfied_capabilities == ("pi-system",)
    assert result.missing_capabilities == ("ai-model",)


def test_unavailable_required_capability_fails_closed() -> None:
    evaluator = MandatoryCapabilityCoverageEvaluator(
        configured_policy("pi-system")
    )

    result = evaluator.evaluate(
        (
            make_observation(
                "pi-system",
                CapabilityAvailabilityState.UNAVAILABLE,
            ),
        )
    )

    assert result.state is MandatoryCapabilityCoverageState.UNSATISFIED
    assert result.unavailable_capabilities == ("pi-system",)


def test_unknown_required_capability_fails_closed() -> None:
    evaluator = MandatoryCapabilityCoverageEvaluator(
        configured_policy("pi-system")
    )

    result = evaluator.evaluate(
        (
            make_observation(
                "pi-system",
                CapabilityAvailabilityState.UNKNOWN,
            ),
        )
    )

    assert result.state is MandatoryCapabilityCoverageState.UNSATISFIED
    assert result.unknown_capabilities == ("pi-system",)


def test_multiple_observations_for_required_capability_are_ambiguous() -> None:
    evaluator = MandatoryCapabilityCoverageEvaluator(
        configured_policy("pi-system")
    )

    result = evaluator.evaluate(
        (
            make_observation(
                "pi-system",
                CapabilityAvailabilityState.AVAILABLE,
                "source-a",
            ),
            make_observation(
                "pi-system",
                CapabilityAvailabilityState.AVAILABLE,
                "source-b",
            ),
        )
    )

    assert result.state is MandatoryCapabilityCoverageState.UNSATISFIED
    assert result.ambiguous_capabilities == ("pi-system",)
    assert result.satisfied_capabilities == ()


def test_non_required_observations_do_not_affect_coverage() -> None:
    evaluator = MandatoryCapabilityCoverageEvaluator(
        configured_policy("pi-system")
    )

    result = evaluator.evaluate(
        (
            make_observation(
                "pi-system",
                CapabilityAvailabilityState.AVAILABLE,
            ),
            make_observation(
                "ai-model",
                CapabilityAvailabilityState.UNAVAILABLE,
            ),
        )
    )

    assert result.state is MandatoryCapabilityCoverageState.SATISFIED
    assert result.satisfied_capabilities == ("pi-system",)
    assert result.unavailable_capabilities == ()


def test_diagnostic_order_preserves_policy_requirement_order() -> None:
    evaluator = MandatoryCapabilityCoverageEvaluator(
        configured_policy(
            "knowledge-store",
            "pi-system",
            "ai-model",
        )
    )

    result = evaluator.evaluate(())

    assert result.required_capabilities == (
        "knowledge-store",
        "pi-system",
        "ai-model",
    )
    assert result.missing_capabilities == (
        "knowledge-store",
        "pi-system",
        "ai-model",
    )


def test_each_required_capability_receives_one_classification() -> None:
    evaluator = MandatoryCapabilityCoverageEvaluator(
        configured_policy(
            "available-capability",
            "missing-capability",
            "unavailable-capability",
            "unknown-capability",
            "ambiguous-capability",
        )
    )

    result = evaluator.evaluate(
        (
            make_observation(
                "available-capability",
                CapabilityAvailabilityState.AVAILABLE,
            ),
            make_observation(
                "unavailable-capability",
                CapabilityAvailabilityState.UNAVAILABLE,
            ),
            make_observation(
                "unknown-capability",
                CapabilityAvailabilityState.UNKNOWN,
            ),
            make_observation(
                "ambiguous-capability",
                CapabilityAvailabilityState.AVAILABLE,
                "source-a",
            ),
            make_observation(
                "ambiguous-capability",
                CapabilityAvailabilityState.UNAVAILABLE,
                "source-b",
            ),
        )
    )

    classified = (
        result.satisfied_capabilities
        + result.missing_capabilities
        + result.unavailable_capabilities
        + result.unknown_capabilities
        + result.ambiguous_capabilities
    )

    assert len(classified) == len(result.required_capabilities)
    assert set(classified) == set(result.required_capabilities)


def test_evaluator_uses_exact_policy_instance() -> None:
    policy = configured_policy("pi-system")

    evaluator = MandatoryCapabilityCoverageEvaluator(policy)

    assert evaluator._policy is policy


def test_composition_exposes_same_coverage_evaluator() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.container.resolve(MandatoryCapabilityCoverageEvaluator)
        is platform.mandatory_capability_coverage_evaluator
    )


def test_composed_evaluator_uses_composed_policy() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.mandatory_capability_coverage_evaluator._policy
        is platform.mandatory_capability_policy
    )


def test_evaluation_does_not_modify_runtime_or_request_admission() -> None:
    platform = CompositionRoot.build()
    platform.runtime.mark_ready()
    platform.runtime.enable_request_admission()

    initial_state = platform.runtime.state
    initial_admission = platform.runtime.is_request_admission_enabled

    platform.mandatory_capability_coverage_evaluator.evaluate(())

    assert platform.runtime.state is initial_state
    assert platform.runtime.is_request_admission_enabled is initial_admission


def test_evaluation_does_not_modify_policy_or_availability_observer() -> None:
    platform = CompositionRoot.build()

    policy = platform.mandatory_capability_policy
    initial_state = policy.state
    initial_requirements = policy.required_capabilities

    observer = platform.availability_observer
    initial_sources = observer._sources

    platform.mandatory_capability_coverage_evaluator.evaluate(
        observer.observe_all()
    )

    assert platform.mandatory_capability_policy is policy
    assert policy.state is initial_state
    assert policy.required_capabilities is initial_requirements
    assert platform.availability_observer is observer
    assert observer._sources is initial_sources
