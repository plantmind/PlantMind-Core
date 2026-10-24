"""Explicit orchestration of parsing followed by canonical Knowledge ingestion."""
from __future__ import annotations

from dataclasses import dataclass
from app.domain.base import EntityId
from app.domain.document_content import DocumentContentDescriptor
from app.services.document_content_parsing_application_service import (
    DocumentContentParsingApplicationService, DocumentContentParsingRequest,
    DocumentContentParsingResult,
)
from app.services.document_knowledge_ingestion_application_service import (
    DocumentKnowledgeIngestionApplicationService, DocumentKnowledgeIngestionRequest,
    DocumentKnowledgeIngestionResult,
)
from app.services.knowledge_capture_application_service import KnowledgeCaptureSubject


@dataclass(frozen=True, slots=True, kw_only=True)
class ParsedDocumentKnowledgeIngestionRequest:
    """Explicit request; content and provenance are not caller overrides."""
    document_id: EntityId
    kind: str
    title: str
    subject: KnowledgeCaptureSubject | None = None


class ParsedDocumentKnowledgeIngestionApplicationService:
    """Delegate without owning transactions, retries or default host wiring."""

    def __init__(self, *, parsing_service: DocumentContentParsingApplicationService,
                 ingestion_service: DocumentKnowledgeIngestionApplicationService) -> None:
        self._parsing_service = parsing_service
        self._ingestion_service = ingestion_service

    def ingest(self, request: ParsedDocumentKnowledgeIngestionRequest) -> DocumentKnowledgeIngestionResult:
        if not isinstance(request, ParsedDocumentKnowledgeIngestionRequest):
            raise TypeError("Expected ParsedDocumentKnowledgeIngestionRequest.")
        if not isinstance(request.document_id, EntityId):
            raise TypeError("document_id must be an EntityId.")
        parsed = self._parsing_service.parse(
            DocumentContentParsingRequest(document_id=request.document_id)
        )
        if not isinstance(parsed, DocumentContentParsingResult):
            raise TypeError("Expected DocumentContentParsingResult.")
        if not isinstance(parsed.descriptor, DocumentContentDescriptor):
            raise TypeError("Expected DocumentContentDescriptor.")
        if not isinstance(parsed.text, str):
            raise TypeError("Parsed text must be a string.")
        if parsed.descriptor.document_id != request.document_id:
            raise ValueError("Parsed document identity does not match the request.")
        if not parsed.text.strip():
            raise ValueError("Parsed text must not be empty or whitespace-only.")
        return self._ingestion_service.ingest(DocumentKnowledgeIngestionRequest(
            document_id=request.document_id, kind=request.kind, title=request.title,
            content=parsed.text, subject=request.subject,
        ))
