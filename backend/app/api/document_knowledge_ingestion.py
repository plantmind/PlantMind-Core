"""Opt-in HTTP transport for canonical document Knowledge ingestion (AD-067)."""
from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import AfterValidator, BaseModel, ConfigDict, StrictStr

from app.core.runtime import Runtime
from app.domain.base import EntityId
from app.document_parsing.parser import (
    DocumentContentParserInvalidContentError,
    DocumentContentParserUnsupportedMediaTypeError,
)
from app.knowledge_lineage_transaction.coordinator import (
    KnowledgeLineageTransactionPostCommitCleanupError,
)
from app.services.application_facade import (
    ApplicationFacade, ApplicationFacadeDocumentIngestionNotConfiguredError,
)
from app.services.document_content_access_application_service import (
    DocumentContentAccessContentNotFoundError,
    DocumentContentAccessDocumentNotFoundError,
    DocumentContentAccessIntegrityError,
)
from app.services.document_knowledge_ingestion_application_service import (
    DocumentKnowledgeIngestionDocumentNotFoundError,
    DocumentKnowledgeIngestionResult,
)
from app.services.knowledge_capture_application_service import KnowledgeCaptureSubject
from app.services.parsed_document_knowledge_ingestion_application_service import (
    ParsedDocumentKnowledgeIngestionRequest,
)


def _nonblank(value: str) -> str:
    if not value.strip():
        raise ValueError("Must not be blank.")
    return value


NonblankText = Annotated[StrictStr, AfterValidator(_nonblank)]


class DocumentKnowledgeSubjectRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    subject_type: NonblankText
    subject_id: UUID


class DocumentKnowledgeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: NonblankText
    title: NonblankText
    subject: DocumentKnowledgeSubjectRequest | None = None


class DocumentKnowledgeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    document_id: UUID
    knowledge_record_id: UUID


def _response(result: DocumentKnowledgeIngestionResult, identity: EntityId) -> DocumentKnowledgeResponse:
    if not isinstance(result, DocumentKnowledgeIngestionResult):
        raise TypeError("Unexpected ingestion result.")
    doc, linked, record = result.lineage.document_id, result.lineage.knowledge_record_id, result.knowledge_record.id
    if not all(isinstance(value, EntityId) and isinstance(value.value, UUID)
               for value in (doc, linked, record)):
        raise TypeError("Unexpected result identity types.")
    if doc != identity or linked != record:
        raise ValueError("Unexpected result association.")
    return DocumentKnowledgeResponse(document_id=doc.value, knowledge_record_id=record.value)


def _http_error(error: Exception) -> HTTPException:
    mappings = (
        (ApplicationFacadeDocumentIngestionNotConfiguredError, 503, "INGESTION_NOT_CONFIGURED"),
        (DocumentContentAccessDocumentNotFoundError, 404, "DOCUMENT_NOT_FOUND"),
        (DocumentKnowledgeIngestionDocumentNotFoundError, 404, "DOCUMENT_NOT_FOUND"),
        (DocumentContentAccessContentNotFoundError, 409, "DOCUMENT_CONTENT_NOT_AVAILABLE"),
        (DocumentContentAccessIntegrityError, 409, "DOCUMENT_CONTENT_INTEGRITY_FAILURE"),
        (DocumentContentParserUnsupportedMediaTypeError, 422, "DOCUMENT_MEDIA_TYPE_UNSUPPORTED"),
        (DocumentContentParserInvalidContentError, 422, "DOCUMENT_CONTENT_INVALID"),
    )
    for kind, status_code, code in mappings:
        if isinstance(error, kind):
            return HTTPException(status_code=status_code, detail={"code": code})
    committed = isinstance(error, KnowledgeLineageTransactionPostCommitCleanupError)
    return HTTPException(status_code=500, detail={
        "code": "INGESTION_COMMITTED_CLEANUP_FAILED" if committed else "INGESTION_FAILED",
        "persistence_outcome": "committed" if committed else "unknown",
        "retry_recommended": False,
    })


def create_router(*, facade: ApplicationFacade, runtime: Runtime) -> APIRouter:
    """Caller owns the facade, runtime, middleware and host lifecycle."""
    router = APIRouter()

    def require_admission() -> None:
        if not runtime.is_request_admission_enabled:
            raise HTTPException(status_code=503,
                detail="PlantMind is not accepting operational requests.")

    @router.post("/documents/{document_id}/knowledge", status_code=201,
                 response_model=DocumentKnowledgeResponse, dependencies=[Depends(require_admission)])
    def ingest(document_id: UUID, request: DocumentKnowledgeRequest) -> DocumentKnowledgeResponse:
        try:
            identity = EntityId(value=document_id)
            subject = None if request.subject is None else KnowledgeCaptureSubject(
                subject_type=request.subject.subject_type,
                subject_id=EntityId(value=request.subject.subject_id),
            )
            command = ParsedDocumentKnowledgeIngestionRequest(
                document_id=identity, kind=request.kind, title=request.title, subject=subject,
            )
            return _response(facade.ingest_document_knowledge(command), identity)
        except Exception as error:
            raise _http_error(error) from error

    return router
