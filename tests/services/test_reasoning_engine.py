from app.domain.context import EngineeringContext
from app.domain.judgment import JudgmentLevel
from app.domain.risk_assessment import RiskLevel
from app.services.reasoning.reasoning_engine import ReasoningEngine


def test_reasoning_engine_produces_conclusion() -> None:
    engine = ReasoningEngine()

    conclusion = engine.conclude(
        EngineeringContext(),
    )

    assert conclusion.judgment.level is JudgmentLevel.NORMAL
    assert conclusion.judgment.confidence == 0.50


def test_reasoning_engine_produces_baseline_risk() -> None:
    engine = ReasoningEngine()

    risk = engine.assess_risk(
        EngineeringContext(),
    )

    assert risk.level is RiskLevel.LOW
    assert risk.score == 0.10