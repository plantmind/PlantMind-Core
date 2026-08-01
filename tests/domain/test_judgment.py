import pytest

from app.domain.context import EngineeringContext
from app.domain.judgment import Judgment, JudgmentLevel


def test_valid_judgment() -> None:
    judgment = Judgment(
        context=EngineeringContext(),
        level=JudgmentLevel.WARNING,
        summary="Discharge pressure requires engineering attention.",
        confidence=0.90,
    )

    assert judgment.level is JudgmentLevel.WARNING
    assert judgment.confidence == 0.90


def test_empty_summary_is_rejected() -> None:
    with pytest.raises(ValueError):
        Judgment(
            context=EngineeringContext(),
            level=JudgmentLevel.CAUTION,
            summary="   ",
            confidence=0.70,
        )


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_invalid_confidence_is_rejected(confidence: float) -> None:
    with pytest.raises(ValueError):
        Judgment(
            context=EngineeringContext(),
            level=JudgmentLevel.CRITICAL,
            summary="Critical condition detected.",
            confidence=confidence,
        )