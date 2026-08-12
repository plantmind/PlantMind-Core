"""SQLAlchemy repository adapter for canonical PlantMind Knowledge."""

from __future__ import annotations

from collections.abc import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.base import EntityId
from app.domain.knowledge import KnowledgeRecord
from app.infrastructure.knowledge.mapping import (
    record_to_row,
    row_to_record,
)
from app.infrastructure.knowledge.models import KnowledgeRecordRow
from app.knowledge.repository import (
    KnowledgeRecordAlreadyExistsError,
    KnowledgeRecordRepository,
)


SessionFactory = Callable[[], Session]

_IDENTITY_UNIQUE_SQLSTATE = "23505"
_IDENTITY_CONSTRAINT_NAME = "pk_knowledge_records"


class SQLAlchemyKnowledgeRecordRepository(
    KnowledgeRecordRepository
):
    """Persist canonical Knowledge through an injected session factory."""

    def __init__(
        self,
        session_factory: SessionFactory,
    ) -> None:
        self._session_factory = session_factory

    def add(
        self,
        record: KnowledgeRecord,
    ) -> None:
        session = self._session_factory()

        try:
            session.add(record_to_row(record))
            session.commit()
        except Exception as exc:
            try:
                session.rollback()
            except Exception as rollback_exc:
                raise rollback_exc from exc

            if (
                isinstance(exc, IntegrityError)
                and _is_identity_duplicate(exc)
            ):
                raise KnowledgeRecordAlreadyExistsError(
                    "Canonical knowledge identity already exists."
                ) from exc

            raise
        finally:
            session.close()

    def get(
        self,
        record_id: EntityId,
    ) -> KnowledgeRecord | None:
        session = self._session_factory()

        try:
            row = session.get(
                KnowledgeRecordRow,
                record_id.value,
            )

            if row is None:
                return None

            return row_to_record(row)
        finally:
            session.close()


def _is_identity_duplicate(
    error: IntegrityError,
) -> bool:
    """Identify only the canonical Knowledge primary-key conflict."""

    driver_error = error.orig

    if (
        getattr(driver_error, "sqlstate", None)
        != _IDENTITY_UNIQUE_SQLSTATE
    ):
        return False

    diagnostic = getattr(
        driver_error,
        "diag",
        None,
    )

    return (
        getattr(
            diagnostic,
            "constraint_name",
            None,
        )
        == _IDENTITY_CONSTRAINT_NAME
    )
