"""Build immutable engineering context from observations."""

from __future__ import annotations

from app.domain.context import EngineeringContext
from app.domain.observation import Observation
from app.services.reasoning.builders.evidence_builder import EvidenceBuilder


class ContextBuilder:
    """
    Build EngineeringContext from validated observations.
    """

    def __init__(self) -> None:
        self._evidence_builder = EvidenceBuilder()

    def build(
        self,
        observations: tuple[Observation, ...],
    ) -> EngineeringContext:
        evidence = self._evidence_builder.build_many(
            observations,
        )

        return EngineeringContext(
            observations=observations,
            evidence=evidence,
        )