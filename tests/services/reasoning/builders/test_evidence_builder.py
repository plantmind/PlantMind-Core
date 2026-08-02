from datetime import datetime, timezone

from app.domain.evidence import EvidenceType
from app.domain.observation import Observation, ObservationType
from app.services.reasoning.builders.evidence_builder import EvidenceBuilder


def make_observation(
    observation_type: ObservationType,
) -> Observation:
    return Observation(
        source="PI System",
        observation_type=observation_type,
        value="Discharge pressure increased.",
        observed_at=datetime.now(timezone.utc),
    )


def test_build_converts_observation_to_evidence() -> None:
    builder = EvidenceBuilder()

    evidence = builder.build(
        make_observation(ObservationType.PROCESS),
        confidence=0.90,
    )

    assert evidence.source == "PI System"
    assert evidence.evidence_type is EvidenceType.PROCESS
    assert evidence.description == "Discharge pressure increased."
    assert evidence.confidence == 0.90


def test_build_maps_all_supported_observation_types() -> None:
    builder = EvidenceBuilder()

    expected_types = {
        ObservationType.PROCESS: EvidenceType.PROCESS,
        ObservationType.ALARM: EvidenceType.ALARM,
        ObservationType.EQUIPMENT: EvidenceType.EQUIPMENT,
        ObservationType.MAINTENANCE: EvidenceType.MAINTENANCE,
        ObservationType.OPERATOR: EvidenceType.OPERATOR,
    }

    for observation_type, evidence_type in expected_types.items():
        evidence = builder.build(
            make_observation(observation_type),
        )

        assert evidence.evidence_type is evidence_type


def test_build_many_preserves_order() -> None:
    builder = EvidenceBuilder()

    observations = (
        make_observation(ObservationType.ALARM),
        make_observation(ObservationType.MAINTENANCE),
    )

    evidence = builder.build_many(
        observations,
        confidence=0.85,
    )

    assert len(evidence) == 2
    assert evidence[0].evidence_type is EvidenceType.ALARM
    assert evidence[1].evidence_type is EvidenceType.MAINTENANCE
    assert all(item.confidence == 0.85 for item in evidence)