"""Build the final PlantMind engineering report."""

from __future__ import annotations

from app.services.reasoning.explanation import Explanation
from app.services.reasoning.report import ReasoningReport
from app.services.reasoning.result import ReasoningResult


class ReportBuilder:
    """Combine reasoning result and explanation into a report."""

    def build(
        self,
        result: ReasoningResult,
        explanation: Explanation,
    ) -> ReasoningReport:
        return ReasoningReport(
            result=result,
            explanation=explanation,
        )