from __future__ import annotations

import importlib
from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from app.domain.base import DomainException, EntityId
from app.domain.knowledge import (
    KnowledgeKind,
    KnowledgeProvenance,
    KnowledgeRecord,
    KnowledgeSourceType,
)
from app.infrastructure.knowledge.mapping import record_to_row
from app.infrastructure.knowledge.models import KnowledgeRecordRow
from app.knowledge.repository import KnowledgeRecordRepository


def _repository_class():
    module = importlib.import_module(
        "app.infrastructure.knowledge.repository"
    )

    return module.SQLAlchemyKnowledgeRecordRepository


def _build_record() -> KnowledgeRecord:
    return KnowledgeRecord(
        id=EntityId.new(),
        kind=KnowledgeKind(value="procedure"),
        title="Compressor Start Procedure",
        content="Verify suction pressure before startup.",
        provenance=KnowledgeProvenance(
            source_type=KnowledgeSourceType(value="document"),
            source_reference="PROC-001",
            captured_at=datetime(
                2026,
                8,
                12,
                10,
                30,
                tzinfo=timezone.utc,
            ),
        ),
        subject=None,
    )


def test_relational_repository_implements_canonical_port() -> None:
    repository_class = _repository_class()

    assert issubclass(
        repository_class,
        KnowledgeRecordRepository,
    )


def test_add_uses_one_explicit_session_and_commits_once() -> None:
    repository_class = _repository_class()
    session = Mock()
    session_factory = Mock(return_value=session)
    repository = repository_class(session_factory)
    record = _build_record()

    repository.add(record)

    session_factory.assert_called_once_with()
    session.add.assert_called_once()

    persisted = session.add.call_args.args[0]

    assert isinstance(persisted, KnowledgeRecordRow)
    assert persisted.id == record.id.value

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
        repository.add(_build_record())

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
        repository.add(_build_record())

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
        repository.add(_build_record())

    assert exc_info.value is close_failure
    assert exc_info.value.__context__ is operation_failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_get_is_read_only_and_closes_session() -> None:
    repository_class = _repository_class()
    record = _build_record()
    session = Mock()
    session.get.return_value = record_to_row(record)
    session_factory = Mock(return_value=session)
    repository = repository_class(session_factory)

    restored = repository.get(record.id)

    assert restored == record
    session_factory.assert_called_once_with()
    session.get.assert_called_once_with(
        KnowledgeRecordRow,
        record.id.value,
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
    row = record_to_row(_build_record())
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
    from pathlib import Path

    source = Path(
        "backend/app/infrastructure/knowledge/repository.py"
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
