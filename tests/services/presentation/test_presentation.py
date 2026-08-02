import pytest

from app.services.reasoning.presentation import (
    PresentationSection,
    ReasoningPresentation,
)


def test_presentation_models_are_immutable_and_normalized() -> None:
    section = PresentationSection(
        heading="  Evidence  ",
        items=["Pressure increased."],
    )

    presentation = ReasoningPresentation(
        title="Engineering Analysis",
        summary="Review required.",
        risk_level="high",
        decision="Investigate.",
        recommendation="Review engineering decision",
        sections=[section],
    )

    assert section.heading == "Evidence"
    assert section.items == ("Pressure increased.",)
    assert presentation.sections == (section,)


@pytest.mark.parametrize(
    "field_name",
    [
        "title",
        "summary",
        "risk_level",
        "decision",
        "recommendation",
    ],
)
def test_presentation_rejects_empty_required_fields(
    field_name: str,
) -> None:
    values = {
        "title": "Engineering Analysis",
        "summary": "Review required.",
        "risk_level": "high",
        "decision": "Investigate.",
        "recommendation": "Review engineering decision",
    }
    values[field_name] = "   "

    with pytest.raises(ValueError):
        ReasoningPresentation(**values)
