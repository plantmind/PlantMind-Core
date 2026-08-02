"""Generate a complete PlantMind reasoning report."""

from __future__ import annotations

from app.domain.observation import Observation
from app.services.reasoning.explanation_builder import ExplanationBuilder
from app.services.reasoning.pipeline import ReasoningPipeline
from app.services.reasoning.report import ReasoningReport
from app.services.reasoning.report_builder import ReportBuilder
from app.services.reasoning.trace import ReasoningTrace, TraceStep


class ReportGenerator:
    """Execute reasoning and generate a traceable engineering report."""

    def __init__(self) -> None:
        self._pipeline = ReasoningPipeline()
        self._explanation_builder = ExplanationBuilder()
        self._report_builder = ReportBuilder()

    def generate(
        self,
        observations: tuple[Observation, ...],
    ) -> ReasoningReport:
        result = self._pipeline.run_result(observations)

        trace = ReasoningTrace(
            result=result,
            steps=(
                TraceStep(
                    name="ContextBuilder",
                    description="Engineering context created.",
                ),
                TraceStep(
                    name="RiskBuilder",
                    description="Risk assessment completed.",
                ),
                TraceStep(
                    name="JudgmentBuilder",
                    description="Engineering judgment generated.",
                ),
                TraceStep(
                    name="ConclusionBuilder",
                    description="Engineering conclusion generated.",
                ),
                TraceStep(
                    name="DecisionBuilder",
                    description="Engineering decision generated.",
                ),
                TraceStep(
                    name="RecommendationBuilder",
                    description="Human-reviewed recommendation generated.",
                ),
            ),
        )

        explanation = self._explanation_builder.build(trace)

        return self._report_builder.build(
            result=result,
            explanation=explanation,
        )