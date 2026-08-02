"""Build engineering decisions from conclusions."""

from __future__ import annotations

from app.domain.conclusion import Conclusion
from app.domain.decision import Decision, DecisionType


class DecisionBuilder:
    """Transform an engineering conclusion into a decision."""

    def build(
        self,
        conclusion: Conclusion,
    ) -> Decision:
        return Decision(
            judgment=conclusion.judgment,
            decision_type=DecisionType.INVESTIGATE,
            rationale=conclusion.summary,
        )