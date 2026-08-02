from app.domain.conclusion import Conclusion
from app.domain.context import EngineeringContext
from app.domain.decision import DecisionType
from app.domain.judgment import Judgment, JudgmentLevel
from app.services.reasoning.builders.decision_builder import DecisionBuilder


def make_conclusion() -> Conclusion:
    judgment = Judgment(
        context=EngineeringContext(),
        level=JudgmentLevel.WARNING,
        summary="Engineering investigation is required.",
        confidence=0.90,
    )

    return Conclusion(
        judgment=judgment,
        summary=judgment.summary,
    )


def test_build_creates_decision() -> None:
    decision = DecisionBuilder().build(
        make_conclusion(),
    )

    assert decision.decision_type is DecisionType.INVESTIGATE
    assert decision.rationale == "Engineering investigation is required."
    assert decision.judgment.level is JudgmentLevel.WARNING