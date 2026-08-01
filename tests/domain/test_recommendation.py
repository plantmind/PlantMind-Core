import pytest

from app.domain.context import EngineeringContext
from app.domain.decision import Decision, DecisionType
from app.domain.judgment import Judgment, JudgmentLevel
from app.domain.recommendation import (
    Recommendation,
    RecommendationPriority,
)


def make_decision() -> Decision:
    judgment = Judgment(
        context=EngineeringContext(),
        level=JudgmentLevel.WARNING,
        summary="Discharge pressure requires engineering attention.",
        confidence=0.90,
    )

    return Decision(
        judgment=judgment,
        decision_type=DecisionType.INVESTIGATE,
        rationale="Investigate compressor discharge condition.",
    )


def test_valid_recommendation() -> None:
    recommendation = Recommendation(
        decision=make_decision(),
        priority=RecommendationPriority.HIGH,
        title="Inspect compressor discharge condition",
        description="Authorized personnel should inspect COMP-H-001.",
    )

    assert recommendation.priority is RecommendationPriority.HIGH


@pytest.mark.parametrize(
    ("title", "description"),
    [
        ("   ", "Inspect the compressor."),
        ("Inspect compressor", "   "),
    ],
)
def test_empty_text_is_rejected(
    title: str,
    description: str,
) -> None:
    with pytest.raises(ValueError):
        Recommendation(
            decision=make_decision(),
            priority=RecommendationPriority.HIGH,
            title=title,
            description=description,
        )