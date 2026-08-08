from dataclasses import FrozenInstanceError

import pytest

from app.core.availability import CapabilityAvailabilityObserver
from app.core.capability_policy import (
    MandatoryCapabilityPolicy,
    MandatoryCapabilityPolicyState,
)
from app.core.composition import CompositionRoot


def test_policy_state_has_exact_semantics() -> None:
    assert MandatoryCapabilityPolicyState.UNCONFIGURED.value == "unconfigured"
    assert MandatoryCapabilityPolicyState.CONFIGURED.value == "configured"


def test_policy_is_immutable() -> None:
    policy = MandatoryCapabilityPolicy(
        state=MandatoryCapabilityPolicyState.CONFIGURED,
        required_capabilities=("pi-system",),
    )

    with pytest.raises(FrozenInstanceError):
        policy.state = MandatoryCapabilityPolicyState.UNCONFIGURED


def test_unconfigured_policy_requires_empty_requirements() -> None:
    with pytest.raises(ValueError):
        MandatoryCapabilityPolicy(
            state=MandatoryCapabilityPolicyState.UNCONFIGURED,
            required_capabilities=("pi-system",),
        )


def test_configured_policy_requires_at_least_one_requirement() -> None:
    with pytest.raises(ValueError):
        MandatoryCapabilityPolicy(
            state=MandatoryCapabilityPolicyState.CONFIGURED,
            required_capabilities=(),
        )


@pytest.mark.parametrize(
    "capability_name",
    [
        "",
        "   ",
    ],
)
def test_policy_rejects_empty_capability_identifiers(
    capability_name: str,
) -> None:
    with pytest.raises(ValueError):
        MandatoryCapabilityPolicy(
            state=MandatoryCapabilityPolicyState.CONFIGURED,
            required_capabilities=(capability_name,),
        )


@pytest.mark.parametrize(
    "capability_name",
    [
        " pi-system",
        "pi-system ",
        " pi-system ",
    ],
)
def test_policy_rejects_leading_or_trailing_whitespace(
    capability_name: str,
) -> None:
    with pytest.raises(ValueError):
        MandatoryCapabilityPolicy(
            state=MandatoryCapabilityPolicyState.CONFIGURED,
            required_capabilities=(capability_name,),
        )


def test_policy_rejects_duplicate_capabilities() -> None:
    with pytest.raises(ValueError):
        MandatoryCapabilityPolicy(
            state=MandatoryCapabilityPolicyState.CONFIGURED,
            required_capabilities=(
                "pi-system",
                "ai-model",
                "pi-system",
            ),
        )


def test_policy_preserves_explicit_requirement_order() -> None:
    policy = MandatoryCapabilityPolicy(
        state=MandatoryCapabilityPolicyState.CONFIGURED,
        required_capabilities=(
            "pi-system",
            "ai-model",
            "knowledge-store",
        ),
    )

    assert policy.required_capabilities == (
        "pi-system",
        "ai-model",
        "knowledge-store",
    )


def test_composition_exposes_explicit_unconfigured_policy() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.mandatory_capability_policy.state
        is MandatoryCapabilityPolicyState.UNCONFIGURED
    )
    assert platform.mandatory_capability_policy.required_capabilities == ()


def test_container_resolves_same_composed_policy_instance() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.container.resolve(MandatoryCapabilityPolicy)
        is platform.mandatory_capability_policy
    )


def test_policy_access_does_not_modify_runtime_or_request_admission() -> None:
    platform = CompositionRoot.build()
    platform.runtime.mark_ready()
    platform.runtime.enable_request_admission()

    initial_state = platform.runtime.state
    initial_admission = platform.runtime.is_request_admission_enabled

    _ = platform.mandatory_capability_policy.required_capabilities

    assert platform.runtime.state is initial_state
    assert platform.runtime.is_request_admission_enabled is initial_admission


def test_policy_access_does_not_modify_availability_observer() -> None:
    platform = CompositionRoot.build()

    observer = platform.availability_observer
    initial_sources = observer._sources

    _ = platform.mandatory_capability_policy.required_capabilities

    assert platform.availability_observer is observer
    assert platform.availability_observer._sources is initial_sources
    assert isinstance(
        platform.availability_observer,
        CapabilityAvailabilityObserver,
    )
