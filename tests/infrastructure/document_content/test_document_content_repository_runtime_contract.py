from __future__ import annotations

import importlib
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.document_content.repository import (
    DocumentContentRepository,
)
from app.domain.base import DomainException, EntityId
from app.domain.document_content import (
    DocumentContentDescriptor,
    DocumentContentDigest,
    DocumentContentMediaType,
)


def _repository_class():
    module = importlib.import_module(
        "app.infrastructure.document_content.repository"
    )
    return module.SQLAlchemyDocumentContentRepository


def _models():
    return importlib.import_module(
        "app.infrastructure.document_content.models"
    )


def _mapping():
    return importlib.import_module(
        "app.infrastructure.document_content.mapping"
    )


def _descriptor() -> DocumentContentDescriptor:
    return DocumentContentDescriptor(
        document_id=EntityId.new(),
        media_type=DocumentContentMediaType(
            value="application/pdf"
        ),
        byte_length=8192,
        digest=DocumentContentDigest(
            value="ab" * 32
        ),
    )


def test_relational_repository_implements_canonical_port() -> None:
    assert issubclass(
        _repository_class(),
        DocumentContentRepository,
    )


def test_add_uses_one_session_and_commits_once() -> None:
    session = Mock()
    session_factory = Mock(return_value=session)
    repository = _repository_class()(session_factory)
    descriptor = _descriptor()

    repository.add(descriptor)

    session_factory.assert_called_once_with()
    session.add.assert_called_once()

    row = session.add.call_args.args[0]

    assert isinstance(
        row,
        _models().DocumentContentDescriptorRow,
    )
    assert row.document_id == descriptor.document_id.value
    assert row.media_type == descriptor.media_type.value
    assert row.byte_length == descriptor.byte_length
    assert row.digest == descriptor.digest.value

    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_failed_add_rolls_back_and_preserves_original_failure() -> None:
    session = Mock()
    failure = RuntimeError("commit failed")
    session.commit.side_effect = failure

    repository = _repository_class()(
        Mock(return_value=session)
    )

    with pytest.raises(RuntimeError) as exc_info:
        repository.add(_descriptor())

    assert exc_info.value is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_failed_add_raises_rollback_failure_from_original_failure() -> None:
    session = Mock()
    operation_failure = RuntimeError("commit failed")
    rollback_failure = RuntimeError("rollback failed")

    session.commit.side_effect = operation_failure
    session.rollback.side_effect = rollback_failure

    repository = _repository_class()(
        Mock(return_value=session)
    )

    with pytest.raises(RuntimeError) as exc_info:
        repository.add(_descriptor())

    assert exc_info.value is rollback_failure
    assert exc_info.value.__cause__ is operation_failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_failed_add_propagates_close_failure_with_operation_context() -> None:
    session = Mock()
    operation_failure = RuntimeError("commit failed")
    close_failure = RuntimeError("close failed")

    session.commit.side_effect = operation_failure
    session.close.side_effect = close_failure

    repository = _repository_class()(
        Mock(return_value=session)
    )

    with pytest.raises(RuntimeError) as exc_info:
        repository.add(_descriptor())

    assert exc_info.value is close_failure
    assert exc_info.value.__context__ is operation_failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_get_uses_exact_document_identity_and_is_read_only() -> None:
    descriptor = _descriptor()
    session = Mock()
    session.get.return_value = (
        _mapping().descriptor_to_row(descriptor)
    )
    session_factory = Mock(return_value=session)

    repository = _repository_class()(session_factory)

    restored = repository.get(descriptor.document_id)

    assert restored == descriptor

    session_factory.assert_called_once_with()
    session.get.assert_called_once_with(
        _models().DocumentContentDescriptorRow,
        descriptor.document_id.value,
    )
    session.commit.assert_not_called()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_get_returns_none_when_descriptor_is_missing() -> None:
    session = Mock()
    session.get.return_value = None

    repository = _repository_class()(
        Mock(return_value=session)
    )

    result = repository.get(EntityId.new())

    assert result is None
    session.commit.assert_not_called()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_get_closes_session_when_domain_reconstruction_fails() -> None:
    row = _models().DocumentContentDescriptorRow(
        document_id=EntityId.new().value,
        media_type="invalid",
        byte_length=1,
        digest="ab" * 32,
    )

    session = Mock()
    session.get.return_value = row

    repository = _repository_class()(
        Mock(return_value=session)
    )

    with pytest.raises(DomainException):
        repository.get(EntityId.new())

    session.commit.assert_not_called()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_repository_does_not_own_database_runtime_lifecycle() -> None:
    source = Path(
        "backend/app/infrastructure/"
        "document_content/repository.py"
    ).read_text()

    prohibited = (
        "create_engine(",
        "sessionmaker(",
        "DatabaseRuntime(",
        "Settings(",
        "DATABASE_URL",
        "create_all(",
    )

    assert [
        marker
        for marker in prohibited
        if marker in source
    ] == []
