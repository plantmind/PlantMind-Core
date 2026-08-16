"""SQLAlchemy Knowledge-and-lineage transaction coordinator."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageAlreadyExistsError,
    DocumentKnowledgeLineageRepository,
)
from app.domain.base import EntityId
from app.domain.document_knowledge_lineage import (
    DocumentKnowledgeLineage,
)
from app.domain.knowledge import KnowledgeRecord
from app.infrastructure.document_knowledge_lineage.duplicate_classification import (
    is_identity_duplicate as is_lineage_identity_duplicate,
)
from app.infrastructure.document_knowledge_lineage.mapping import (
    lineage_to_row,
    row_to_lineage,
)
from app.infrastructure.document_knowledge_lineage.models import (
    DocumentKnowledgeLineageRow,
)
from app.infrastructure.knowledge.models import KnowledgeRecordRow
from app.infrastructure.knowledge.duplicate_classification import (
    is_identity_duplicate as is_knowledge_identity_duplicate,
)
from app.infrastructure.knowledge.mapping import (
    record_to_row,
    row_to_record,
)
from app.knowledge.repository import (
    KnowledgeRecordAlreadyExistsError,
    KnowledgeRecordRepository,
)
from app.knowledge_lineage_transaction.coordinator import (
    KnowledgeLineageTransactionCoordinator,
    KnowledgeLineageTransactionPostCommitCleanupError,
)


T = TypeVar("T")
SessionFactory = Callable[[], Session]


class _TransactionScopedKnowledgeRecordRepository(
    KnowledgeRecordRepository
):
    """Knowledge repository participant bound to one shared session."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def add(
        self,
        record: KnowledgeRecord,
    ) -> None:
        self._session.add(
            record_to_row(record)
        )

        try:
            self._session.flush()
        except IntegrityError as exc:
            if is_knowledge_identity_duplicate(exc):
                raise KnowledgeRecordAlreadyExistsError(
                    "Canonical knowledge identity already exists."
                ) from exc

            raise

    def get(
        self,
        record_id: EntityId,
    ) -> KnowledgeRecord | None:
        row = self._session.get(
            KnowledgeRecordRow,
            record_id.value,
        )

        if row is None:
            return None

        return row_to_record(row)


class _TransactionScopedDocumentKnowledgeLineageRepository(
    DocumentKnowledgeLineageRepository
):
    """Lineage repository participant bound to one shared session."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def add(
        self,
        lineage: DocumentKnowledgeLineage,
    ) -> None:
        self._session.add(
            lineage_to_row(lineage)
        )

        try:
            self._session.flush()
        except IntegrityError as exc:
            if is_lineage_identity_duplicate(exc):
                raise DocumentKnowledgeLineageAlreadyExistsError(
                    "Canonical Document-to-Knowledge lineage "
                    "identity already exists."
                ) from exc

            raise

    def get(
        self,
        document_id: EntityId,
        knowledge_record_id: EntityId,
    ) -> DocumentKnowledgeLineage | None:
        row = self._session.get(
            DocumentKnowledgeLineageRow,
            (
                document_id.value,
                knowledge_record_id.value,
            ),
        )

        if row is None:
            return None

        return row_to_lineage(row)


class SQLAlchemyKnowledgeLineageTransactionCoordinator(
    KnowledgeLineageTransactionCoordinator
):
    """Coordinate Knowledge and lineage through one SQLAlchemy session."""

    def __init__(
        self,
        session_factory: SessionFactory,
    ) -> None:
        self._session_factory = session_factory

    def execute(
        self,
        operation: Callable[
            [
                KnowledgeRecordRepository,
                DocumentKnowledgeLineageRepository,
            ],
            T,
        ],
    ) -> T:
        session = self._session_factory()

        committed = False
        primary_failure: Exception | None = None

        try:
            try:
                session.begin()
            except Exception as exc:
                primary_failure = exc
                raise

            try:
                knowledge_repository = (
                    _TransactionScopedKnowledgeRecordRepository(
                        session
                    )
                )
                lineage_repository = (
                    _TransactionScopedDocumentKnowledgeLineageRepository(
                        session
                    )
                )

                result = operation(
                    knowledge_repository,
                    lineage_repository,
                )

                session.commit()
                committed = True

                return result

            except Exception as exc:
                primary_failure = exc

                try:
                    session.rollback()
                except Exception as rollback_exc:
                    primary_failure = rollback_exc
                    raise rollback_exc from exc

                raise

        finally:
            try:
                session.close()
            except Exception as close_exc:
                if committed:
                    raise (
                        KnowledgeLineageTransactionPostCommitCleanupError(
                            "Knowledge-and-lineage transaction committed "
                            "successfully, but session cleanup failed."
                        )
                    ) from close_exc

                if primary_failure is not None:
                    primary_failure.add_note(
                        "Coordinator-owned session cleanup also failed: "
                        f"{close_exc!r}"
                    )
                else:
                    raise
