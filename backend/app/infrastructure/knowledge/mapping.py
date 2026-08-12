"""Explicit mapping between canonical Knowledge and relational rows."""

from __future__ import annotations

from app.domain.base import EntityId
from app.domain.knowledge import (
    KnowledgeKind,
    KnowledgeProvenance,
    KnowledgeRecord,
    KnowledgeSourceType,
    KnowledgeSubject,
    KnowledgeSubjectType,
)
from app.infrastructure.knowledge.models import KnowledgeRecordRow


def record_to_row(record: KnowledgeRecord) -> KnowledgeRecordRow:
    """Map canonical Knowledge to its relational representation."""

    subject_type: str | None = None
    subject_id = None

    if record.subject is not None:
        subject_type = record.subject.subject_type.value
        subject_id = record.subject.subject_id.value

    return KnowledgeRecordRow(
        id=record.id.value,
        kind=record.kind.value,
        title=record.title,
        content=record.content,
        provenance_source_type=record.provenance.source_type.value,
        provenance_source_reference=record.provenance.source_reference,
        provenance_captured_at=record.provenance.captured_at,
        subject_type=subject_type,
        subject_id=subject_id,
    )


def row_to_record(row: KnowledgeRecordRow) -> KnowledgeRecord:
    """Reconstruct canonical Knowledge from a relational row."""

    return KnowledgeRecord(
        id=EntityId.from_string(str(row.id)),
        kind=KnowledgeKind(value=row.kind),
        title=row.title,
        content=row.content,
        provenance=KnowledgeProvenance(
            source_type=KnowledgeSourceType(
                value=row.provenance_source_type
            ),
            source_reference=row.provenance_source_reference,
            captured_at=row.provenance_captured_at,
        ),
        subject=_subject_from_row(row),
    )


def _subject_from_row(
    row: KnowledgeRecordRow,
) -> KnowledgeSubject | None:
    """Reconstruct the optional canonical Knowledge subject."""

    has_type = row.subject_type is not None
    has_id = row.subject_id is not None

    if has_type != has_id:
        raise ValueError(
            "Knowledge subject type and identity must both be absent "
            "or both be present."
        )

    if not has_type:
        return None

    return KnowledgeSubject(
        subject_type=KnowledgeSubjectType(
            value=row.subject_type
        ),
        subject_id=EntityId.from_string(
            str(row.subject_id)
        ),
    )
