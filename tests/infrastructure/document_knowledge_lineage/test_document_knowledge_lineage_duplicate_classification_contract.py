"""RFC-063 canonical lineage duplicate-classification contract tests."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageAlreadyExistsError,
)
from app.domain.base import EntityId
from app.domain.document_knowledge_lineage import (
    DocumentKnowledgeLineage,
)
from app.infrastructure.document_knowledge_lineage.repository import (
    SQLAlchemyDocumentKnowledgeLineageRepository,
)


class _Diagnostic:
    def __init__(
        self,
        constraint_name: str | None,
    ) -> None:
        self.constraint_name = constraint_name


class _DriverIntegrityError(Exception):
    def __init__(
        self,
        *,
        sqlstate: str | None,
        constraint_name: str | None,
        message: str = "database integrity failure",
    ) -> None:
        super().__init__(message)
        self.sqlstate = sqlstate
        self.diag = _Diagnostic(constraint_name)


def _build_lineage() -> DocumentKnowledgeLineage:
    return DocumentKnowledgeLineage(
        document_id=EntityId.new(),
        knowledge_record_id=EntityId.new(),
    )


def _integrity_error(
    *,
    sqlstate: str | None,
    constraint_name: str | None,
    message: str = "database integrity failure",
) -> IntegrityError:
    return IntegrityError(
        "INSERT INTO document_knowledge_lineages ...",
        {},
        _DriverIntegrityError(
            sqlstate=sqlstate,
            constraint_name=constraint_name,
            message=message,
        ),
    )


def _repository_with_failure(
    failure: Exception,
) -> tuple[
    SQLAlchemyDocumentKnowledgeLineageRepository,
    Mock,
]:
    session = Mock()
    session.commit.side_effect = failure

    repository = SQLAlchemyDocumentKnowledgeLineageRepository(
        Mock(return_value=session)
    )

    return repository, session


def test_exact_primary_key_unique_violation_is_translated() -> None:
    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_document_knowledge_lineages",
    )

    repository, session = _repository_with_failure(failure)

    with pytest.raises(
        DocumentKnowledgeLineageAlreadyExistsError
    ) as exc_info:
        repository.add(_build_lineage())

    assert exc_info.value.__cause__ is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


@pytest.mark.parametrize(
    ("sqlstate", "constraint_name"),
    [
        ("23505", "uq_unrelated_constraint"),
        ("23514", "pk_document_knowledge_lineages"),
        ("23505", None),
    ],
)
def test_unrelated_integrity_failures_are_not_misclassified(
    sqlstate: str | None,
    constraint_name: str | None,
) -> None:
    failure = _integrity_error(
        sqlstate=sqlstate,
        constraint_name=constraint_name,
    )

    repository, session = _repository_with_failure(failure)

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_build_lineage())

    assert exc_info.value is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_human_readable_message_is_not_used_for_duplicate_detection() -> None:
    failure = _integrity_error(
        sqlstate=None,
        constraint_name=None,
        message=(
            "duplicate key value violates unique constraint "
            "pk_document_knowledge_lineages"
        ),
    )

    repository, _ = _repository_with_failure(failure)

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_build_lineage())

    assert exc_info.value is failure


def test_duplicate_failure_does_not_mutate_canonical_lineage() -> None:
    lineage = _build_lineage()

    document_id = lineage.document_id
    knowledge_record_id = lineage.knowledge_record_id

    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_document_knowledge_lineages",
    )

    repository, _ = _repository_with_failure(failure)

    with pytest.raises(
        DocumentKnowledgeLineageAlreadyExistsError
    ):
        repository.add(lineage)

    assert lineage.document_id == document_id
    assert lineage.knowledge_record_id == knowledge_record_id


def test_add_does_not_precheck_identity_or_referenced_entities() -> None:
    session = Mock()

    repository = SQLAlchemyDocumentKnowledgeLineageRepository(
        Mock(return_value=session)
    )

    repository.add(_build_lineage())

    session.get.assert_not_called()
    session.execute.assert_not_called()
    session.scalar.assert_not_called()
    session.add.assert_called_once()
    session.commit.assert_called_once_with()
