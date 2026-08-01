"""Observation value object for PlantMind engineering reasoning."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class ObservationType(str, Enum):
    PROCESS = "process"
    ALARM = "alarm"
    EQUIPMENT = "equipment"
    MAINTENANCE = "maintenance"
    OPERATOR = "operator"


@dataclass(frozen=True, slots=True, kw_only=True)
class Observation:
    """
    Immutable observation captured from the industrial environment.

    Observations represent facts exactly as observed before any
    engineering interpretation.
    """

    source: str
    observation_type: ObservationType
    value: str
    observed_at: datetime

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("Observation source must not be empty.")

        if not self.value.strip():
            raise ValueError("Observation value must not be empty.")

        if self.observed_at.tzinfo is None:
            raise ValueError(
                "Observation timestamp must include timezone information."
            )

        object.__setattr__(
            self,
            "observed_at",
            self.observed_at.astimezone(timezone.utc),
        )