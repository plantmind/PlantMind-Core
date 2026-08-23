from __future__ import annotations

import importlib
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.document_content.repository import (
    DocumentContentAlreadyExistsError,
)
from app.domain.base import EntityId
from app.domain.document_content import (
    DocumentContentDescriptor,
    DocumentContentDigest,
    DocumentContentMediaType,
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
        "app.infrastructure.document_content.repository"
    )
    return module.SQLAlchemyDocumentContentRepository


def _descriptor() -> DocumentContentDescriptor:
    return DocumentContentDescriptor(
        document_id=EntityId.new(),
        media_type=DocumentContentMediaType(
            value="application/pdf"
        ),
        byte_length=64,
        digest=DocumentContentDigest(
            value="ab" * 32
        ),
    )


def _integrity_error(
    *,
    sqlstate: str | None,
    constraint_name: str | None,
    message: str = "database integrity failure",
) -> IntegrityError:
    return IntegrityError(
        "INSERT INTO document_content_descriptors ...",
        {},
        _DriverIntegrityError(
            sqlstate=sqlstate,
            constraint_name=constraint_name,
            message=message,
        ),
    )


def _repository_with_failure(
    failure: Exception,
):
    session = Mock()
    session.commit.side_effect = failure

    repository = _repository_class()(
        Mock(return_value=session)
    )

    return repository, session


def test_exact_primary_key_unique_violation_is_translated() -> None:
    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_document_content_descriptors",
    )
    repository, session = _repository_with_failure(failure)

    with pytest.raises(
        DocumentContentAlreadyExistsError
    ) as exc_info:
        repository.add(_descriptor())

    assert exc_info.value.__cause__ is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


@pytest.mark.parametrize(
    ("sqlstate", "constraint_name"),
    [
        ("23505", "uq_unrelated_constraint"),
        ("23514", "pk_document_content_descriptors"),
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
        repository.add(_descriptor())

    assert exc_info.value is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_human_readable_message_is_not_used_for_duplicate_detection() -> None:
    failure = _integrity_error(
        sqlstate=None,
        constraint_name=None,
        message=(
            "duplicate key value violates unique constraint "
            "pk_document_content_descriptors"
        ),
    )
    repository, _ = _repository_with_failure(failure)

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_descriptor())

    assert exc_info.value is failure


def test_duplicate_failure_does_not_mutate_domain_descriptor() -> None:
    descriptor = _descriptor()
    original = descriptor

    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_document_content_descriptors",
    )
    repository, _ = _repository_with_failure(failure)

    with pytest.raises(DocumentContentAlreadyExistsError):
        repository.add(descriptor)

    assert descriptor == original
    assert descriptor.document_id == original.document_id


def test_add_does_not_precheck_document_identity() -> None:
    session = Mock()
    repository = _repository_class()(
        Mock(return_value=session)
    )

    repository.add(_descriptor())

    session.get.assert_not_called()
    session.execute.assert_not_called()
    session.scalar.assert_not_called()
    session.add.assert_called_once()
    session.commit.assert_called_once_with()
