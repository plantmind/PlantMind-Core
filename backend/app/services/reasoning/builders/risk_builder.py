"""Build baseline engineering risk assessments from engineering context."""

from __future__ import annotations

from app.domain.context import EngineeringContext
from app.domain.risk_assessment import (
    RiskAssessment,
    RiskLevel,
)


class RiskBuilder:
    """
    Non-production baseline risk evaluator.

    This implementation estimates risk only from the number of evidence
    items. It does not yet evaluate evidence severity, alarm priority,
    process limits, PI trends, maintenance history, procedures, safeguards,
    or equipment-specific engineering rules.

    Its output is intended for development and pipeline validation only.
    It must not be treated as a final industrial risk assessment.
    """

    def build(
        self,
        context: EngineeringContext,
    ) -> RiskAssessment:
        score = min(
            1.0,
            0.10 + (len(context.evidence) * 0.10),
        )

        if score >= 0.80:
            level = RiskLevel.CRITICAL
        elif score >= 0.60:
            level = RiskLevel.HIGH
        elif score >= 0.30:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return RiskAssessment(
            context=context,
            level=level,
            score=score,
            rationale=(
                "Development baseline only: assessment generated from "
                f"{len(context.evidence)} evidence item(s); evidence "
                "severity and engineering rules were not evaluated."
            ),
        )