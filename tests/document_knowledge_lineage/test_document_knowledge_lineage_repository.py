"""Contract tests for canonical Document-to-Knowledge lineage repository."""

from __future__ import annotations

from inspect import isabstract

import pytest

from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageAlreadyExistsError,
    DocumentKnowledgeLineageRepository,
)
from app.domain.base import DomainException, EntityId
from app.domain.document_knowledge_lineage import DocumentKnowledgeLineage


def _lineage(
    *,
    document_id: EntityId | None = None,
    knowledge_record_id: EntityId | None = None,
) -> DocumentKnowledgeLineage:
    return DocumentKnowledgeLineage(
        document_id=document_id or EntityId.new(),
        knowledge_record_id=knowledge_record_id or EntityId.new(),
    )


class InMemoryDocumentKnowledgeLineageRepository(
    DocumentKnowledgeLineageRepository
):
    """Test-only reference implementation of accepted repository semantics."""

    def __init__(self) -> None:
        self._lineages: dict[
            tuple[EntityId, EntityId],
            DocumentKnowledgeLineage,
        ] = {}

    def add(
        self,
        lineage: DocumentKnowledgeLineage,
    ) -> None:
        key = (
            lineage.document_id,
            lineage.knowledge_record_id,
        )

        if key in self._lineages:
            raise DocumentKnowledgeLineageAlreadyExistsError(
                "Canonical Document-to-Knowledge lineage already exists."
            )

        self._lineages[key] = lineage

    def get(
        self,
        document_id: EntityId,
        knowledge_record_id: EntityId,
    ) -> DocumentKnowledgeLineage | None:
        return self._lineages.get(
            (
                document_id,
                knowledge_record_id,
            )
        )


def test_repository_is_abstract_with_exact_operation_set() -> None:
    assert isabstract(DocumentKnowledgeLineageRepository)
    assert DocumentKnowledgeLineageRepository.__abstractmethods__ == {
        "add",
        "get",
    }

    with pytest.raises(TypeError):
        DocumentKnowledgeLineageRepository()


def test_repository_conflict_is_not_domain_validation_error() -> None:
    assert issubclass(
        DocumentKnowledgeLineageAlreadyExistsError,
        Exception,
    )
    assert not issubclass(
        DocumentKnowledgeLineageAlreadyExistsError,
        DomainException,
    )


def test_add_and_get_preserve_canonical_lineage_value() -> None:
    repository = InMemoryDocumentKnowledgeLineageRepository()
    lineage = _lineage()

    repository.add(lineage)

    assert repository.get(
        lineage.document_id,
        lineage.knowledge_record_id,
    ) == lineage


def test_get_absent_exact_pair_returns_none() -> None:
    repository = InMemoryDocumentKnowledgeLineageRepository()

    assert repository.get(
        EntityId.new(),
        EntityId.new(),
    ) is None


def test_duplicate_exact_pair_raises_repository_conflict() -> None:
    repository = InMemoryDocumentKnowledgeLineageRepository()
    lineage = _lineage()

    repository.add(lineage)

    with pytest.raises(
        DocumentKnowledgeLineageAlreadyExistsError
    ):
        repository.add(lineage)


def test_duplicate_add_does_not_silently_overwrite() -> None:
    repository = InMemoryDocumentKnowledgeLineageRepository()

    document_id = EntityId.new()
    knowledge_record_id = EntityId.new()

    original = _lineage(
        document_id=document_id,
        knowledge_record_id=knowledge_record_id,
    )

    repository.add(original)

    duplicate = DocumentKnowledgeLineage(
        document_id=document_id,
        knowledge_record_id=knowledge_record_id,
    )

    with pytest.raises(
        DocumentKnowledgeLineageAlreadyExistsError
    ):
        repository.add(duplicate)

    assert repository.get(
        document_id,
        knowledge_record_id,
    ) == original


def test_same_document_with_distinct_knowledge_is_not_duplicate() -> None:
    repository = InMemoryDocumentKnowledgeLineageRepository()
    document_id = EntityId.new()

    first = _lineage(
        document_id=document_id,
        knowledge_record_id=EntityId.new(),
    )
    second = _lineage(
        document_id=document_id,
        knowledge_record_id=EntityId.new(),
    )

    repository.add(first)
    repository.add(second)

    assert repository.get(
        first.document_id,
        first.knowledge_record_id,
    ) == first
    assert repository.get(
        second.document_id,
        second.knowledge_record_id,
    ) == second


def test_same_knowledge_with_distinct_documents_is_not_duplicate() -> None:
    repository = InMemoryDocumentKnowledgeLineageRepository()
    knowledge_record_id = EntityId.new()

    first = _lineage(
        document_id=EntityId.new(),
        knowledge_record_id=knowledge_record_id,
    )
    second = _lineage(
        document_id=EntityId.new(),
        knowledge_record_id=knowledge_record_id,
    )

    repository.add(first)
    repository.add(second)

    assert repository.get(
        first.document_id,
        first.knowledge_record_id,
    ) == first
    assert repository.get(
        second.document_id,
        second.knowledge_record_id,
    ) == second
