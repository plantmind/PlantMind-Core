import pytest

from app.domain.context import EngineeringContext
from app.domain.risk_assessment import RiskAssessment, RiskLevel


def test_valid_risk_assessment() -> None:
    assessment = RiskAssessment(
        context=EngineeringContext(),
        level=RiskLevel.HIGH,
        score=0.85,
        rationale="Active alarms and degraded equipment condition.",
    )

    assert assessment.level is RiskLevel.HIGH
    assert assessment.score == 0.85


@pytest.mark.parametrize("score", [-0.01, 1.01])
def test_invalid_score_is_rejected(score: float) -> None:
    with pytest.raises(ValueError):
        RiskAssessment(
            context=EngineeringContext(),
            level=RiskLevel.CRITICAL,
            score=score,
            rationale="Critical operational risk.",
        )


def test_empty_rationale_is_rejected() -> None:
    with pytest.raises(ValueError):
        RiskAssessment(
            context=EngineeringContext(),
            level=RiskLevel.MEDIUM,
            score=0.50,
            rationale="   ",
        )