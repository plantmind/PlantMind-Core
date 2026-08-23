"""SQLAlchemy repository adapter for canonical Document Content."""

from __future__ import annotations

from collections.abc import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.document_content.repository import (
    DocumentContentAlreadyExistsError,
    DocumentContentRepository,
)
from app.domain.base import EntityId
from app.domain.document_content import DocumentContentDescriptor
from app.infrastructure.document_content.duplicate_classification import (
    is_identity_duplicate,
)
from app.infrastructure.document_content.mapping import (
    descriptor_to_row,
    row_to_descriptor,
)
from app.infrastructure.document_content.models import (
    DocumentContentDescriptorRow,
)


SessionFactory = Callable[[], Session]


class SQLAlchemyDocumentContentRepository(
    DocumentContentRepository
):
    """Persist canonical descriptors through an injected session factory."""

    def __init__(
        self,
        session_factory: SessionFactory,
    ) -> None:
        self._session_factory = session_factory

    def add(
        self,
        descriptor: DocumentContentDescriptor,
    ) -> None:
        session = self._session_factory()

        try:
            session.add(
                descriptor_to_row(descriptor)
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
                raise DocumentContentAlreadyExistsError(
                    "Canonical Document Content descriptor "
                    "identity already exists."
                ) from exc

            raise
        finally:
            session.close()

    def get(
        self,
        document_id: EntityId,
    ) -> DocumentContentDescriptor | None:
        session = self._session_factory()

        try:
            row = session.get(
                DocumentContentDescriptorRow,
                document_id.value,
            )

            if row is None:
                return None

            return row_to_descriptor(row)
        finally:
            session.close()
