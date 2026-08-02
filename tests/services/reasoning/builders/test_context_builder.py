from datetime import datetime, timezone

from app.domain.evidence import EvidenceType
from app.domain.observation import Observation, ObservationType
from app.services.reasoning.builders.context_builder import ContextBuilder


def make_observation(
    observation_type: ObservationType,
    value: str,
) -> Observation:
    return Observation(
        source="PI System",
        observation_type=observation_type,
        value=value,
        observed_at=datetime.now(timezone.utc),
    )


def test_build_creates_context_with_observations_and_evidence() -> None:
    builder = ContextBuilder()

    observations = (
        make_observation(
            ObservationType.PROCESS,
            "Discharge pressure increased.",
        ),
        make_observation(
            ObservationType.ALARM,
            "PAHH-1001 active.",
        ),
    )

    context = builder.build(observations)

    assert context.observations == observations
    assert len(context.evidence) == 2
    assert context.evidence[0].evidence_type is EvidenceType.PROCESS
    assert context.evidence[1].evidence_type is EvidenceType.ALARM


def test_build_preserves_observation_order() -> None:
    builder = ContextBuilder()

    observations = (
        make_observation(
            ObservationType.MAINTENANCE,
            "Open work order exists.",
        ),
        make_observation(
            ObservationType.OPERATOR,
            "Operator reported abnormal vibration.",
        ),
    )

    context = builder.build(observations)

    assert context.observations == observations
    assert context.evidence[0].description == "Open work order exists."
    assert (
        context.evidence[1].description
        == "Operator reported abnormal vibration."
    )


def test_build_accepts_empty_observations() -> None:
    builder = ContextBuilder()

    context = builder.build(())

    assert context.observations == ()
    assert context.evidence == ()