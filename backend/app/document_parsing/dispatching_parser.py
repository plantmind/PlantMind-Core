"""Canonical Document Content parser dispatch implementation."""

from __future__ import annotations

from typing import BinaryIO

from app.document_parsing.parser import DocumentContentParser
from app.document_parsing.resolver import DocumentContentParserResolver
from app.domain.document_content import DocumentContentDescriptor


class DispatchingDocumentContentParser(DocumentContentParser):
    """Resolve and invoke one parser through the canonical parser port."""

    def __init__(
        self,
        *,
        resolver: DocumentContentParserResolver,
    ) -> None:
        self._resolver = resolver

    def parse(
        self,
        *,
        descriptor: DocumentContentDescriptor,
        payload: BinaryIO,
    ) -> str:
        """Delegate parsing by the descriptor's canonical media type."""
        parser = self._resolver.resolve(
            media_type=descriptor.media_type,
        )

        return parser.parse(
            descriptor=descriptor,
            payload=payload,
        )
