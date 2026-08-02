from datetime import datetime, timezone

from app.domain.conclusion import Conclusion
from app.domain.observation import Observation, ObservationType
from app.services.reasoning.builders.conclusion_builder import ConclusionBuilder
from app.services.reasoning.builders.context_builder import ContextBuilder
from app.services.reasoning.builders.judgment_builder import JudgmentBuilder
from app.services.reasoning.builders.risk_builder import RiskBuilder


def make_observation(index: int) -> Observation:
    return Observation(
        source="PI System",
        observation_type=ObservationType.PROCESS,
        value=f"Observation {index}",
        observed_at=datetime.now(timezone.utc),
    )


def test_complete_reasoning_pipeline() -> None:
    observations = tuple(
        make_observation(i)
        for i in range(5)
    )

    context = ContextBuilder().build(observations)

    risk = RiskBuilder().build(context)

    judgment = JudgmentBuilder().build(
        context,
        risk,
    )

    conclusion = ConclusionBuilder().build(
        judgment,
    )

    assert isinstance(conclusion, Conclusion)
    assert conclusion.judgment is judgment
    assert conclusion.summary == judgment.summary
    assert len(context.evidence) == 5