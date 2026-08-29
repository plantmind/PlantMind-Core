"""Persistence-neutral parser port for verified canonical Document Content."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import BinaryIO

from app.domain.document_content import DocumentContentDescriptor


class DocumentContentParserUnsupportedMediaTypeError(Exception):
    """Raised when a parser does not support the canonical media type."""


class DocumentContentParserInvalidContentError(Exception):
    """Raised when supported content cannot be structurally parsed."""


class DocumentContentParser(ABC):
    """Parse verified canonical Document Content into textual content."""

    @abstractmethod
    def parse(
        self,
        *,
        descriptor: DocumentContentDescriptor,
        payload: BinaryIO,
    ) -> str:
        """Parse one borrowed verified payload into text."""
