"""Build engineering evidence from validated observations."""

from __future__ import annotations

from app.domain.evidence import Evidence, EvidenceType
from app.domain.observation import Observation, ObservationType


_OBSERVATION_TO_EVIDENCE = {
    ObservationType.PROCESS: EvidenceType.PROCESS,
    ObservationType.ALARM: EvidenceType.ALARM,
    ObservationType.EQUIPMENT: EvidenceType.EQUIPMENT,
    ObservationType.MAINTENANCE: EvidenceType.MAINTENANCE,
    ObservationType.OPERATOR: EvidenceType.OPERATOR,
}


class EvidenceBuilder:
    """Transform validated observations into engineering evidence."""

    def build(
        self,
        observation: Observation,
        *,
        confidence: float = 1.0,
    ) -> Evidence:
        return Evidence(
            source=observation.source,
            evidence_type=_OBSERVATION_TO_EVIDENCE[
                observation.observation_type
            ],
            description=observation.value,
            confidence=confidence,
        )

    def build_many(
        self,
        observations: tuple[Observation, ...],
        *,
        confidence: float = 1.0,
    ) -> tuple[Evidence, ...]:
        return tuple(
            self.build(
                observation,
                confidence=confidence,
            )
            for observation in observations
        )