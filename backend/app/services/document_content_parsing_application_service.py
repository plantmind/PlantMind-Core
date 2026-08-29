"""Application boundary for canonical Document Content parsing."""

from __future__ import annotations

from dataclasses import dataclass

from app.document_parsing.parser import DocumentContentParser
from app.domain.base import EntityId
from app.domain.document_content import DocumentContentDescriptor
from app.services.document_content_access_application_service import (
    DocumentContentAccessApplicationService,
    DocumentContentAccessRequest,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentParsingRequest:
    """Immutable input for one canonical Document Content parse."""

    document_id: EntityId


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentParsingResult:
    """Verified descriptor plus parsed textual content."""

    descriptor: DocumentContentDescriptor
    text: str


class DocumentContentParsingApplicationService:
    """Parse verified canonical content through the accepted parser port."""

    def __init__(
        self,
        *,
        content_access_service: DocumentContentAccessApplicationService,
        parser: DocumentContentParser,
    ) -> None:
        self._content_access_service = content_access_service
        self._parser = parser

    def parse(
        self,
        request: DocumentContentParsingRequest,
    ) -> DocumentContentParsingResult:
        """Parse one canonical Document Content payload."""

        access_request = DocumentContentAccessRequest(
            document_id=request.document_id
        )

        with self._content_access_service.open(access_request) as access:
            descriptor = access.descriptor
            text = self._parser.parse(
                descriptor=descriptor,
                payload=access.payload,
            )

            if not isinstance(text, str):
                raise TypeError(
                    "Document Content parser must return str."
                )

        return DocumentContentParsingResult(
            descriptor=descriptor,
            text=text,
        )
