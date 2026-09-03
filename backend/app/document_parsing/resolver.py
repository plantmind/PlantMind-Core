"""Persistence-neutral parser resolver port for canonical Document Content."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.document_parsing.parser import DocumentContentParser
from app.domain.document_content import DocumentContentMediaType


class DocumentContentParserResolver(ABC):
    """Resolve one parser from canonical Document Content media type."""

    @abstractmethod
    def resolve(
        self,
        *,
        media_type: DocumentContentMediaType,
    ) -> DocumentContentParser:
        """Return the parser selected for one canonical media type."""
        ...
