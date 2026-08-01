"""Engineering decision produced from validated judgment."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.domain.judgment import Judgment


class DecisionType(str, Enum):
    ACCEPT = "accept"
    INVESTIGATE = "investigate"
    MONITOR = "monitor"
    ESCALATE = "escalate"


@dataclass(frozen=True, slots=True, kw_only=True)
class Decision:
    """
    Engineering decision derived from a validated judgment.
    """

    judgment: Judgment
    decision_type: DecisionType
    rationale: str

    def __post_init__(self) -> None:
        if not self.rationale.strip():
            raise ValueError("Decision rationale must not be empty.")