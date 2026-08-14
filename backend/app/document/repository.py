"""Persistence-neutral repository contract for canonical PlantMind Documents."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.base import EntityId
from app.domain.document import EnterpriseDocument


class EnterpriseDocumentAlreadyExistsError(Exception):
    """Raised when canonical Enterprise Document identity already exists."""


class EnterpriseDocumentRepository(ABC):
    """Persistence-neutral repository port for canonical Documents."""

    @abstractmethod
    def add(
        self,
        document: EnterpriseDocument,
    ) -> None:
        """Store one canonical Document without silent overwrite."""
        ...

    @abstractmethod
    def get(
        self,
        document_id: EntityId,
    ) -> EnterpriseDocument | None:
        """Return the canonical Document for an identity, if present."""
        ...
