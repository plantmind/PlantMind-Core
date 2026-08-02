"""Explain PlantMind engineering reasoning."""

from __future__ import annotations

from app.services.reasoning.trace import ReasoningTrace


class ReasoningExplainer:
    """Generate a human-readable explanation of a reasoning trace."""

    def explain(
        self,
        trace: ReasoningTrace,
    ) -> str:
        lines = [
            "PlantMind Engineering Reasoning",
            "",
        ]

        for step in trace.steps:
            lines.append(f"- {step.name}: {step.description}")

        lines.extend(
            (
                "",
                f"Decision: {trace.result.decision.rationale}",
                f"Recommendation: {trace.result.recommendation.title}",
            )
        )

        return "\n".join(lines)