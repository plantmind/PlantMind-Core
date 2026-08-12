from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.domain.base import EntityId
from app.domain.knowledge import (
    KnowledgeKind,
    KnowledgeProvenance,
    KnowledgeRecord,
    KnowledgeSourceType,
)
from app.infrastructure.knowledge.repository import (
    SQLAlchemyKnowledgeRecordRepository,
)
from app.knowledge.repository import (
    KnowledgeRecordAlreadyExistsError,
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
        "INSERT INTO knowledge_records ...",
        {},
        driver_error,
    )


def test_identity_unique_violation_is_translated_to_canonical_duplicate() -> None:
    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_knowledge_records",
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = SQLAlchemyKnowledgeRecordRepository(
        Mock(return_value=session)
    )

    with pytest.raises(
        KnowledgeRecordAlreadyExistsError
    ) as exc_info:
        repository.add(_build_record())

    assert exc_info.value.__cause__ is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_other_unique_constraint_is_not_misclassified_as_identity_duplicate() -> None:
    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="uq_unrelated_constraint",
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = SQLAlchemyKnowledgeRecordRepository(
        Mock(return_value=session)
    )

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_build_record())

    assert exc_info.value is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_non_unique_integrity_violation_is_not_misclassified() -> None:
    failure = _integrity_error(
        sqlstate="23514",
        constraint_name="ck_knowledge_records_subject_pair",
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = SQLAlchemyKnowledgeRecordRepository(
        Mock(return_value=session)
    )

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_build_record())

    assert exc_info.value is failure
    session.rollback.assert_called_once_with()
    session.close.assert_called_once_with()


def test_human_readable_error_message_is_not_used_for_duplicate_detection() -> None:
    failure = _integrity_error(
        sqlstate=None,
        constraint_name=None,
        message=(
            "duplicate key value violates unique constraint "
            "pk_knowledge_records"
        ),
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = SQLAlchemyKnowledgeRecordRepository(
        Mock(return_value=session)
    )

    with pytest.raises(IntegrityError) as exc_info:
        repository.add(_build_record())

    assert exc_info.value is failure


def test_duplicate_failure_does_not_mutate_canonical_record() -> None:
    record = _build_record()
    original = record

    failure = _integrity_error(
        sqlstate="23505",
        constraint_name="pk_knowledge_records",
    )
    session = Mock()
    session.commit.side_effect = failure
    repository = SQLAlchemyKnowledgeRecordRepository(
        Mock(return_value=session)
    )

    with pytest.raises(
        KnowledgeRecordAlreadyExistsError
    ):
        repository.add(record)

    assert record == original
    assert record.id == original.id


def test_add_does_not_precheck_identity_before_insert() -> None:
    session = Mock()
    repository = SQLAlchemyKnowledgeRecordRepository(
        Mock(return_value=session)
    )

    repository.add(_build_record())

    session.get.assert_not_called()
    session.execute.assert_not_called()
    session.scalar.assert_not_called()
    session.add.assert_called_once()
    session.commit.assert_called_once_with()
