"""Opt-in composition for canonical Document Content parsing."""

from __future__ import annotations

from dataclasses import dataclass

from app.document_parsing.binding import DocumentContentParserBinding
from app.document_parsing.dispatching_parser import (
    DispatchingDocumentContentParser,
)
from app.domain.document_content import DocumentContentMediaType
from app.infrastructure.document_parsing.registry_backed_resolver import (
    RegistryBackedDocumentContentParserResolver,
)
from app.infrastructure.document_parsing.utf8_plain_text_parser import (
    Utf8PlainTextDocumentContentParser,
)
from app.services.document_content_access_application_service import (
    DocumentContentAccessApplicationService,
)
from app.services.document_content_parsing_application_service import (
    DocumentContentParsingApplicationService,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentParsingComposition:
    """Immutable canonical Document Content parsing object graph."""

    plain_text_parser: Utf8PlainTextDocumentContentParser
    plain_text_binding: DocumentContentParserBinding
    resolver: RegistryBackedDocumentContentParserResolver
    dispatcher: DispatchingDocumentContentParser
    application_service: DocumentContentParsingApplicationService


def build_document_content_parsing_composition(
    *,
    content_access_service: DocumentContentAccessApplicationService,
) -> DocumentContentParsingComposition:
    """Build one isolated opt-in canonical plain-text parsing graph."""
    if not isinstance(
        content_access_service,
        DocumentContentAccessApplicationService,
    ):
        raise TypeError(
            "content_access_service must be a "
            "DocumentContentAccessApplicationService."
        )

    plain_text_parser = Utf8PlainTextDocumentContentParser()

    plain_text_media_type = DocumentContentMediaType(
        value="text/plain",
    )

    def provide_plain_text_parser() -> Utf8PlainTextDocumentContentParser:
        return plain_text_parser

    plain_text_binding = DocumentContentParserBinding(
        media_type=plain_text_media_type,
        factory=provide_plain_text_parser,
    )

    resolver = RegistryBackedDocumentContentParserResolver(
        bindings=(plain_text_binding,),
    )

    dispatcher = DispatchingDocumentContentParser(
        resolver=resolver,
    )

    application_service = DocumentContentParsingApplicationService(
        content_access_service=content_access_service,
        parser=dispatcher,
    )

    return DocumentContentParsingComposition(
        plain_text_parser=plain_text_parser,
        plain_text_binding=plain_text_binding,
        resolver=resolver,
        dispatcher=dispatcher,
        application_service=application_service,
    )
