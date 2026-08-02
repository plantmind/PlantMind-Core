from datetime import datetime, timezone

from app.domain.observation import Observation, ObservationType
from app.domain.recommendation import Recommendation
from app.services.reasoning.pipeline import ReasoningPipeline


def make_observation(index: int) -> Observation:
    return Observation(
        source="PI System",
        observation_type=ObservationType.PROCESS,
        value=f"Observation {index}",
        observed_at=datetime.now(timezone.utc),
    )


def test_pipeline_returns_recommendation() -> None:
    recommendation = ReasoningPipeline().run(
        tuple(make_observation(i) for i in range(5))
    )

    assert isinstance(recommendation, Recommendation)
    assert recommendation.title == "Review engineering decision"
    assert recommendation.description