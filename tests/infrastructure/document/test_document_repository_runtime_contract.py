from __future__ import annotations

import importlib
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.document.repository import (
    EnterpriseDocumentRepository,
)
from app.domain.base import DomainException, EntityId
from app.domain.document import (
    DocumentSource,
    DocumentSourceType,
    DocumentType,
    EnterpriseDocument,
)


def _repository_class():
    module = importlib.import_module(
        "app.infrastructure.document.repository"
    )

    return module.SQLAlchemyEnterpriseDocumentRepository


def _models_module():
    return importlib.import_module(
        "app.infrastructure.document.models"
    )


def _mapping_module():
    return importlib.import_module(
        "app.infrastructure.document.mapping"
    )


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


def test_relational_repository_implements_canonical_port() -> None:
    repository_class = _repository_class()

    assert issubclass(
        repository_class,
        EnterpriseDocumentRepository,
    )


def test_add_uses_one_explicit_session_and_commits_once() -> None:
    repository_class = _repository_class()
    models = _models_module()

    session = Mock()
    session_factory = Mock(return_value=session)
    repository = repository_class(session_factory)
    document = _build_document()

    repository.add(document)

    session_factory.assert_called_once_with()
    session.add.assert_called_once()

    persisted = session.add.call_args.args[0]

    assert isinstance(
        persisted,
        models.EnterpriseDocumentRow,
    )
    assert persisted.id == document.id.value

    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_failed_add_rolls_back_and_preserves_original_failure() -> None:
    repository_class = _repository_class()

    session = Mock()
    failure = RuntimeError("commit failed")
    session.commit.side_effect = failure
    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(RuntimeError) as exc_info:
        repository.add(_build_document())

    assert exc_info.value is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_failed_add_preserves_rollback_failure_with_original_context() -> None:
    repository_class = _repository_class()

    session = Mock()
    operation_failure = RuntimeError("commit failed")
    rollback_failure = RuntimeError("rollback failed")

    session.commit.side_effect = operation_failure
    session.rollback.side_effect = rollback_failure

    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(RuntimeError) as exc_info:
        repository.add(_build_document())

    assert exc_info.value is rollback_failure
    assert exc_info.value.__cause__ is operation_failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_failed_add_preserves_close_failure_with_original_context() -> None:
    repository_class = _repository_class()

    session = Mock()
    operation_failure = RuntimeError("commit failed")
    close_failure = RuntimeError("close failed")

    session.commit.side_effect = operation_failure
    session.close.side_effect = close_failure

    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(RuntimeError) as exc_info:
        repository.add(_build_document())

    assert exc_info.value is close_failure
    assert exc_info.value.__context__ is operation_failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_get_is_read_only_and_closes_session() -> None:
    repository_class = _repository_class()
    models = _models_module()
    mapping = _mapping_module()

    document = _build_document()
    session = Mock()
    session.get.return_value = mapping.document_to_row(
        document
    )
    session_factory = Mock(return_value=session)
    repository = repository_class(session_factory)

    restored = repository.get(document.id)

    assert restored == document
    session_factory.assert_called_once_with()
    session.get.assert_called_once_with(
        models.EnterpriseDocumentRow,
        document.id.value,
    )
    session.commit.assert_not_called()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_get_returns_none_without_commit() -> None:
    repository_class = _repository_class()

    session = Mock()
    session.get.return_value = None
    repository = repository_class(
        Mock(return_value=session)
    )

    result = repository.get(EntityId.new())

    assert result is None
    session.commit.assert_not_called()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_get_closes_session_when_domain_reconstruction_fails() -> None:
    repository_class = _repository_class()
    mapping = _mapping_module()

    row = mapping.document_to_row(
        _build_document()
    )
    row.title = "   "

    session = Mock()
    session.get.return_value = row
    repository = repository_class(
        Mock(return_value=session)
    )

    with pytest.raises(DomainException):
        repository.get(EntityId.new())

    session.commit.assert_not_called()
    session.close.assert_called_once_with()


def test_repository_does_not_own_database_runtime_lifecycle() -> None:
    source_path = Path(
        "backend/app/infrastructure/document/"
        "repository.py"
    )

    assert source_path.is_file()

    source = source_path.read_text()

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
