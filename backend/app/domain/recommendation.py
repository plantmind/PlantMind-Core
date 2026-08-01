"""Engineering recommendation produced from an engineering decision."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.domain.decision import Decision


class RecommendationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True, kw_only=True)
class Recommendation:
    """
    Human-executable engineering recommendation.

    PlantMind recommends.
    Humans decide.
    Plant systems execute through approved workflows.
    """

    decision: Decision
    priority: RecommendationPriority
    title: str
    description: str

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Recommendation title must not be empty.")

        if not self.description.strip():
            raise ValueError("Recommendation description must not be empty.")