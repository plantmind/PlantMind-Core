"""SQLAlchemy repository adapter for canonical Document-to-Knowledge lineage."""

from __future__ import annotations

from collections.abc import Callable

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
from app.infrastructure.document_knowledge_lineage.duplicate_classification import (
    is_identity_duplicate,
)
from app.infrastructure.document_knowledge_lineage.mapping import (
    lineage_to_row,
    row_to_lineage,
)
from app.infrastructure.document_knowledge_lineage.models import (
    DocumentKnowledgeLineageRow,
)


SessionFactory = Callable[[], Session]

class SQLAlchemyDocumentKnowledgeLineageRepository(
    DocumentKnowledgeLineageRepository
):
    """Persist canonical lineage through an injected session factory."""

    def __init__(
        self,
        session_factory: SessionFactory,
    ) -> None:
        self._session_factory = session_factory

    def add(
        self,
        lineage: DocumentKnowledgeLineage,
    ) -> None:
        session = self._session_factory()

        try:
            session.add(
                lineage_to_row(lineage)
            )
            session.commit()
        except Exception as exc:
            try:
                session.rollback()
            except Exception as rollback_exc:
                raise rollback_exc from exc

            if (
                isinstance(exc, IntegrityError)
                and is_identity_duplicate(exc)
            ):
                raise DocumentKnowledgeLineageAlreadyExistsError(
                    "Canonical Document-to-Knowledge lineage "
                    "identity already exists."
                ) from exc

            raise
        finally:
            session.close()

    def get(
        self,
        document_id: EntityId,
        knowledge_record_id: EntityId,
    ) -> DocumentKnowledgeLineage | None:
        session = self._session_factory()

        try:
            row = session.get(
                DocumentKnowledgeLineageRow,
                (
                    document_id.value,
                    knowledge_record_id.value,
                ),
            )

            if row is None:
                return None

            return row_to_lineage(row)
        finally:
            session.close()
