"""Engineering judgment produced from validated context."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.domain.context import EngineeringContext


class JudgmentLevel(str, Enum):
    NORMAL = "normal"
    CAUTION = "caution"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True, kw_only=True)
class Judgment:
    """
    Engineering conclusion produced from an EngineeringContext.
    """

    context: EngineeringContext
    level: JudgmentLevel
    summary: str
    confidence: float

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ValueError("Judgment summary must not be empty.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Judgment confidence must be between 0.0 and 1.0."
            )