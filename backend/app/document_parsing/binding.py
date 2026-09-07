"""Canonical Document Content parser binding contracts."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.document_parsing.parser import DocumentContentParser
from app.domain.document_content import DocumentContentMediaType


DocumentContentParserFactory = Callable[[], DocumentContentParser]


class DocumentContentParserDuplicateBindingError(ValueError):
    """Raised when a canonical parser media type is bound more than once."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentParserBinding:
    """Immutable canonical media-type-to-parser-factory binding."""

    media_type: DocumentContentMediaType
    factory: DocumentContentParserFactory

    def __post_init__(self) -> None:
        if not isinstance(
            self.media_type,
            DocumentContentMediaType,
        ):
            raise TypeError(
                "Document Content parser binding media type must be "
                "a DocumentContentMediaType."
            )

        if not callable(self.factory):
            raise TypeError(
                "Document Content parser binding factory must be callable."
            )
