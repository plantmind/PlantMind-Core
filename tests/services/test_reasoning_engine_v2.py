from datetime import datetime, timezone

from app.domain.judgment import JudgmentLevel
from app.domain.observation import Observation, ObservationType
from app.domain.risk_assessment import RiskLevel
from app.services.reasoning.reasoning_engine import ReasoningEngine


def make_observation(index: int) -> Observation:
    return Observation(
        source="PI System",
        observation_type=ObservationType.PROCESS,
        value=f"Observation {index}",
        observed_at=datetime.now(timezone.utc),
    )


def test_reasoning_engine_executes_full_pipeline() -> None:
    engine = ReasoningEngine()

    conclusion = engine.reason(
        tuple(make_observation(i) for i in range(5))
    )

    assert conclusion.judgment.level is JudgmentLevel.WARNING
    assert conclusion.judgment.context.evidence
    assert len(conclusion.judgment.context.evidence) == 5


def test_reasoning_engine_builds_low_risk_for_empty_input() -> None:
    engine = ReasoningEngine()

    context = engine.build_context(())
    risk = engine.assess_risk(context)

    assert risk.level is RiskLevel.LOW
    assert risk.score == 0.10