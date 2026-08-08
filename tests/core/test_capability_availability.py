from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone

import pytest

from app.core.availability import (
    CapabilityAvailabilityObservation,
    CapabilityAvailabilityObserver,
    CapabilityAvailabilitySource,
    CapabilityAvailabilityState,
)
from app.core.composition import CompositionRoot


class StaticAvailabilitySource(CapabilityAvailabilitySource):
    def __init__(
        self,
        capability_name: str,
        source_name: str,
        state: CapabilityAvailabilityState,
    ) -> None:
        self._capability_name = capability_name
        self._source_name = source_name
        self._state = state

    @property
    def capability_name(self) -> str:
        return self._capability_name

    @property
    def source_name(self) -> str:
        return self._source_name

    def observe(self) -> CapabilityAvailabilityObservation:
        return CapabilityAvailabilityObservation(
            capability_name=self.capability_name,
            state=self._state,
            observed_at=datetime.now(UTC),
            source_name=self.source_name,
        )


class FailingAvailabilitySource(CapabilityAvailabilitySource):
    @property
    def capability_name(self) -> str:
        return "pi-system"

    @property
    def source_name(self) -> str:
        return "pi-health-probe"

    def observe(self) -> CapabilityAvailabilityObservation:
        raise RuntimeError("probe failed")


def test_availability_state_has_required_semantics() -> None:
    assert CapabilityAvailabilityState.AVAILABLE.value == "available"
    assert CapabilityAvailabilityState.UNAVAILABLE.value == "unavailable"
    assert CapabilityAvailabilityState.UNKNOWN.value == "unknown"


def test_availability_observation_is_immutable() -> None:
    observation = CapabilityAvailabilityObservation(
        capability_name="pi-system",
        state=CapabilityAvailabilityState.AVAILABLE,
        observed_at=datetime.now(UTC),
        source_name="pi-health-probe",
    )

    with pytest.raises(FrozenInstanceError):
        observation.state = CapabilityAvailabilityState.UNAVAILABLE


@pytest.mark.parametrize(
    ("capability_name", "source_name"),
    [
        ("", "source"),
        ("   ", "source"),
        ("capability", ""),
        ("capability", "   "),
    ],
)
def test_availability_observation_requires_non_empty_identities(
    capability_name: str,
    source_name: str,
) -> None:
    with pytest.raises(ValueError):
        CapabilityAvailabilityObservation(
            capability_name=capability_name,
            state=CapabilityAvailabilityState.UNKNOWN,
            observed_at=datetime.now(UTC),
            source_name=source_name,
        )


def test_availability_observation_rejects_naive_timestamp() -> None:
    with pytest.raises(ValueError):
        CapabilityAvailabilityObservation(
            capability_name="pi-system",
            state=CapabilityAvailabilityState.AVAILABLE,
            observed_at=datetime.now(),
            source_name="pi-health-probe",
        )


def test_availability_observation_normalizes_timestamp_to_utc() -> None:
    observed_at = datetime(
        2026,
        8,
        8,
        15,
        0,
        tzinfo=timezone(timedelta(hours=3)),
    )

    observation = CapabilityAvailabilityObservation(
        capability_name="pi-system",
        state=CapabilityAvailabilityState.AVAILABLE,
        observed_at=observed_at,
        source_name="pi-health-probe",
    )

    assert observation.observed_at.tzinfo is UTC
    assert observation.observed_at.hour == 12


def test_observer_preserves_explicit_source_order() -> None:
    observer = CapabilityAvailabilityObserver(
        sources=(
            StaticAvailabilitySource(
                "pi-system",
                "pi-health-probe",
                CapabilityAvailabilityState.AVAILABLE,
            ),
            StaticAvailabilitySource(
                "ai-model",
                "model-health-probe",
                CapabilityAvailabilityState.UNAVAILABLE,
            ),
        )
    )

    observations = observer.observe_all()

    assert tuple(item.capability_name for item in observations) == (
        "pi-system",
        "ai-model",
    )


def test_observer_returns_successful_source_observation() -> None:
    observer = CapabilityAvailabilityObserver(
        sources=(
            StaticAvailabilitySource(
                "pi-system",
                "pi-health-probe",
                CapabilityAvailabilityState.AVAILABLE,
            ),
        )
    )

    observations = observer.observe_all()

    assert len(observations) == 1
    assert observations[0].state is CapabilityAvailabilityState.AVAILABLE
    assert observations[0].source_name == "pi-health-probe"


def test_source_failure_maps_to_unknown() -> None:
    observer = CapabilityAvailabilityObserver(
        sources=(FailingAvailabilitySource(),)
    )

    observations = observer.observe_all()

    assert len(observations) == 1
    assert observations[0].capability_name == "pi-system"
    assert observations[0].source_name == "pi-health-probe"
    assert observations[0].state is CapabilityAvailabilityState.UNKNOWN
    assert observations[0].observed_at.tzinfo is UTC


def test_source_failure_does_not_prevent_other_observations() -> None:
    observer = CapabilityAvailabilityObserver(
        sources=(
            FailingAvailabilitySource(),
            StaticAvailabilitySource(
                "ai-model",
                "model-health-probe",
                CapabilityAvailabilityState.AVAILABLE,
            ),
        )
    )

    observations = observer.observe_all()

    assert len(observations) == 2
    assert observations[0].state is CapabilityAvailabilityState.UNKNOWN
    assert observations[1].state is CapabilityAvailabilityState.AVAILABLE


def test_observer_with_no_sources_produces_no_evidence() -> None:
    observer = CapabilityAvailabilityObserver(sources=())

    assert observer.observe_all() == ()


def test_composition_exposes_single_availability_observer() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.container.resolve(CapabilityAvailabilityObserver)
        is platform.availability_observer
    )


def test_observation_does_not_modify_runtime_lifecycle_or_admission() -> None:
    platform = CompositionRoot.build()
    platform.runtime.mark_ready()
    platform.runtime.enable_request_admission()

    initial_state = platform.runtime.state
    initial_admission = platform.runtime.is_request_admission_enabled

    platform.availability_observer.observe_all()

    assert platform.runtime.state is initial_state
    assert platform.runtime.is_request_admission_enabled is initial_admission
