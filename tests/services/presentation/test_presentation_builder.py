from datetime import datetime, timezone

from app.domain.observation import Observation, ObservationType
from app.services.reasoning.presentation_builder import PresentationBuilder
from app.services.reasoning.report_generator import ReportGenerator


def test_presentation_builder_maps_reasoning_report() -> None:
    observation = Observation(
        source="PI System",
        observation_type=ObservationType.PROCESS,
        value="Discharge pressure increased.",
        observed_at=datetime.now(timezone.utc),
    )

    report = ReportGenerator().generate((observation,))
    presentation = PresentationBuilder().build(report)

    assert presentation.title == "PlantMind Engineering Analysis"
    assert presentation.risk_level == report.result.risk.level.value
    assert presentation.decision == report.result.decision.rationale
    assert len(presentation.sections) == 2
    assert presentation.sections[0].items == (
        "Discharge pressure increased.",
    )
