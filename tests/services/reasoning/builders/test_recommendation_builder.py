from app.domain.context import EngineeringContext
from app.domain.decision import Decision, DecisionType
from app.domain.judgment import Judgment, JudgmentLevel
from app.domain.recommendation import RecommendationPriority
from app.services.reasoning.builders.recommendation_builder import (
    RecommendationBuilder,
)


def make_decision() -> Decision:
    judgment = Judgment(
        context=EngineeringContext(),
        level=JudgmentLevel.WARNING,
        summary="Engineering investigation is required.",
        confidence=0.90,
    )

    return Decision(
        judgment=judgment,
        decision_type=DecisionType.INVESTIGATE,
        rationale="Investigate abnormal operating conditions.",
    )


def test_build_creates_recommendation() -> None:
    recommendation = RecommendationBuilder().build(
        make_decision(),
    )

    assert recommendation.priority is RecommendationPriority.MEDIUM
    assert recommendation.title == "Review engineering decision"
    assert recommendation.description == (
        "Investigate abnormal operating conditions."
    )


def test_build_accepts_custom_priority() -> None:
    recommendation = RecommendationBuilder().build(
        make_decision(),
        priority=RecommendationPriority.HIGH,
    )

    assert recommendation.priority is RecommendationPriority.HIGH