"""Persistence-neutral repository contract for canonical PlantMind knowledge."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.base import EntityId
from app.domain.knowledge import KnowledgeRecord


class KnowledgeRecordAlreadyExistsError(Exception):
    """Raised when canonical knowledge identity already exists."""


class KnowledgeRecordRepository(ABC):
    """Persistence-neutral repository port for canonical knowledge records."""

    @abstractmethod
    def add(
        self,
        record: KnowledgeRecord,
    ) -> None:
        """Store one canonical knowledge record without silent overwrite."""
        ...

    @abstractmethod
    def get(
        self,
        record_id: EntityId,
    ) -> KnowledgeRecord | None:
        """Return the canonical knowledge record for an identity, if present."""
        ...
