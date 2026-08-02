"""Build engineering risk assessments from engineering context."""

from __future__ import annotations

from app.domain.context import EngineeringContext
from app.domain.risk_assessment import (
    RiskAssessment,
    RiskLevel,
)


class RiskBuilder:
    """
    Initial engineering risk evaluation.

    This is the baseline implementation. Future versions will use
    alarms, PI trends, maintenance history and engineering rules.
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
                f"Baseline assessment generated from "
                f"{len(context.evidence)} evidence item(s)."
            ),
        )