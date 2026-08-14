"""SQLAlchemy repository adapter for canonical PlantMind Documents."""

from __future__ import annotations

from collections.abc import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.document.repository import (
    EnterpriseDocumentAlreadyExistsError,
    EnterpriseDocumentRepository,
)
from app.domain.base import EntityId
from app.domain.document import EnterpriseDocument
from app.infrastructure.document.mapping import (
    document_to_row,
    row_to_document,
)
from app.infrastructure.document.models import (
    EnterpriseDocumentRow,
)


SessionFactory = Callable[[], Session]

_IDENTITY_UNIQUE_SQLSTATE = "23505"
_IDENTITY_CONSTRAINT_NAME = "pk_enterprise_documents"


class SQLAlchemyEnterpriseDocumentRepository(
    EnterpriseDocumentRepository
):
    """Persist canonical Documents through an injected session factory."""

    def __init__(
        self,
        session_factory: SessionFactory,
    ) -> None:
        self._session_factory = session_factory

    def add(
        self,
        document: EnterpriseDocument,
    ) -> None:
        session = self._session_factory()

        try:
            session.add(
                document_to_row(document)
            )
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
                raise EnterpriseDocumentAlreadyExistsError(
                    "Canonical enterprise Document identity already exists."
                ) from exc

            raise
        finally:
            session.close()

    def get(
        self,
        document_id: EntityId,
    ) -> EnterpriseDocument | None:
        session = self._session_factory()

        try:
            row = session.get(
                EnterpriseDocumentRow,
                document_id.value,
            )

            if row is None:
                return None

            return row_to_document(row)
        finally:
            session.close()


def _is_identity_duplicate(
    error: IntegrityError,
) -> bool:
    """Identify only the canonical Document primary-key conflict."""

    driver_error = error.orig

    if (
        getattr(
            driver_error,
            "sqlstate",
            None,
        )
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
