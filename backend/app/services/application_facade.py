"""PlantMind application facade."""

from __future__ import annotations

from uuid import uuid4

from app.domain.observation import Observation
from app.services.integration_gateway import IntegrationGateway
from app.services.orchestration.workflow import WorkflowExecution
from app.domain.operational_workload_evidence import (
    ApplicationFacadeEntryEvidence,
)

from app.services.parsed_document_knowledge_ingestion_application_service import (
    ParsedDocumentKnowledgeIngestionApplicationService,
    ParsedDocumentKnowledgeIngestionRequest,
)
from app.services.document_knowledge_ingestion_application_service import (
    DocumentKnowledgeIngestionResult,
)


class ApplicationFacadeDocumentIngestionNotConfiguredError(RuntimeError):
    """The opt-in document ingestion dependency has not been supplied."""


class ApplicationFacade:
    """Stable application-level entry point.

    External interfaces should use this facade instead of depending
    directly on internal orchestration or reasoning services.
    """

    def __init__(
        self,
        gateway: IntegrationGateway | None = None,
        *,
        parsed_document_knowledge_ingestion_service: ParsedDocumentKnowledgeIngestionApplicationService | None = None,
    ) -> None:
        self._gateway = gateway or IntegrationGateway()
        self._parsed_document_knowledge_ingestion_service = parsed_document_knowledge_ingestion_service

    def analyze(
        self,
        observations: tuple[Observation, ...],
    ) -> WorkflowExecution:
        """Run one complete PlantMind analysis workflow."""
        facade_entry_evidence = ApplicationFacadeEntryEvidence(
            workload_id=uuid4()
        )

        return self._gateway.execute(
            observations,
            facade_entry_evidence=facade_entry_evidence,
        )

    def ingest_document_knowledge(
        self,
        request: ParsedDocumentKnowledgeIngestionRequest,
    ) -> DocumentKnowledgeIngestionResult:
        """Explicitly delegate ingestion; no default wiring or automatic retry."""
        if self._parsed_document_knowledge_ingestion_service is None:
            raise ApplicationFacadeDocumentIngestionNotConfiguredError(
                "Document knowledge ingestion is not configured."
            )
        return self._parsed_document_knowledge_ingestion_service.ingest(request)
