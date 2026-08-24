"""Persistence-neutral binary Document Content store/access contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import BinaryIO

from app.domain.base import EntityId


class DocumentContentPayloadAlreadyExistsError(Exception):
    """Raised when binary content already exists for a document."""


class DocumentContentStore(ABC):
    """Persistence-neutral port for immutable binary Document Content."""

    @abstractmethod
    def add(
        self,
        document_id: EntityId,
        source: BinaryIO,
    ) -> None:
        """Establish one immutable binary payload for a document."""
        ...

    @abstractmethod
    def open(
        self,
        document_id: EntityId,
    ) -> AbstractContextManager[BinaryIO] | None:
        """Open the payload context, or return None for confirmed absence."""
        ...
