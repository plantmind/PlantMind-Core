"""Application boundary for canonical Document-to-Knowledge ingestion."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.document.repository import EnterpriseDocumentRepository
from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageRepository,
)
from app.domain.base import EntityId
from app.domain.document_knowledge_lineage import DocumentKnowledgeLineage
from app.domain.knowledge import KnowledgeRecord
from app.knowledge.repository import KnowledgeRecordRepository
from app.knowledge_lineage_transaction.coordinator import (
    KnowledgeLineageTransactionCoordinator,
)
from app.services.knowledge_capture_application_service import (
    KnowledgeCaptureApplicationService,
    KnowledgeCaptureRequest,
    KnowledgeCaptureSubject,
)


KnowledgeCaptureFactory = Callable[
    [KnowledgeRecordRepository],
    KnowledgeCaptureApplicationService,
]


def _default_knowledge_capture_factory(
    repository: KnowledgeRecordRepository,
) -> KnowledgeCaptureApplicationService:
    """Build Knowledge Capture on the exact supplied repository scope."""
    return KnowledgeCaptureApplicationService(
        repository=repository,
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentKnowledgeIngestionRequest:
    """Immutable input for one canonical Document-derived Knowledge ingestion."""

    document_id: EntityId
    kind: str
    title: str
    content: str
    subject: KnowledgeCaptureSubject | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentKnowledgeIngestionResult:
    """Immutable result of one committed Document-to-Knowledge ingestion."""

    knowledge_record: KnowledgeRecord
    lineage: DocumentKnowledgeLineage


class DocumentKnowledgeIngestionDocumentNotFoundError(Exception):
    """Raised when the requested canonical Enterprise Document is absent."""


class DocumentKnowledgeIngestionApplicationService:
    """Coordinate one canonical Document-to-Knowledge ingestion use case."""

    def __init__(
        self,
        *,
        document_repository: EnterpriseDocumentRepository,
        transaction_coordinator: KnowledgeLineageTransactionCoordinator,
        knowledge_capture_factory: KnowledgeCaptureFactory | None = None,
    ) -> None:
        self._document_repository = document_repository
        self._transaction_coordinator = transaction_coordinator
        self._knowledge_capture_factory = (
            knowledge_capture_factory
            if knowledge_capture_factory is not None
            else _default_knowledge_capture_factory
        )

    def ingest(
        self,
        request: DocumentKnowledgeIngestionRequest,
    ) -> DocumentKnowledgeIngestionResult:
        """Ingest Knowledge derived from one existing canonical Document."""
        document = self._document_repository.get(
            request.document_id,
        )

        if document is None:
            raise DocumentKnowledgeIngestionDocumentNotFoundError(
                f"Enterprise Document '{request.document_id}' was not found."
            )

        def operation(
            knowledge_repository: KnowledgeRecordRepository,
            lineage_repository: DocumentKnowledgeLineageRepository,
        ) -> DocumentKnowledgeIngestionResult:
            capture_service = self._knowledge_capture_factory(
                knowledge_repository,
            )

            knowledge_record = capture_service.capture(
                KnowledgeCaptureRequest(
                    kind=request.kind,
                    title=request.title,
                    content=request.content,
                    source_type=document.source.source_type.value,
                    source_reference=document.source.source_reference,
                    subject=request.subject,
                )
            )

            lineage = DocumentKnowledgeLineage(
                document_id=document.id,
                knowledge_record_id=knowledge_record.id,
            )

            lineage_repository.add(lineage)

            return DocumentKnowledgeIngestionResult(
                knowledge_record=knowledge_record,
                lineage=lineage,
            )

        return self._transaction_coordinator.execute(
            operation,
        )
