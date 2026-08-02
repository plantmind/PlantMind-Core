from app.services.reasoning.explanation import Explanation


def test_explanation_model() -> None:
    explanation = Explanation(
        title="Engineering Analysis",
        summary="Operating conditions require investigation.",
        details=(
            "Evidence collected from PI System.",
            "Risk level assessed as HIGH.",
            "Recommendation generated.",
        ),
    )

    assert explanation.title == "Engineering Analysis"
    assert explanation.summary == "Operating conditions require investigation."
    assert len(explanation.details) == 3
    assert explanation.details[0] == "Evidence collected from PI System."