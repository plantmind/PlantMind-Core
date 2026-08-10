"""Contract tests for the canonical knowledge repository port."""

from __future__ import annotations

from datetime import datetime, timezone
from inspect import isabstract

import pytest

from app.domain.base import DomainException, EntityId
from app.domain.knowledge import (
    KnowledgeKind,
    KnowledgeProvenance,
    KnowledgeRecord,
    KnowledgeSourceType,
)
from app.knowledge.repository import (
    KnowledgeRecordAlreadyExistsError,
    KnowledgeRecordRepository,
)


def build_record(
    *,
    record_id: EntityId | None = None,
    title: str = "Compressor Start Procedure",
) -> KnowledgeRecord:
    return KnowledgeRecord(
        id=record_id or EntityId.new(),
        kind=KnowledgeKind(value="procedure"),
        title=title,
        content="Verify suction pressure before startup.",
        provenance=KnowledgeProvenance(
            source_type=KnowledgeSourceType(value="document"),
            source_reference="PROC-001",
            captured_at=datetime(
                2026,
                8,
                10,
                18,
                30,
                tzinfo=timezone.utc,
            ),
        ),
        subject=None,
    )


class InMemoryKnowledgeRecordRepository(KnowledgeRecordRepository):
    """Test-only reference implementation of repository semantics."""

    def __init__(self) -> None:
        self._records: dict[EntityId, KnowledgeRecord] = {}

    def add(self, record: KnowledgeRecord) -> None:
        if record.id in self._records:
            raise KnowledgeRecordAlreadyExistsError(
                f"Knowledge record {record.id} already exists."
            )

        self._records[record.id] = record

    def get(self, record_id: EntityId) -> KnowledgeRecord | None:
        return self._records.get(record_id)


def test_knowledge_record_repository_is_abstract() -> None:
    assert isabstract(KnowledgeRecordRepository)
    assert KnowledgeRecordRepository.__abstractmethods__ == {"add", "get"}

    with pytest.raises(TypeError):
        KnowledgeRecordRepository()


def test_repository_conflict_is_not_a_domain_validation_error() -> None:
    assert issubclass(KnowledgeRecordAlreadyExistsError, Exception)
    assert not issubclass(KnowledgeRecordAlreadyExistsError, DomainException)


def test_repository_add_and_get_preserve_domain_value() -> None:
    repository = InMemoryKnowledgeRecordRepository()
    record = build_record()

    repository.add(record)

    retrieved = repository.get(record.id)

    assert retrieved == record


def test_repository_get_returns_none_for_missing_identity() -> None:
    repository = InMemoryKnowledgeRecordRepository()

    assert repository.get(EntityId.new()) is None


def test_repository_rejects_duplicate_canonical_identity() -> None:
    repository = InMemoryKnowledgeRecordRepository()
    record_id = EntityId.new()
    original = build_record(
        record_id=record_id,
        title="Original Knowledge",
    )
    duplicate = build_record(
        record_id=record_id,
        title="Replacement Knowledge",
    )

    repository.add(original)

    with pytest.raises(KnowledgeRecordAlreadyExistsError):
        repository.add(duplicate)

    assert repository.get(record_id) == original
