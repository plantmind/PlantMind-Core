"""Engineering context used during PlantMind reasoning."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.evidence import Evidence
from app.domain.observation import Observation


@dataclass(frozen=True, slots=True, kw_only=True)
class EngineeringContext:
    """
    Immutable engineering context.

    Combines raw observations with validated evidence before
    intelligence engines perform reasoning.
    """

    observations: tuple[Observation, ...] = ()
    evidence: tuple[Evidence, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "observations", tuple(self.observations))
        object.__setattr__(self, "evidence", tuple(self.evidence))