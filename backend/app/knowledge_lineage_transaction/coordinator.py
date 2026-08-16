"""Persistence-neutral Knowledge-and-lineage transaction coordination contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeVar

from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageRepository,
)
from app.knowledge.repository import KnowledgeRecordRepository


T = TypeVar("T")


class KnowledgeLineageTransactionPostCommitCleanupError(Exception):
    """Raised when commit succeeds but coordinator-owned cleanup fails."""


class KnowledgeLineageTransactionCoordinator(ABC):
    """Coordinate canonical Knowledge and lineage persistence atomically."""

    @abstractmethod
    def execute(
        self,
        operation: Callable[
            [
                KnowledgeRecordRepository,
                DocumentKnowledgeLineageRepository,
            ],
            T,
        ],
    ) -> T:
        """Execute one operation inside one coordinated transaction scope."""
        ...
