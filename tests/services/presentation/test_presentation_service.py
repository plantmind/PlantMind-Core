from datetime import datetime, timezone

from app.domain.observation import Observation, ObservationType
from app.services.reasoning.presentation_service import PresentationService


def test_presentation_service_executes_complete_workflow() -> None:
    observation = Observation(
        source="PI System",
        observation_type=ObservationType.ALARM,
        value="PAHH-1001 active.",
        observed_at=datetime.now(timezone.utc),
    )

    payload = PresentationService().generate((observation,))

    assert payload["title"] == "PlantMind Engineering Analysis"
    assert payload["recommendation"] == "Review engineering decision"
    assert payload["sections"][0]["items"] == ["PAHH-1001 active."]


def test_presentation_service_accepts_empty_input() -> None:
    payload = PresentationService().generate(())

    assert payload["risk_level"] == "low"
    assert payload["sections"][0]["items"] == []
