"""PlantMind Engineering Reasoning Pipeline."""

from __future__ import annotations

from app.domain.observation import Observation
from app.domain.recommendation import Recommendation
from app.services.reasoning.builders.conclusion_builder import ConclusionBuilder
from app.services.reasoning.builders.context_builder import ContextBuilder
from app.services.reasoning.builders.decision_builder import DecisionBuilder
from app.services.reasoning.builders.judgment_builder import JudgmentBuilder
from app.services.reasoning.builders.recommendation_builder import (
    RecommendationBuilder,
)
from app.services.reasoning.builders.risk_builder import RiskBuilder
from app.services.reasoning.result import ReasoningResult


class ReasoningPipeline:
    """Execute the complete engineering reasoning workflow."""

    def __init__(self) -> None:
        self._context_builder = ContextBuilder()
        self._risk_builder = RiskBuilder()
        self._judgment_builder = JudgmentBuilder()
        self._conclusion_builder = ConclusionBuilder()
        self._decision_builder = DecisionBuilder()
        self._recommendation_builder = RecommendationBuilder()

    def run_result(
        self,
        observations: tuple[Observation, ...],
    ) -> ReasoningResult:
        """Execute the workflow once and return its complete result."""
        context = self._context_builder.build(observations)
        risk = self._risk_builder.build(context)

        judgment = self._judgment_builder.build(
            context,
            risk,
        )

        conclusion = self._conclusion_builder.build(judgment)
        decision = self._decision_builder.build(conclusion)
        recommendation = self._recommendation_builder.build(decision)

        return ReasoningResult(
            context=context,
            risk=risk,
            judgment=judgment,
            conclusion=conclusion,
            decision=decision,
            recommendation=recommendation,
        )

    def run(
        self,
        observations: tuple[Observation, ...],
    ) -> Recommendation:
        """Preserve the existing recommendation-only interface."""
        return self.run_result(observations).recommendation