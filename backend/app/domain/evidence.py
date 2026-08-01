"""Evidence domain object used by PlantMind engineering reasoning."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceType(str, Enum):
    """Supported engineering evidence categories."""

    ALARM = "alarm"
    PROCESS = "process"
    EQUIPMENT = "equipment"
    MAINTENANCE = "maintenance"
    PROCEDURE = "procedure"
    OPERATOR = "operator"


@dataclass(frozen=True, slots=True, kw_only=True)
class Evidence:
    """
    Immutable engineering evidence.

    Evidence represents a verified engineering fact consumed by
    PlantMind intelligence engines.
    """

    source: str
    evidence_type: EvidenceType
    description: str
    confidence: float

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("Evidence source must not be empty.")

        if not self.description.strip():
            raise ValueError("Evidence description must not be empty.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Evidence confidence must be between 0.0 and 1.0.")