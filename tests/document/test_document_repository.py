"""Contract tests for the canonical Enterprise Document repository port."""

from __future__ import annotations

from dataclasses import replace

import pytest

from app.document.repository import (
    EnterpriseDocumentAlreadyExistsError,
    EnterpriseDocumentRepository,
)
from app.domain.base import DomainException, EntityId
from app.domain.document import (
    DocumentSource,
    DocumentSourceType,
    DocumentType,
    EnterpriseDocument,
)


def _document(
    *,
    document_id: EntityId | None = None,
    title: str = "Operating Procedure",
    source_reference: str = "PROC-001",
) -> EnterpriseDocument:
    return EnterpriseDocument(
        id=document_id or EntityId.new(),
        document_type=DocumentType(value="procedure"),
        title=title,
        source=DocumentSource(
            source_type=DocumentSourceType(value="file_server"),
            source_reference=source_reference,
        ),
    )


class InMemoryEnterpriseDocumentRepository(
    EnterpriseDocumentRepository
):
    """Test-only implementation of the accepted repository contract."""

    def __init__(self) -> None:
        self._documents: dict[EntityId, EnterpriseDocument] = {}

    def add(
        self,
        document: EnterpriseDocument,
    ) -> None:
        if document.id in self._documents:
            raise EnterpriseDocumentAlreadyExistsError(
                "Canonical Enterprise Document identity already exists."
            )

        self._documents[document.id] = document

    def get(
        self,
        document_id: EntityId,
    ) -> EnterpriseDocument | None:
        return self._documents.get(document_id)


def test_repository_exposes_exact_abstract_operation_set() -> None:
    assert EnterpriseDocumentRepository.__abstractmethods__ == {
        "add",
        "get",
    }


def test_duplicate_exception_is_repository_level() -> None:
    assert issubclass(
        EnterpriseDocumentAlreadyExistsError,
        Exception,
    )
    assert not issubclass(
        EnterpriseDocumentAlreadyExistsError,
        DomainException,
    )


def test_repository_add_and_get_canonical_document() -> None:
    repository = InMemoryEnterpriseDocumentRepository()
    document = _document()

    repository.add(document)

    assert repository.get(document.id) == document


def test_repository_get_absent_identity_returns_none() -> None:
    repository = InMemoryEnterpriseDocumentRepository()

    assert repository.get(EntityId.new()) is None


def test_duplicate_canonical_identity_raises_conflict() -> None:
    repository = InMemoryEnterpriseDocumentRepository()
    document = _document()

    repository.add(document)

    with pytest.raises(EnterpriseDocumentAlreadyExistsError):
        repository.add(document)


def test_duplicate_identity_does_not_silently_overwrite() -> None:
    repository = InMemoryEnterpriseDocumentRepository()
    document = _document(title="Original")

    repository.add(document)

    competing_document = replace(
        document,
        title="Replacement",
    )

    with pytest.raises(EnterpriseDocumentAlreadyExistsError):
        repository.add(competing_document)

    assert repository.get(document.id) == document


def test_equal_source_reference_is_not_duplicate_identity() -> None:
    repository = InMemoryEnterpriseDocumentRepository()

    first = _document(
        source_reference="PROC-001",
    )
    second = _document(
        source_reference="PROC-001",
    )

    assert first.id != second.id

    repository.add(first)
    repository.add(second)

    assert repository.get(first.id) == first
    assert repository.get(second.id) == second


def test_equal_title_is_not_duplicate_identity() -> None:
    repository = InMemoryEnterpriseDocumentRepository()

    first = _document(title="Shared Title")
    second = _document(title="Shared Title")

    repository.add(first)
    repository.add(second)

    assert repository.get(first.id) == first
    assert repository.get(second.id) == second
