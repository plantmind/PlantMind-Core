"""Persistence-neutral repository contract for canonical Document-to-Knowledge lineage."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.base import EntityId
from app.domain.document_knowledge_lineage import DocumentKnowledgeLineage


class DocumentKnowledgeLineageAlreadyExistsError(Exception):
    """Raised when canonical Document-to-Knowledge lineage already exists."""


class DocumentKnowledgeLineageRepository(ABC):
    """Persistence-neutral repository port for canonical lineage."""

    @abstractmethod
    def add(
        self,
        lineage: DocumentKnowledgeLineage,
    ) -> None:
        """Store one canonical lineage relation without silent overwrite."""
        ...

    @abstractmethod
    def get(
        self,
        document_id: EntityId,
        knowledge_record_id: EntityId,
    ) -> DocumentKnowledgeLineage | None:
        """Return the canonical lineage for an exact identity pair, if present."""
        ...
