from pytest import raises

from app.domain.evidence import Evidence, EvidenceType


def test_valid_evidence():
    evidence = Evidence(
        source="PI System",
        evidence_type=EvidenceType.PROCESS,
        description="Discharge pressure increased",
        confidence=0.95,
    )

    assert evidence.confidence == 0.95


def test_empty_source():
    with raises(ValueError):
        Evidence(
            source="",
            evidence_type=EvidenceType.PROCESS,
            description="x",
            confidence=0.5,
        )


def test_invalid_confidence():
    with raises(ValueError):
        Evidence(
            source="PI",
            evidence_type=EvidenceType.PROCESS,
            description="x",
            confidence=1.5,
        )