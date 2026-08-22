"""Persistence-neutral repository contract for canonical Document Content."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.base import EntityId
from app.domain.document_content import DocumentContentDescriptor


class DocumentContentAlreadyExistsError(Exception):
    """Raised when canonical Document Content already exists."""


class DocumentContentRepository(ABC):
    """Persistence-neutral repository port for canonical Document Content."""

    @abstractmethod
    def add(
        self,
        descriptor: DocumentContentDescriptor,
    ) -> None:
        """Store one canonical descriptor without silent overwrite."""
        ...

    @abstractmethod
    def get(
        self,
        document_id: EntityId,
    ) -> DocumentContentDescriptor | None:
        """Return the canonical descriptor for a Document, if present."""
        ...
