import pytest

from app.domain.context import EngineeringContext
from app.domain.decision import Decision, DecisionType
from app.domain.judgment import Judgment, JudgmentLevel


def make_judgment() -> Judgment:
    return Judgment(
        context=EngineeringContext(),
        level=JudgmentLevel.WARNING,
        summary="Discharge pressure requires engineering attention.",
        confidence=0.90,
    )


def test_valid_decision() -> None:
    decision = Decision(
        judgment=make_judgment(),
        decision_type=DecisionType.INVESTIGATE,
        rationale="Investigate the compressor discharge condition.",
    )

    assert decision.decision_type is DecisionType.INVESTIGATE


def test_empty_rationale_is_rejected() -> None:
    with pytest.raises(ValueError):
        Decision(
            judgment=make_judgment(),
            decision_type=DecisionType.ESCALATE,
            rationale="   ",
        )