"""Build engineering recommendations from engineering decisions."""

from __future__ import annotations

from app.domain.decision import Decision
from app.domain.recommendation import (
    Recommendation,
    RecommendationPriority,
)


class RecommendationBuilder:
    """Build a human-reviewed recommendation from an engineering decision."""

    def build(
        self,
        decision: Decision,
        *,
        priority: RecommendationPriority = RecommendationPriority.MEDIUM,
    ) -> Recommendation:
        return Recommendation(
            decision=decision,
            priority=priority,
            title="Review engineering decision",
            description=decision.rationale,
        )