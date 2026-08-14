"""Canonical Document-to-Knowledge lineage domain contract."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.base import DomainException, EntityId


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentKnowledgeLineage:
    """Immutable canonical identity relationship from Document to Knowledge."""

    document_id: EntityId
    knowledge_record_id: EntityId

    def __post_init__(self) -> None:
        if not isinstance(self.document_id, EntityId):
            raise DomainException(
                "Document lineage identity must be an EntityId."
            )

        if not isinstance(self.knowledge_record_id, EntityId):
            raise DomainException(
                "Knowledge lineage identity must be an EntityId."
            )
