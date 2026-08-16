"""RFC-064 SQLAlchemy transaction coordinator runtime contract tests."""

from __future__ import annotations

import importlib
from unittest.mock import Mock

import pytest

from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageRepository,
)
from app.knowledge.repository import KnowledgeRecordRepository


def _coordinator_class():
    module = importlib.import_module(
        "app.infrastructure.knowledge_lineage_transaction.coordinator"
    )

    return module.SQLAlchemyKnowledgeLineageTransactionCoordinator


def test_successful_execution_owns_one_shared_transaction_scope() -> None:
    coordinator_class = _coordinator_class()

    session = Mock()
    session_factory = Mock(return_value=session)

    coordinator = coordinator_class(session_factory)

    result_value = object()
    operation = Mock(return_value=result_value)

    result = coordinator.execute(operation)

    assert result is result_value

    session_factory.assert_called_once_with()
    session.begin.assert_called_once_with()

    operation.assert_called_once()

    knowledge_repository, lineage_repository = (
        operation.call_args.args
    )

    assert isinstance(
        knowledge_repository,
        KnowledgeRecordRepository,
    )
    assert isinstance(
        lineage_repository,
        DocumentKnowledgeLineageRepository,
    )

    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_operation_runs_only_after_transaction_is_established() -> None:
    coordinator_class = _coordinator_class()

    events: list[str] = []

    session = Mock()
    session.begin.side_effect = lambda: events.append("begin")
    session.commit.side_effect = lambda: events.append("commit")
    session.close.side_effect = lambda: events.append("close")

    def operation(
        knowledge_repository: KnowledgeRecordRepository,
        lineage_repository: DocumentKnowledgeLineageRepository,
    ) -> str:
        assert isinstance(
            knowledge_repository,
            KnowledgeRecordRepository,
        )
        assert isinstance(
            lineage_repository,
            DocumentKnowledgeLineageRepository,
        )
        events.append("operation")
        return "completed"

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    result = coordinator.execute(operation)

    assert result == "completed"
    assert events == [
        "begin",
        "operation",
        "commit",
        "close",
    ]


def test_operation_failure_rolls_back_once_and_closes_once() -> None:
    coordinator_class = _coordinator_class()

    session = Mock()
    session_factory = Mock(return_value=session)
    coordinator = coordinator_class(session_factory)

    failure = RuntimeError("operation failed")

    def operation(
        knowledge_repository: KnowledgeRecordRepository,
        lineage_repository: DocumentKnowledgeLineageRepository,
    ) -> None:
        raise failure

    with pytest.raises(RuntimeError) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value is failure

    session_factory.assert_called_once_with()
    session.begin.assert_called_once_with()
    session.commit.assert_not_called()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_post_commit_close_failure_has_explicit_committed_outcome() -> None:
    from app.knowledge_lineage_transaction.coordinator import (
        KnowledgeLineageTransactionPostCommitCleanupError,
    )

    coordinator_class = _coordinator_class()

    session = Mock()
    close_failure = RuntimeError("close failed")
    session.close.side_effect = close_failure

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    operation = Mock(return_value="completed")

    with pytest.raises(
        KnowledgeLineageTransactionPostCommitCleanupError
    ) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value.__cause__ is close_failure

    operation.assert_called_once()
    session.begin.assert_called_once_with()
    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_close_failure_does_not_mask_existing_rollback_failure() -> None:
    coordinator_class = _coordinator_class()

    session = Mock()

    operation_failure = RuntimeError("operation failed")
    rollback_failure = RuntimeError("rollback failed")
    close_failure = RuntimeError("close failed")

    session.rollback.side_effect = rollback_failure
    session.close.side_effect = close_failure

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    def operation(
        knowledge_repository: KnowledgeRecordRepository,
        lineage_repository: DocumentKnowledgeLineageRepository,
    ) -> None:
        raise operation_failure

    with pytest.raises(RuntimeError) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value is rollback_failure
    assert exc_info.value.__cause__ is operation_failure

    session.begin.assert_called_once_with()
    session.commit.assert_not_called()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_session_factory_failure_does_not_run_operation_or_cleanup() -> None:
    coordinator_class = _coordinator_class()

    acquisition_failure = RuntimeError("session acquisition failed")
    session_factory = Mock(side_effect=acquisition_failure)
    operation = Mock()

    coordinator = coordinator_class(session_factory)

    with pytest.raises(RuntimeError) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value is acquisition_failure

    session_factory.assert_called_once_with()
    operation.assert_not_called()


def test_transaction_start_failure_does_not_run_operation_and_closes_session() -> None:
    coordinator_class = _coordinator_class()

    session = Mock()
    start_failure = RuntimeError("transaction start failed")
    session.begin.side_effect = start_failure

    operation = Mock()

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    with pytest.raises(RuntimeError) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value is start_failure

    operation.assert_not_called()
    session.commit.assert_not_called()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_final_commit_failure_rolls_back_and_is_not_reported_as_success() -> None:
    coordinator_class = _coordinator_class()

    session = Mock()
    commit_failure = RuntimeError("commit failed")
    session.commit.side_effect = commit_failure

    operation = Mock(return_value="must-not-escape")

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    with pytest.raises(RuntimeError) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value is commit_failure

    operation.assert_called_once()
    session.commit.assert_called_once_with()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_commit_time_integrity_failure_is_not_heuristically_reclassified() -> None:
    from sqlalchemy.exc import IntegrityError

    class Diagnostic:
        constraint_name = "pk_knowledge_records"

    class DriverError(Exception):
        sqlstate = "23505"
        diag = Diagnostic()

    failure = IntegrityError(
        "COMMIT",
        {},
        DriverError("commit integrity failure"),
    )

    coordinator_class = _coordinator_class()

    session = Mock()
    session.commit.side_effect = failure

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    operation = Mock(return_value="must-not-escape")

    with pytest.raises(IntegrityError) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value is failure

    operation.assert_called_once()
    session.commit.assert_called_once_with()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_independent_executions_use_independent_sessions() -> None:
    coordinator_class = _coordinator_class()

    first_session = Mock()
    second_session = Mock()

    session_factory = Mock(
        side_effect=[
            first_session,
            second_session,
        ]
    )

    coordinator = coordinator_class(session_factory)

    seen_repositories = []

    def operation(
        knowledge_repository,
        lineage_repository,
    ) -> None:
        seen_repositories.append(
            (
                knowledge_repository,
                lineage_repository,
            )
        )

    coordinator.execute(operation)
    coordinator.execute(operation)

    assert session_factory.call_count == 2

    first_session.begin.assert_called_once_with()
    first_session.commit.assert_called_once_with()
    first_session.close.assert_called_once_with()

    second_session.begin.assert_called_once_with()
    second_session.commit.assert_called_once_with()
    second_session.close.assert_called_once_with()

    assert seen_repositories[0][0] is not seen_repositories[1][0]
    assert seen_repositories[0][1] is not seen_repositories[1][1]
