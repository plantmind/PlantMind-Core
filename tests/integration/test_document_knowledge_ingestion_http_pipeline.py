"""RFC-081 HTTP journeys with predecessor real-adapter fixtures; temporary SQLite only."""
from io import BytesIO
from app.services.application_facade import (
    ApplicationFacade, ApplicationFacadeDocumentIngestionNotConfiguredError,
)
from pathlib import Path
from tempfile import TemporaryDirectory, gettempdir

import pytest
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session, sessionmaker
from app.domain.base import DomainException, EntityId
from app.infrastructure.document.models import EnterpriseDocumentRow
from app.infrastructure.document.repository import SQLAlchemyEnterpriseDocumentRepository as Documents
from app.infrastructure.document_content.models import DocumentContentDescriptorRow
from app.infrastructure.document_content.repository import SQLAlchemyDocumentContentRepository as Contents
from app.infrastructure.document_content.filesystem_store import FilesystemDocumentContentStore as Store
from app.infrastructure.knowledge.models import KnowledgeRecordRow as KnowledgeRow
from app.infrastructure.document_knowledge_lineage.models import DocumentKnowledgeLineageRow as LineageRow
from app.infrastructure.knowledge_lineage_transaction.coordinator import SQLAlchemyKnowledgeLineageTransactionCoordinator as Coordinator
from app.knowledge_lineage_transaction.coordinator import KnowledgeLineageTransactionPostCommitCleanupError
from app.services.enterprise_document_registration_application_service import (
    EnterpriseDocumentRegistrationApplicationService as Registrar, EnterpriseDocumentRegistrationRequest as Registration)
from app.services.document_content_establishment_application_service import (
    DocumentContentEstablishmentApplicationService as Establishment, DocumentContentEstablishmentRequest as EstablishRequest)
from app.services.document_content_access_application_service import (
    DocumentContentAccessApplicationService as Access, DocumentContentAccessDocumentNotFoundError,
    DocumentContentAccessIntegrityError)
from app.core.composition.document_content_parsing import build_document_content_parsing_composition as compose
from app.services.document_content_parsing_application_service import DocumentContentParsingRequest
from app.services.document_knowledge_ingestion_application_service import DocumentKnowledgeIngestionApplicationService as Ingestion
from app.services.parsed_document_knowledge_ingestion_application_service import (
    ParsedDocumentKnowledgeIngestionApplicationService as Service, ParsedDocumentKnowledgeIngestionRequest as Request)
from app.document_parsing.parser import DocumentContentParserInvalidContentError, DocumentContentParserUnsupportedMediaTypeError


@pytest.fixture
def local():
    assert not Path(gettempdir()).resolve().is_relative_to(Path(__file__).resolve().parents[2])
    with TemporaryDirectory(prefix="PlantMind-RFC081-") as directory:
        folder = Path(directory).resolve()
        storage = folder / "payloads"
        storage.mkdir()
        engine = create_engine("sqlite+pysqlite:///" + str(folder / "test.sqlite"))
        try:
            for row in (EnterpriseDocumentRow, DocumentContentDescriptorRow, KnowledgeRow, LineageRow):
                row.__table__.create(engine)
            factory = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
            documents, contents, store = Documents(factory), Contents(factory), Store(storage)
            registrar = Registrar(repository=documents)
            establishment = Establishment(document_repository=documents,
                content_repository=contents, content_store=store)
            parsing = compose(content_access_service=Access(document_repository=documents,
                content_repository=contents, content_store=store)).application_service
            def build(transaction_factory=factory):
                return ApplicationFacade(parsed_document_knowledge_ingestion_service=Service(
                    parsing_service=parsing, ingestion_service=Ingestion(document_repository=documents,
                        transaction_coordinator=Coordinator(transaction_factory))))
            def save(payload=b"Original text", media_type="text/plain"):
                doc = registrar.register(Registration(document_type="procedure", title="Synthetic",
                    source_type="document_control", source_reference="TEST-ONLY"))
                with BytesIO(payload) as source:
                    establishment.establish(EstablishRequest(document_id=doc.id,
                        media_type=media_type, source=source))
                return doc
            def counts():
                with factory() as session:
                    return tuple(session.scalar(select(func.count()).select_from(row))
                                 for row in (KnowledgeRow, LineageRow))
            yield build(), build, save, counts, factory, parsing, storage, engine
        finally:
            engine.dispose()


from contextlib import contextmanager
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.document_knowledge_ingestion import create_router
from app.api.request_admission import RequestAdmissionMiddleware
from app.core.runtime import Runtime


@contextmanager
def http_client(facade, runtime):
    app = FastAPI()
    app.add_middleware(RequestAdmissionMiddleware, runtime=runtime)
    app.include_router(create_router(facade=facade, runtime=runtime))
    with TestClient(app) as client:
        yield client


@pytest.fixture
def http(local):
    runtime = Runtime()
    runtime.enable_request_admission()
    with http_client(local[0], runtime) as client:
        yield client, runtime, local


def post(client, identity, **extra):
    return client.post(f"/documents/{identity}/knowledge",
                       json={"kind": "procedure", "title": "Synthetic knowledge", **extra})


def test_persists_real_knowledge_and_lineage_via_http(http):
    client, runtime, local = http
    _, _, save, counts, factory, parsing, _, engine = local
    text = "  نص عربي\r\nSecond line  "
    doc = save(b"\xef\xbb\xbf" + text.encode("utf-8"))
    assert parsing.parse(DocumentContentParsingRequest(document_id=doc.id)).text == text
    assert counts() == (0, 0)
    before = runtime.state, runtime.is_request_admission_enabled
    response = post(client, doc.id)
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"document_id", "knowledge_record_id"} and body["document_id"] == str(doc.id)
    knowledge = EntityId.from_string(body["knowledge_record_id"])
    engine.dispose()
    assert counts() == (1, 1)
    with factory() as session:
        record = session.get(KnowledgeRow, knowledge.value)
        assert record.content == text.strip()
        assert record.provenance_source_reference == "TEST-ONLY"
        assert session.get(LineageRow, (doc.id.value, knowledge.value)) is not None
    assert before == (runtime.state, runtime.is_request_admission_enabled)


@pytest.mark.parametrize("payload,media,status,code", [
    (b"", "text/plain", 500, "INGESTION_FAILED"),
    (b" \n\t", "text/plain", 500, "INGESTION_FAILED"),
    (b"\xff", "text/plain", 422, "DOCUMENT_CONTENT_INVALID"),
    (b"opaque", "application/octet-stream", 422, "DOCUMENT_MEDIA_TYPE_UNSUPPORTED"),
])
def test_content_rejection_never_writes(http, payload, media, status, code):
    client, _, local = http
    doc = local[2](payload, media)
    response = post(client, doc.id)
    assert response.status_code == status and response.json()["detail"]["code"] == code
    assert local[3]() == (0, 0)


def test_missing_document_is_not_found_via_http(http):
    client, _, local = http
    identity = EntityId.new()
    assert Documents(local[4]).get(identity) is None
    response = post(client, identity)
    assert response.status_code == 404
    assert response.json() == {"detail": {"code": "DOCUMENT_NOT_FOUND"}}
    assert local[3]() == (0, 0)


def test_registered_document_without_content_is_unavailable_via_http(http):
    client, _, local = http
    documents, contents, storage = Documents(local[4]), Contents(local[4]), local[6]
    doc = Registrar(repository=documents).register(Registration(
        document_type="procedure", title="Registered without content",
        source_type="document_control", source_reference="TEST-ONLY",
    ))
    assert documents.get(doc.id) == doc
    assert contents.get(doc.id) is None
    assert not list(storage.rglob("*.bin"))
    response = post(client, doc.id)
    assert response.status_code == 409
    assert response.json() == {"detail": {"code": "DOCUMENT_CONTENT_NOT_AVAILABLE"}}
    assert local[3]() == (0, 0)
    assert documents.get(doc.id) == doc and contents.get(doc.id) is None
    assert not list(storage.rglob("*.bin"))


def test_corrupted_payload_is_integrity_failure_via_http(http):
    client, _, local = http
    doc = local[2](b"original")
    contents, storage = Contents(local[4]), local[6]
    descriptor = contents.get(doc.id)
    assert descriptor is not None
    files = list(storage.rglob("*.bin"))
    assert len(files) == 1 and files[0].read_bytes() == b"original"
    files[0].write_bytes(b"Original")  # Only the fixture's temporary payload.
    response = post(client, doc.id)
    assert response.status_code == 409
    assert response.json() == {"detail": {"code": "DOCUMENT_CONTENT_INTEGRITY_FAILURE"}}
    assert local[3]() == (0, 0)
    assert contents.get(doc.id) == descriptor
    assert files[0].read_bytes() == b"Original"  # No automatic repair.


def test_descriptor_without_payload_is_integrity_failure_via_http(http):
    client, _, local = http
    doc = local[2](b"original")
    contents, storage = Contents(local[4]), local[6]
    descriptor = contents.get(doc.id)
    assert descriptor is not None
    files = list(storage.rglob("*.bin"))
    assert len(files) == 1 and files[0].read_bytes() == b"original"
    files[0].unlink()  # Only the fixture's temporary payload; descriptor stays.
    response = post(client, doc.id)
    assert response.status_code == 409
    assert response.json() == {"detail": {"code": "DOCUMENT_CONTENT_INTEGRITY_FAILURE"}}
    assert local[3]() == (0, 0)
    assert Documents(local[4]).get(doc.id) == doc
    assert contents.get(doc.id) == descriptor  # No descriptor deletion or repair.
    assert not list(storage.rglob("*.bin"))


def test_closed_admission_invalid_input_and_default_facade_make_no_writes(http):
    client, runtime, local = http
    doc, storage = local[2](), local[6]
    before = {p: p.read_bytes() for p in storage.rglob("*.bin")}
    initial = runtime.state
    runtime.disable_request_admission()
    assert post(client, doc.id).status_code == 503
    runtime.enable_request_admission()
    assert post(client, doc.id, content="override").status_code == 422
    with http_client(ApplicationFacade(), runtime) as disabled:
        assert post(disabled, doc.id).json() == {"detail": {"code": "INGESTION_NOT_CONFIGURED"}}
    assert local[3]() == (0, 0) and runtime.state is initial
    assert before == {p: p.read_bytes() for p in storage.rglob("*.bin")}


def test_explicit_repetition_is_not_silently_deduplicated(http):
    client, _, local = http
    doc = local[2]()
    first, second = post(client, doc.id), post(client, doc.id)
    assert first.status_code == second.status_code == 201
    assert first.json()["knowledge_record_id"] != second.json()["knowledge_record_id"]
    assert local[3]() == (2, 2)


def test_lineage_failure_rolls_back_through_http(http):
    client, _, local = http
    doc, observed = local[2](), []
    def fail(_mapper, connection, _target):
        observed.append(connection.scalar(select(func.count()).select_from(KnowledgeRow)))
        raise RuntimeError("PRIVATE SQL PATH")
    event.listen(LineageRow, "before_insert", fail)
    try:
        response = post(client, doc.id)
    finally:
        event.remove(LineageRow, "before_insert", fail)
    assert response.status_code == 500 and "PRIVATE" not in response.text
    assert response.json()["detail"]["persistence_outcome"] == "unknown"
    assert observed == [1] and local[3]() == (0, 0)


def test_cleanup_after_commit_reports_committed_without_retry(http):
    _, runtime, local = http
    doc, closes = local[2](), []
    class ClosingSession(Session):
        def close(self):
            super().close()
            closes.append(1)
            raise RuntimeError("PRIVATE cleanup")
    facade = local[1](sessionmaker(bind=local[7], class_=ClosingSession,
                                   expire_on_commit=False, autoflush=False))
    with http_client(facade, runtime) as client:
        response = post(client, doc.id)
    assert response.status_code == 500 and response.json() == {"detail": {
        "code": "INGESTION_COMMITTED_CLEANUP_FAILED",
        "persistence_outcome": "committed", "retry_recommended": False}}
    assert "PRIVATE" not in response.text and closes == [1] and local[3]() == (1, 1)


def test_malformed_result_after_real_write_reports_unknown_not_rollback(http, monkeypatch):
    client, _, local = http
    doc = local[2]()
    actual = local[0].ingest_document_knowledge
    calls = []
    def wrong_result(request):
        calls.append(request)
        actual(request)
        return object()
    monkeypatch.setattr(local[0], "ingest_document_knowledge", wrong_result)
    response = post(client, doc.id)
    assert response.status_code == 500
    assert response.json()["detail"] == {"code": "INGESTION_FAILED",
        "persistence_outcome": "unknown", "retry_recommended": False}
    assert len(calls) == 1 and local[3]() == (1, 1)
