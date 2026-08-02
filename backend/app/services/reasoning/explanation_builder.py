"""Build structured explanations from reasoning traces."""

from __future__ import annotations

from app.services.reasoning.explanation import Explanation
from app.services.reasoning.trace import ReasoningTrace


class ExplanationBuilder:
    """Create a structured explanation from a reasoning trace."""

    def build(
        self,
        trace: ReasoningTrace,
    ) -> Explanation:
        return Explanation(
            title="PlantMind Engineering Analysis",
            summary=trace.result.conclusion.summary,
            details=tuple(
                f"{step.name}: {step.description}"
                for step in trace.steps
            ),
        )