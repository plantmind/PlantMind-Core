from app.services.reasoning.presentation import (
    PresentationSection,
    ReasoningPresentation,
)
from app.services.reasoning.report_presenter import ReportPresenter


def test_report_presenter_returns_api_ready_dictionary() -> None:
    presentation = ReasoningPresentation(
        title="Engineering Analysis",
        summary="Review required.",
        risk_level="high",
        decision="Investigate.",
        recommendation="Review engineering decision",
        sections=(
            PresentationSection(
                heading="Evidence",
                items=("Pressure increased.",),
            ),
        ),
    )

    payload = ReportPresenter().present(presentation)

    assert payload["risk_level"] == "high"
    assert payload["sections"] == [
        {
            "heading": "Evidence",
            "items": ["Pressure increased."],
        }
    ]
