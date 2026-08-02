from app.domain.context import EngineeringContext
from app.domain.judgment import Judgment, JudgmentLevel
from app.services.reasoning.builders.conclusion_builder import (
    ConclusionBuilder,
)


def make_judgment() -> Judgment:
    return Judgment(
        context=EngineeringContext(),
        level=JudgmentLevel.WARNING,
        summary="Engineering investigation is required.",
        confidence=0.90,
    )


def test_build_creates_conclusion() -> None:
    builder = ConclusionBuilder()

    conclusion = builder.build(
        make_judgment(),
    )

    assert conclusion.summary == "Engineering investigation is required."
    assert conclusion.judgment.level is JudgmentLevel.WARNING


def test_build_preserves_original_judgment() -> None:
    builder = ConclusionBuilder()

    judgment = make_judgment()

    conclusion = builder.build(
        judgment,
    )

    assert conclusion.judgment is judgment