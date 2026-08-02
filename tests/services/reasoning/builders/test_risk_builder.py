from datetime import datetime, timezone

from app.domain.observation import Observation, ObservationType
from app.services.reasoning.builders.context_builder import ContextBuilder
from app.services.reasoning.builders.risk_builder import RiskBuilder
from app.domain.risk_assessment import RiskLevel


def make_observation(index: int) -> Observation:
    return Observation(
        source="PI System",
        observation_type=ObservationType.PROCESS,
        value=f"Observation {index}",
        observed_at=datetime.now(timezone.utc),
    )


def test_empty_context_produces_low_risk() -> None:
    builder = RiskBuilder()

    context = ContextBuilder().build(())

    risk = builder.build(context)

    assert risk.level is RiskLevel.LOW
    assert risk.score == 0.10


def test_three_evidence_items_produce_medium_risk() -> None:
    builder = RiskBuilder()

    context = ContextBuilder().build(
        tuple(make_observation(i) for i in range(3))
    )

    risk = builder.build(context)

    assert risk.level is RiskLevel.MEDIUM
    assert risk.score == 0.40


def test_seven_evidence_items_produce_critical_risk() -> None:
    builder = RiskBuilder()

    context = ContextBuilder().build(
        tuple(make_observation(i) for i in range(7))
    )

    risk = builder.build(context)

    assert risk.level is RiskLevel.CRITICAL
    assert risk.score == 0.80