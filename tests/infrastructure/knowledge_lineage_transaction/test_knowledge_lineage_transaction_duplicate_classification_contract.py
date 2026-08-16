"""RFC-064 coordinated duplicate-classification contract tests."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
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
from app.domain.knowledge import (
    KnowledgeKind,
    KnowledgeProvenance,
    KnowledgeRecord,
    KnowledgeSourceType,
)
from app.infrastructure.knowledge_lineage_transaction.coordinator import (
    SQLAlchemyKnowledgeLineageTransactionCoordinator,
)
from app.knowledge.repository import (
    KnowledgeRecordAlreadyExistsError,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

KNOWLEDGE_REPOSITORY = (
    PROJECT_ROOT
    / "backend/app/infrastructure/knowledge/repository.py"
)

LINEAGE_REPOSITORY = (
    PROJECT_ROOT
    / "backend/app/infrastructure/"
    "document_knowledge_lineage/repository.py"
)

COORDINATOR = (
    PROJECT_ROOT
    / "backend/app/infrastructure/"
    "knowledge_lineage_transaction/coordinator.py"
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
    ) -> None:
        super().__init__("database integrity failure")
        self.sqlstate = sqlstate
        self.diag = _Diagnostic(constraint_name)


def _integrity_error(
    *,
    sqlstate: str | None,
    constraint_name: str | None,
) -> IntegrityError:
    return IntegrityError(
        "INSERT ...",
        {},
        _DriverIntegrityError(
            sqlstate=sqlstate,
            constraint_name=constraint_name,
        ),
    )


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
                16,
                10,
                30,
                tzinfo=timezone.utc,
            ),
        ),
        subject=None,
    )


def _build_lineage() -> DocumentKnowledgeLineage:
    return DocumentKnowledgeLineage(
        document_id=EntityId.new(),
        knowledge_record_id=EntityId.new(),
    )


def test_scoped_knowledge_flush_translates_exact_identity_duplicate() -> None:
    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_knowledge_records",
    )

    session = Mock()
    session.flush.side_effect = failure

    coordinator = SQLAlchemyKnowledgeLineageTransactionCoordinator(
        Mock(return_value=session)
    )

    def operation(
        knowledge_repository,
        lineage_repository,
    ) -> None:
        knowledge_repository.add(_build_record())

    with pytest.raises(
        KnowledgeRecordAlreadyExistsError
    ) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value.__cause__ is failure
    session.commit.assert_not_called()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_scoped_lineage_flush_translates_exact_identity_duplicate() -> None:
    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_document_knowledge_lineages",
    )

    session = Mock()
    session.flush.side_effect = failure

    coordinator = SQLAlchemyKnowledgeLineageTransactionCoordinator(
        Mock(return_value=session)
    )

    def operation(
        knowledge_repository,
        lineage_repository,
    ) -> None:
        lineage_repository.add(_build_lineage())

    with pytest.raises(
        DocumentKnowledgeLineageAlreadyExistsError
    ) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value.__cause__ is failure
    session.commit.assert_not_called()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


@pytest.mark.parametrize(
    ("participant", "constraint_name"),
    [
        ("knowledge", "uq_unrelated_constraint"),
        ("lineage", "uq_unrelated_constraint"),
    ],
)
def test_scoped_unrelated_unique_failure_is_not_misclassified(
    participant: str,
    constraint_name: str,
) -> None:
    failure = _integrity_error(
        sqlstate="23505",
        constraint_name=constraint_name,
    )

    session = Mock()
    session.flush.side_effect = failure

    coordinator = SQLAlchemyKnowledgeLineageTransactionCoordinator(
        Mock(return_value=session)
    )

    def operation(
        knowledge_repository,
        lineage_repository,
    ) -> None:
        if participant == "knowledge":
            knowledge_repository.add(_build_record())
        else:
            lineage_repository.add(_build_lineage())

    with pytest.raises(IntegrityError) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value is failure
    session.commit.assert_not_called()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_standalone_and_scoped_paths_use_shared_classification_modules() -> None:
    knowledge_source = KNOWLEDGE_REPOSITORY.read_text()
    lineage_source = LINEAGE_REPOSITORY.read_text()
    coordinator_source = COORDINATOR.read_text()

    knowledge_classifier = (
        "app.infrastructure.knowledge."
        "duplicate_classification"
    )
    lineage_classifier = (
        "app.infrastructure.document_knowledge_lineage."
        "duplicate_classification"
    )

    assert knowledge_classifier in knowledge_source
    assert knowledge_classifier in coordinator_source

    assert lineage_classifier in lineage_source
    assert lineage_classifier in coordinator_source


def test_second_participant_failure_rolls_back_entire_coordinated_execution() -> None:
    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_document_knowledge_lineages",
    )

    session = Mock()
    session.flush.side_effect = [
        None,
        failure,
    ]

    coordinator = SQLAlchemyKnowledgeLineageTransactionCoordinator(
        Mock(return_value=session)
    )

    record = _build_record()
    lineage = DocumentKnowledgeLineage(
        document_id=EntityId.new(),
        knowledge_record_id=record.id,
    )

    def operation(
        knowledge_repository,
        lineage_repository,
    ) -> str:
        knowledge_repository.add(record)
        lineage_repository.add(lineage)

        return "must-not-escape"

    with pytest.raises(
        DocumentKnowledgeLineageAlreadyExistsError
    ) as exc_info:
        coordinator.execute(operation)

    assert exc_info.value.__cause__ is failure

    assert session.add.call_count == 2
    assert session.flush.call_count == 2

    session.commit.assert_not_called()
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()
