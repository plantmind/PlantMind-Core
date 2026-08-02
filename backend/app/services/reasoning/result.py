"""Immutable result produced by the complete reasoning pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.conclusion import Conclusion
from app.domain.context import EngineeringContext
from app.domain.decision import Decision
from app.domain.judgment import Judgment
from app.domain.recommendation import Recommendation
from app.domain.risk_assessment import RiskAssessment


@dataclass(frozen=True, slots=True, kw_only=True)
class ReasoningResult:
    """Complete traceable output of one PlantMind reasoning run."""

    context: EngineeringContext
    risk: RiskAssessment
    judgment: Judgment
    conclusion: Conclusion
    decision: Decision
    recommendation: Recommendation