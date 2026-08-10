"""Unit tests for the canonical enterprise knowledge domain."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

from app.domain.base import DomainException, EntityId
from app.domain.knowledge import (
    KnowledgeKind,
    KnowledgeProvenance,
    KnowledgeRecord,
    KnowledgeSourceType,
    KnowledgeSubject,
    KnowledgeSubjectType,
)


@pytest.mark.parametrize(
    "value_type",
    [
        KnowledgeKind,
        KnowledgeSourceType,
        KnowledgeSubjectType,
    ],
)
def test_knowledge_type_value_objects_normalize_open_values(value_type) -> None:
    value = value_type(value="  Procedure  Manual-V2  ")

    assert value.value == "procedure  manual-v2"


@pytest.mark.parametrize(
    "value_type",
    [
        KnowledgeKind,
        KnowledgeSourceType,
        KnowledgeSubjectType,
    ],
)
def test_knowledge_type_value_objects_reject_empty_values(value_type) -> None:
    with pytest.raises(DomainException):
        value_type(value="   ")


@pytest.mark.parametrize(
    "value_type",
    [
        KnowledgeKind,
        KnowledgeSourceType,
        KnowledgeSubjectType,
    ],
)
def test_knowledge_type_value_objects_are_immutable(value_type) -> None:
    value = value_type(value="procedure")

    with pytest.raises(FrozenInstanceError):
        setattr(value, "value", "changed")


def test_knowledge_provenance_normalizes_reference_and_timestamp_to_utc() -> None:
    captured_at = datetime(
        2026,
        8,
        10,
        21,
        30,
        tzinfo=timezone(timedelta(hours=3)),
    )

    provenance = KnowledgeProvenance(
        source_type=KnowledgeSourceType(value="  Document  "),
        source_reference="  PROC-001  ",
        captured_at=captured_at,
    )

    assert provenance.source_type.value == "document"
    assert provenance.source_reference == "PROC-001"
    assert provenance.captured_at == datetime(
        2026,
        8,
        10,
        18,
        30,
        tzinfo=timezone.utc,
    )
    assert provenance.captured_at.tzinfo is timezone.utc


def test_knowledge_provenance_rejects_empty_source_reference() -> None:
    with pytest.raises(DomainException):
        KnowledgeProvenance(
            source_type=KnowledgeSourceType(value="document"),
            source_reference="   ",
            captured_at=datetime.now(timezone.utc),
        )


def test_knowledge_provenance_requires_timezone_aware_timestamp() -> None:
    with pytest.raises(DomainException):
        KnowledgeProvenance(
            source_type=KnowledgeSourceType(value="document"),
            source_reference="PROC-001",
            captured_at=datetime(2026, 8, 10, 18, 30),
        )


def test_knowledge_subject_preserves_canonical_entity_reference() -> None:
    subject_id = EntityId.new()

    subject = KnowledgeSubject(
        subject_type=KnowledgeSubjectType(value="  Equipment  "),
        subject_id=subject_id,
    )

    assert subject.subject_type.value == "equipment"
    assert subject.subject_id == subject_id


def test_knowledge_subject_is_immutable() -> None:
    subject = KnowledgeSubject(
        subject_type=KnowledgeSubjectType(value="equipment"),
        subject_id=EntityId.new(),
    )

    with pytest.raises(FrozenInstanceError):
        setattr(subject, "subject_id", EntityId.new())


def build_provenance() -> KnowledgeProvenance:
    return KnowledgeProvenance(
        source_type=KnowledgeSourceType(value="document"),
        source_reference="PROC-001",
        captured_at=datetime(2026, 8, 10, 18, 30, tzinfo=timezone.utc),
    )


def build_record(
    *,
    title: str = "Compressor Start Procedure",
    content: str = "Verify suction pressure before startup.",
    subject: KnowledgeSubject | None = None,
) -> KnowledgeRecord:
    return KnowledgeRecord(
        id=EntityId.new(),
        kind=KnowledgeKind(value="procedure"),
        title=title,
        content=content,
        provenance=build_provenance(),
        subject=subject,
    )


def test_knowledge_record_uses_canonical_entity_identity() -> None:
    record_id = EntityId.new()

    record = KnowledgeRecord(
        id=record_id,
        kind=KnowledgeKind(value="procedure"),
        title="Compressor Start Procedure",
        content="Verify suction pressure before startup.",
        provenance=build_provenance(),
        subject=None,
    )

    assert record.id == record_id
    assert isinstance(record.id, EntityId)


def test_knowledge_record_normalizes_only_surrounding_content_whitespace() -> None:
    record = build_record(
        title="  Compressor  Start Procedure  ",
        content="  Step 1\n\n  Verify  pressure.  ",
    )

    assert record.title == "Compressor  Start Procedure"
    assert record.content == "Step 1\n\n  Verify  pressure."


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("title", "   "),
        ("content", "   "),
    ],
)
def test_knowledge_record_rejects_empty_required_text(
    field_name: str,
    field_value: str,
) -> None:
    values = {
        "title": "Compressor Start Procedure",
        "content": "Verify suction pressure before startup.",
    }
    values[field_name] = field_value

    with pytest.raises(DomainException):
        build_record(**values)


def test_knowledge_record_may_exist_without_subject() -> None:
    record = build_record()

    assert record.subject is None


def test_knowledge_record_references_equipment_identity_without_embedding_equipment() -> None:
    equipment_id = EntityId.new()
    subject = KnowledgeSubject(
        subject_type=KnowledgeSubjectType(value="equipment"),
        subject_id=equipment_id,
    )

    record = build_record(subject=subject)

    assert record.subject == subject
    assert record.subject.subject_id == equipment_id


def test_knowledge_record_is_immutable() -> None:
    record = build_record()

    with pytest.raises(FrozenInstanceError):
        setattr(record, "title", "Changed")
