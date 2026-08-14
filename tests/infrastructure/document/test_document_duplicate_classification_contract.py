from __future__ import annotations

import importlib
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.document.repository import (
    EnterpriseDocumentAlreadyExistsError,
)
from app.domain.base import EntityId
from app.domain.document import (
    DocumentSource,
    DocumentSourceType,
    DocumentType,
    EnterpriseDocument,
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


def _repository_class():
    module = importlib.import_module(
        "app.infrastructure.document.repository"
    )

    return module.SQLAlchemyEnterpriseDocumentRepository


def _build_document() -> EnterpriseDocument:
    return EnterpriseDocument(
        id=EntityId.new(),
        document_type=DocumentType(
            value="procedure",
        ),
        title="Compressor Startup Procedure",
        source=DocumentSource(
            source_type=DocumentSourceType(
                value="document",
            ),
            source_reference="PROC-001",
        ),
    )


def _integrity_error(
    *,
    sqlstate: str | None,
    constraint_name: str | None,
    message: str = "database integrity failure",
) -> IntegrityError:
    driver_error = _DriverIntegrityError(
        sqlstate=sqlstate,
        constraint_name=constraint_name,
        message=message,
    )

    return IntegrityError(
        "INSERT INTO enterprise_documents ...",
        {},
        driver_error,
    )


def test_identity_unique_violation_is_translated_to_canonical_duplicate() -> None:
    repository_class = _repository_class()

    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_enterprise_documents",
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(
        EnterpriseDocumentAlreadyExistsError
    ) as exc_info:
        repository.add(_build_document())

    assert exc_info.value.__cause__ is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_other_unique_constraint_is_not_misclassified() -> None:
    repository_class = _repository_class()

    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="uq_unrelated_constraint",
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_build_document())

    assert exc_info.value is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_constraint_name_without_unique_sqlstate_is_not_misclassified() -> None:
    repository_class = _repository_class()

    failure = _integrity_error(
        sqlstate="23514",
        constraint_name="pk_enterprise_documents",
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_build_document())

    assert exc_info.value is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_unique_sqlstate_without_constraint_identity_is_not_misclassified() -> None:
    repository_class = _repository_class()

    failure = _integrity_error(
        sqlstate="23505",
        constraint_name=None,
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_build_document())

    assert exc_info.value is failure


def test_human_readable_error_message_is_not_used_for_duplicate_detection() -> None:
    repository_class = _repository_class()

    failure = _integrity_error(
        sqlstate=None,
        constraint_name=None,
        message=(
            "duplicate key value violates unique constraint "
            "pk_enterprise_documents"
        ),
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_build_document())

    assert exc_info.value is failure


def test_duplicate_failure_does_not_mutate_canonical_document() -> None:
    repository_class = _repository_class()
    document = _build_document()
    original = document

    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_enterprise_documents",
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(
        EnterpriseDocumentAlreadyExistsError
    ):
        repository.add(document)

    assert document == original
    assert document.id == original.id


def test_add_does_not_precheck_identity_before_insert() -> None:
    repository_class = _repository_class()
    session = Mock()
    repository = repository_class(
        Mock(return_value=session)
    )

    repository.add(_build_document())

    session.get.assert_not_called()
    session.execute.assert_not_called()
    session.scalar.assert_not_called()
    session.add.assert_called_once()
    session.commit.assert_called_once_with()
