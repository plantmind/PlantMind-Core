"""PlantMind Engineering Reasoning Engine."""

from __future__ import annotations

from app.domain.conclusion import Conclusion
from app.domain.context import EngineeringContext
from app.domain.judgment import Judgment
from app.domain.observation import Observation
from app.domain.risk_assessment import RiskAssessment
from app.services.reasoning.builders.conclusion_builder import ConclusionBuilder
from app.services.reasoning.builders.context_builder import ContextBuilder
from app.services.reasoning.builders.judgment_builder import JudgmentBuilder
from app.services.reasoning.builders.risk_builder import RiskBuilder


class ReasoningEngine:
    """Coordinate the PlantMind engineering reasoning pipeline."""

    def __init__(self) -> None:
        self._context_builder = ContextBuilder()
        self._risk_builder = RiskBuilder()
        self._judgment_builder = JudgmentBuilder()
        self._conclusion_builder = ConclusionBuilder()

    def build_context(
        self,
        observations: tuple[Observation, ...],
    ) -> EngineeringContext:
        return self._context_builder.build(observations)

    def assess_risk(
        self,
        context: EngineeringContext,
    ) -> RiskAssessment:
        return self._risk_builder.build(context)

    def build_judgment(
        self,
        context: EngineeringContext,
        risk: RiskAssessment,
    ) -> Judgment:
        return self._judgment_builder.build(
            context,
            risk,
        )

    def conclude(
        self,
        context: EngineeringContext,
    ) -> Conclusion:
        risk = self.assess_risk(context)

        judgment = self.build_judgment(
            context,
            risk,
        )

        return self._conclusion_builder.build(
            judgment,
        )

    def reason(
        self,
        observations: tuple[Observation, ...],
    ) -> Conclusion:
        context = self.build_context(observations)

        return self.conclude(context)