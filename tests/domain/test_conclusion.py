import pytest

from app.domain.conclusion import Conclusion
from app.domain.context import EngineeringContext
from app.domain.judgment import Judgment, JudgmentLevel


def make_judgment() -> Judgment:
    return Judgment(
        context=EngineeringContext(),
        level=JudgmentLevel.WARNING,
        summary="Discharge pressure requires engineering attention.",
        confidence=0.90,
    )


def test_valid_conclusion() -> None:
    conclusion = Conclusion(
        judgment=make_judgment(),
        summary="The compressor discharge condition is abnormal.",
    )

    assert conclusion.judgment.level is JudgmentLevel.WARNING


def test_empty_summary_is_rejected() -> None:
    with pytest.raises(ValueError):
        Conclusion(
            judgment=make_judgment(),
            summary="   ",
        )