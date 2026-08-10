"""Runtime contract tests for the canonical enterprise knowledge domain."""

from __future__ import annotations

from datetime import datetime, timezone

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
    ("value_type", "invalid_value"),
    [
        (KnowledgeKind, None),
        (KnowledgeSourceType, 123),
        (KnowledgeSubjectType, object()),
    ],
)
def test_open_knowledge_types_reject_non_string_values(
    value_type,
    invalid_value: object,
) -> None:
    with pytest.raises(DomainException):
        value_type(value=invalid_value)


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("source_type", "document"),
        ("source_reference", 123),
        ("captured_at", "2026-08-10T18:30:00Z"),
    ],
)
def test_knowledge_provenance_rejects_invalid_runtime_types(
    field_name: str,
    invalid_value: object,
) -> None:
    values = {
        "source_type": KnowledgeSourceType(value="document"),
        "source_reference": "PROC-001",
        "captured_at": datetime(2026, 8, 10, 18, 30, tzinfo=timezone.utc),
    }
    values[field_name] = invalid_value

    with pytest.raises(DomainException):
        KnowledgeProvenance(**values)


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("subject_type", "equipment"),
        ("subject_id", "COMP-H-001"),
    ],
)
def test_knowledge_subject_rejects_invalid_runtime_types(
    field_name: str,
    invalid_value: object,
) -> None:
    values = {
        "subject_type": KnowledgeSubjectType(value="equipment"),
        "subject_id": EntityId.new(),
    }
    values[field_name] = invalid_value

    with pytest.raises(DomainException):
        KnowledgeSubject(**values)


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("id", "not-an-entity-id"),
        ("kind", "procedure"),
        ("title", 123),
        ("content", 123),
        ("provenance", "PROC-001"),
        ("subject", "COMP-H-001"),
    ],
)
def test_knowledge_record_rejects_invalid_runtime_types(
    field_name: str,
    invalid_value: object,
) -> None:
    values = {
        "id": EntityId.new(),
        "kind": KnowledgeKind(value="procedure"),
        "title": "Compressor Start Procedure",
        "content": "Verify suction pressure before startup.",
        "provenance": KnowledgeProvenance(
            source_type=KnowledgeSourceType(value="document"),
            source_reference="PROC-001",
            captured_at=datetime(2026, 8, 10, 18, 30, tzinfo=timezone.utc),
        ),
        "subject": None,
    }
    values[field_name] = invalid_value

    with pytest.raises(DomainException):
        KnowledgeRecord(**values)
