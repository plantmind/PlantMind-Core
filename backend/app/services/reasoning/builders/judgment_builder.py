"""Build engineering judgments from risk assessments."""

from __future__ import annotations

from app.domain.context import EngineeringContext
from app.domain.judgment import Judgment, JudgmentLevel
from app.domain.risk_assessment import RiskAssessment, RiskLevel


class JudgmentBuilder:
    """
    Transform engineering risk into an engineering judgment.
    """

    _LEVEL_MAP = {
        RiskLevel.LOW: JudgmentLevel.NORMAL,
        RiskLevel.MEDIUM: JudgmentLevel.CAUTION,
        RiskLevel.HIGH: JudgmentLevel.WARNING,
        RiskLevel.CRITICAL: JudgmentLevel.CRITICAL,
    }

    def build(
        self,
        context: EngineeringContext,
        risk: RiskAssessment,
    ) -> Judgment:
        return Judgment(
            context=context,
            level=self._LEVEL_MAP[risk.level],
            summary=(
                f"Engineering judgment generated from "
                f"{risk.level.value} risk."
            ),
            confidence=min(
                1.0,
                max(0.50, risk.score + 0.20),
            ),
        )