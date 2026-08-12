from __future__ import annotations

import importlib
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
from app.infrastructure.knowledge.models import KnowledgeRecordRow


def _mapping_module():
    return importlib.import_module(
        "app.infrastructure.knowledge.mapping"
    )


def _build_record(
    *,
    subject: KnowledgeSubject | None = None,
) -> KnowledgeRecord:
    return KnowledgeRecord(
        id=EntityId.new(),
        kind=KnowledgeKind(value=" Procedure "),
        title=" Compressor Start Procedure ",
        content=" Verify suction pressure before startup. ",
        provenance=KnowledgeProvenance(
            source_type=KnowledgeSourceType(value=" Document "),
            source_reference=" PROC-001 ",
            captured_at=datetime(
                2026,
                8,
                12,
                10,
                30,
                tzinfo=timezone(
                    timedelta(hours=3)
                ),
            ),
        ),
        subject=subject,
    )


def test_domain_to_relational_mapping_preserves_canonical_values() -> None:
    mapping = _mapping_module()
    record = _build_record()

    row = mapping.record_to_row(record)

    assert isinstance(row, KnowledgeRecordRow)
    assert row.id == record.id.value
    assert row.kind == "procedure"
    assert row.title == "Compressor Start Procedure"
    assert row.content == "Verify suction pressure before startup."
    assert row.provenance_source_type == "document"
    assert row.provenance_source_reference == "PROC-001"
    assert row.provenance_captured_at == record.provenance.captured_at
    assert row.subject_type is None
    assert row.subject_id is None


def test_relational_to_domain_mapping_round_trips_without_subject() -> None:
    mapping = _mapping_module()
    original = _build_record()

    restored = mapping.row_to_record(
        mapping.record_to_row(original)
    )

    assert restored == original


def test_relational_to_domain_mapping_round_trips_subject() -> None:
    mapping = _mapping_module()

    subject = KnowledgeSubject(
        subject_type=KnowledgeSubjectType(
            value=" Equipment "
        ),
        subject_id=EntityId.new(),
    )
    original = _build_record(subject=subject)

    restored = mapping.row_to_record(
        mapping.record_to_row(original)
    )

    assert restored == original


def test_relational_to_domain_mapping_canonicalizes_timestamp_to_utc() -> None:
    mapping = _mapping_module()

    row = KnowledgeRecordRow(
        id=EntityId.new().value,
        kind="procedure",
        title="Compressor Start Procedure",
        content="Verify suction pressure before startup.",
        provenance_source_type="document",
        provenance_source_reference="PROC-001",
        provenance_captured_at=datetime(
            2026,
            8,
            12,
            13,
            30,
            tzinfo=timezone(
                timedelta(hours=3)
            ),
        ),
        subject_type=None,
        subject_id=None,
    )

    restored = mapping.row_to_record(row)

    assert restored.provenance.captured_at.tzinfo is timezone.utc
    assert restored.provenance.captured_at == datetime(
        2026,
        8,
        12,
        10,
        30,
        tzinfo=timezone.utc,
    )


def test_relational_to_domain_mapping_rejects_partial_subject() -> None:
    mapping = _mapping_module()

    row = KnowledgeRecordRow(
        id=EntityId.new().value,
        kind="procedure",
        title="Compressor Start Procedure",
        content="Verify suction pressure before startup.",
        provenance_source_type="document",
        provenance_source_reference="PROC-001",
        provenance_captured_at=datetime.now(timezone.utc),
        subject_type="equipment",
        subject_id=None,
    )

    with pytest.raises(ValueError):
        mapping.row_to_record(row)


def test_relational_to_domain_mapping_preserves_domain_validation() -> None:
    mapping = _mapping_module()

    row = KnowledgeRecordRow(
        id=EntityId.new().value,
        kind="procedure",
        title="   ",
        content="Valid content",
        provenance_source_type="document",
        provenance_source_reference="PROC-001",
        provenance_captured_at=datetime.now(timezone.utc),
        subject_type=None,
        subject_id=None,
    )

    with pytest.raises(DomainException):
        mapping.row_to_record(row)
