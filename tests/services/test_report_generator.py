from datetime import datetime, timezone

from app.domain.observation import Observation, ObservationType
from app.services.reasoning.report import ReasoningReport
from app.services.reasoning.report_generator import ReportGenerator


def make_observation(index: int) -> Observation:
    return Observation(
        source="PI System",
        observation_type=ObservationType.PROCESS,
        value=f"Observation {index}",
        observed_at=datetime.now(timezone.utc),
    )


def test_report_generator_creates_report() -> None:
    report = ReportGenerator().generate(
        tuple(make_observation(i) for i in range(5))
    )

    assert isinstance(report, ReasoningReport)
    assert report.result.recommendation.title == (
        "Review engineering decision"
    )
    assert report.explanation.title == (
        "PlantMind Engineering Analysis"
    )


def test_report_generator_accepts_empty_observations() -> None:
    report = ReportGenerator().generate(())

    assert report.result.context.observations == ()
    assert report.result.context.evidence == ()
