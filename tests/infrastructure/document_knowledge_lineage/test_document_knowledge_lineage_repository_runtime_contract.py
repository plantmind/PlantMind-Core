"""RFC-063 relational lineage repository runtime contract tests."""

from __future__ import annotations

import importlib
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageRepository,
)
from app.domain.base import EntityId
from app.domain.document_knowledge_lineage import (
    DocumentKnowledgeLineage,
)
from app.infrastructure.document_knowledge_lineage.mapping import (
    lineage_to_row,
)
from app.infrastructure.document_knowledge_lineage.models import (
    DocumentKnowledgeLineageRow,
)


def _repository_class():
    module = importlib.import_module(
        "app.infrastructure.document_knowledge_lineage.repository"
    )

    return module.SQLAlchemyDocumentKnowledgeLineageRepository


def _build_lineage() -> DocumentKnowledgeLineage:
    return DocumentKnowledgeLineage(
        document_id=EntityId.new(),
        knowledge_record_id=EntityId.new(),
    )


def test_relational_repository_implements_canonical_port() -> None:
    repository_class = _repository_class()

    assert issubclass(
        repository_class,
        DocumentKnowledgeLineageRepository,
    )


def test_add_uses_one_explicit_session_and_commits_once() -> None:
    repository_class = _repository_class()

    session = Mock()
    session_factory = Mock(return_value=session)
    repository = repository_class(session_factory)
    lineage = _build_lineage()

    repository.add(lineage)

    session_factory.assert_called_once_with()
    session.add.assert_called_once()

    persisted = session.add.call_args.args[0]

    assert isinstance(
        persisted,
        DocumentKnowledgeLineageRow,
    )
    assert persisted.document_id == lineage.document_id.value
    assert (
        persisted.knowledge_record_id
        == lineage.knowledge_record_id.value
    )

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
        repository.add(_build_lineage())

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
        repository.add(_build_lineage())

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
        repository.add(_build_lineage())

    assert exc_info.value is close_failure
    assert exc_info.value.__context__ is operation_failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_get_uses_exact_composite_identity_and_is_read_only() -> None:
    repository_class = _repository_class()

    lineage = _build_lineage()
    session = Mock()
    session.get.return_value = lineage_to_row(lineage)

    session_factory = Mock(return_value=session)
    repository = repository_class(session_factory)

    restored = repository.get(
        lineage.document_id,
        lineage.knowledge_record_id,
    )

    assert restored == lineage

    session_factory.assert_called_once_with()
    session.get.assert_called_once_with(
        DocumentKnowledgeLineageRow,
        (
            lineage.document_id.value,
            lineage.knowledge_record_id.value,
        ),
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

    result = repository.get(
        EntityId.new(),
        EntityId.new(),
    )

    assert result is None
    session.commit.assert_not_called()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_repository_does_not_own_database_runtime_lifecycle() -> None:
    _repository_class()

    source = Path(
        "backend/app/infrastructure/"
        "document_knowledge_lineage/repository.py"
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
