"""Application boundary for canonical enterprise Document registration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.document.repository import EnterpriseDocumentRepository
from app.domain.base import EntityId
from app.domain.document import (
    DocumentSource,
    DocumentSourceType,
    DocumentType,
    EnterpriseDocument,
)


IdentitySource = Callable[[], EntityId]


@dataclass(frozen=True, slots=True, kw_only=True)
class EnterpriseDocumentRegistrationRequest:
    """Immutable application input for one canonical Document registration."""

    document_type: str
    title: str
    source_type: str
    source_reference: str


class EnterpriseDocumentRegistrationApplicationService:
    """Coordinate one canonical enterprise Document registration use case."""

    def __init__(
        self,
        *,
        repository: EnterpriseDocumentRepository,
        identity_source: IdentitySource = EntityId.new,
    ) -> None:
        self._repository = repository
        self._identity_source = identity_source

    def register(
        self,
        request: EnterpriseDocumentRegistrationRequest,
    ) -> EnterpriseDocument:
        """Construct, persist and return one canonical Enterprise Document."""
        document_id = self._identity_source()

        source = DocumentSource(
            source_type=DocumentSourceType(
                value=request.source_type,
            ),
            source_reference=request.source_reference,
        )

        document = EnterpriseDocument(
            id=document_id,
            document_type=DocumentType(
                value=request.document_type,
            ),
            title=request.title,
            source=source,
        )

        self._repository.add(document)

        return document
