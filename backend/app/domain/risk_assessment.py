"""Engineering risk assessment produced from validated engineering context."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.domain.context import EngineeringContext


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True, kw_only=True)
class RiskAssessment:
    """
    Quantified engineering risk.

    Risk Assessment estimates operational risk based on validated
    engineering context before recommendations are generated.
    """

    context: EngineeringContext
    level: RiskLevel
    score: float
    rationale: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(
                "Risk score must be between 0.0 and 1.0."
            )

        if not self.rationale.strip():
            raise ValueError(
                "Risk rationale must not be empty."
            )