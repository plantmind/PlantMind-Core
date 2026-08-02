import pytest

from app.domain.context import EngineeringContext
from app.domain.judgment import JudgmentLevel
from app.domain.risk_assessment import RiskAssessment, RiskLevel
from app.services.reasoning.builders.judgment_builder import JudgmentBuilder


@pytest.mark.parametrize(
    ("risk_level", "risk_score", "expected_level", "expected_confidence"),
    [
        (RiskLevel.LOW, 0.10, JudgmentLevel.NORMAL, 0.50),
        (RiskLevel.MEDIUM, 0.40, JudgmentLevel.CAUTION, 0.60),
        (RiskLevel.HIGH, 0.70, JudgmentLevel.WARNING, 0.90),
        (RiskLevel.CRITICAL, 0.90, JudgmentLevel.CRITICAL, 1.00),
    ],
)
def test_build_maps_risk_to_judgment(
    risk_level: RiskLevel,
    risk_score: float,
    expected_level: JudgmentLevel,
    expected_confidence: float,
) -> None:
    context = EngineeringContext()

    risk = RiskAssessment(
        context=context,
        level=risk_level,
        score=risk_score,
        rationale="Test risk assessment.",
    )

    judgment = JudgmentBuilder().build(
        context,
        risk,
    )

    assert judgment.level is expected_level
    assert judgment.confidence == pytest.approx(expected_confidence)
    assert risk_level.value in judgment.summary


def test_build_preserves_context() -> None:
    context = EngineeringContext()

    risk = RiskAssessment(
        context=context,
        level=RiskLevel.MEDIUM,
        score=0.40,
        rationale="Test risk assessment.",
    )

    judgment = JudgmentBuilder().build(
        context,
        risk,
    )

    assert judgment.context is context