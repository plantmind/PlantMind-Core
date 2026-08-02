"""Build presentation-ready output from a reasoning report."""

from __future__ import annotations

from app.services.reasoning.presentation import (
    PresentationSection,
    ReasoningPresentation,
)
from app.services.reasoning.report import ReasoningReport


class PresentationBuilder:
    """Convert a reasoning report into a structured presentation."""

    def build(
        self,
        report: ReasoningReport,
    ) -> ReasoningPresentation:
        evidence_items = tuple(
            evidence.description
            for evidence in report.result.context.evidence
        )

        sections = (
            PresentationSection(
                heading="Engineering Evidence",
                items=evidence_items,
            ),
            PresentationSection(
                heading="Reasoning Trace",
                items=report.explanation.details,
            ),
        )

        return ReasoningPresentation(
            title=report.explanation.title,
            summary=report.explanation.summary,
            risk_level=report.result.risk.level.value,
            decision=report.result.decision.rationale,
            recommendation=report.result.recommendation.title,
            sections=sections,
        )
