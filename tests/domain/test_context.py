from app.domain.context import EngineeringContext
from app.domain.evidence import Evidence, EvidenceType
from app.domain.observation import Observation, ObservationType

from datetime import datetime, timezone


def make_observation():
    return Observation(
        source="PI System",
        observation_type=ObservationType.PROCESS,
        value="Discharge Pressure = 41.2 bar",
        observed_at=datetime.now(timezone.utc),
    )


def make_evidence():
    return Evidence(
        source="PI System",
        evidence_type=EvidenceType.PROCESS,
        description="Pressure trend confirmed",
        confidence=0.95,
    )


def test_context_is_immutable():
    context = EngineeringContext(
        observations=[make_observation()],
        evidence=[make_evidence()],
    )

    assert len(context.observations) == 1
    assert len(context.evidence) == 1
    assert isinstance(context.observations, tuple)
    assert isinstance(context.evidence, tuple)