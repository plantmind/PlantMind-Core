"""RFC-083 managed HTTP host with canonical SQLite/filesystem resources owned by the caller."""
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
def local(composition_builder):
    assert not Path(gettempdir()).resolve().is_relative_to(Path(__file__).resolve().parents[2])
    with TemporaryDirectory(prefix="PlantMind-RFC083-") as directory:
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
                return composition_builder(parsed_document_knowledge_ingestion_service=Service(
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


from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.api.document_knowledge_ingestion_host import create_app
from app.core.composition.composition_root import (
    CompositionRoot,
    build_platform_composition,
)


@pytest.fixture(params=(CompositionRoot.build, build_platform_composition),
                ids=("composition-root", "compatibility-factory"))
def composition_builder(request):
    return request.param


def post(client, identity, **extra):
    return client.post(f"/documents/{identity}/knowledge",
                       json={"kind": "procedure", "title": "Synthetic knowledge", **extra})


def payloads(storage):
    return {path: path.read_bytes() for path in storage.rglob("*.bin")}


def test_managed_host_persists_lineage_and_preserves_caller_resources(local, monkeypatch):
    platform, _, save, counts, factory, parsing, storage, engine = local
    text = "  نص عربي\r\nSecond line  "
    document = save(b"\xef\xbb\xbf" + text.encode("utf-8"))
    before = payloads(storage)
    facade = platform.application_facade
    actual_ingest = facade.ingest_document_knowledge
    calls, operational_calls, disposed = [], [], []

    def ingest(request):
        calls.append(request)
        return actual_ingest(request)

    def operational(*args, **kwargs):
        operational_calls.append((args, kwargs))
        raise AssertionError("The host must not request an operational transition.")

    with monkeypatch.context() as patch:
        original_dispose = engine.dispose

        def dispose(*args, **kwargs):
            disposed.append((args, kwargs))
            return original_dispose(*args, **kwargs)

        patch.setattr(engine, "dispose", dispose)
        patch.setattr(facade, "ingest_document_knowledge", ingest)
        patch.setattr(platform.operational_transition_application_service,
                      "request_operational", operational)
        assert platform.container.resolve(ApplicationFacade) is facade
        assert platform.operational_transition_application_service.application_facade is facade
        assert platform.runtime.is_request_admission_enabled is False
        app = create_app(platform=platform)
        assert calls == operational_calls == disposed == [] and counts() == (0, 0)

        with factory() as caller_session:
            assert caller_session.execute(select(1)).scalar_one() == 1
            with TestClient(app) as client:
                assert platform.runtime.is_request_admission_enabled is True
                assert client.get("/").json()["runtime"]["status"] == platform.runtime.state.value
                assert client.get("/health").json() == jsonable_encoder(platform.health.get_status())
                assert calls == operational_calls == [] and counts() == (0, 0)
                response = post(client, document.id)
                assert response.status_code == 201
                body = response.json()
                assert set(body) == {"document_id", "knowledge_record_id"}
                assert body["document_id"] == str(document.id)
                knowledge = EntityId.from_string(body["knowledge_record_id"])
                assert str(knowledge) == body["knowledge_record_id"]
                assert len(calls) == 1 and counts() == (1, 1)

            assert platform.runtime.is_request_admission_enabled is False
            assert len(calls) == 1 and operational_calls == disposed == []
            assert caller_session.execute(select(1)).scalar_one() == 1
            record = caller_session.get(KnowledgeRow, knowledge.value)
            assert record is not None and record.content == text.strip()
            assert record.provenance_source_reference == "TEST-ONLY"
            assert caller_session.get(LineageRow, (document.id.value, knowledge.value)) is not None

        with engine.connect() as connection:
            assert connection.scalar(select(1)) == 1
        assert parsing.parse(DocumentContentParsingRequest(document_id=document.id)).text == text
        assert payloads(storage) == before
        later = save(b"Caller resources remain usable after host shutdown")
        assert parsing.parse(DocumentContentParsingRequest(document_id=later.id)).text == (
            "Caller resources remain usable after host shutdown"
        )
        assert all(path.read_bytes() == data for path, data in before.items())
        assert counts() == (1, 1) and disposed == []


def test_closed_host_precedes_validation_and_open_invalid_requests_do_not_write(local, monkeypatch):
    platform, _, save, counts, _, _, storage, _ = local
    document = save()
    before, calls = payloads(storage), []

    def forbidden(request):
        calls.append(request)
        raise AssertionError("Rejected requests must not reach the facade.")

    monkeypatch.setattr(platform.application_facade, "ingest_document_knowledge", forbidden)
    app = create_app(platform=platform)
    closed = {"detail": "PlantMind is not accepting operational requests."}
    client = TestClient(app)
    try:
        assert platform.runtime.is_request_admission_enabled is False
        assert post(client, document.id).json() == closed
        invalid = client.post("/documents/not-a-uuid/knowledge", json={"unexpected": True})
        assert invalid.status_code == 503 and invalid.json() == closed
        assert client.get("/").status_code == client.get("/health").status_code == 200
        assert client.get("/analysis/health").status_code == 503
    finally:
        client.close()
    assert counts() == (0, 0) and payloads(storage) == before and calls == []

    with TestClient(app) as client:
        assert platform.runtime.is_request_admission_enabled is True
        assert post(client, "not-a-uuid").status_code == 422
        assert post(client, document.id, content="override").status_code == 422
        assert counts() == (0, 0) and payloads(storage) == before and calls == []

    assert platform.runtime.is_request_admission_enabled is False
    client = TestClient(app)
    try:
        response = post(client, document.id)
        assert response.status_code == 503 and response.json() == closed
    finally:
        client.close()
    assert counts() == (0, 0) and payloads(storage) == before and calls == []


def test_managed_unconfigured_host_keeps_existing_not_configured_response(composition_builder):
    platform = composition_builder()
    assert platform.runtime.is_request_admission_enabled is False
    with TestClient(create_app(platform=platform)) as client:
        assert platform.runtime.is_request_admission_enabled is True
        response = post(client, EntityId.new())
        assert response.status_code == 503
        assert response.json() == {"detail": {"code": "INGESTION_NOT_CONFIGURED"}}
    assert platform.runtime.is_request_admission_enabled is False


@pytest.mark.parametrize("payload,media,status,code", [
    (b"\xff", "text/plain", 422, "DOCUMENT_CONTENT_INVALID"),
    (b"opaque", "application/octet-stream", 422, "DOCUMENT_MEDIA_TYPE_UNSUPPORTED"),
    (b"", "text/plain", 500, "INGESTION_FAILED"),
])
def test_managed_host_content_rejection_does_not_write(local, payload, media, status, code):
    platform, _, save, counts, _, _, storage, _ = local
    document = save(payload, media)
    before = payloads(storage)
    with TestClient(create_app(platform=platform)) as client:
        response = post(client, document.id)
        assert response.status_code == status and response.json()["detail"]["code"] == code
        if status == 500:
            assert response.json()["detail"]["persistence_outcome"] == "unknown"
            assert response.json()["detail"]["retry_recommended"] is False
    assert counts() == (0, 0) and payloads(storage) == before
    assert platform.runtime.is_request_admission_enabled is False


@pytest.mark.parametrize("state,status,code", [
    ("missing-document", 404, "DOCUMENT_NOT_FOUND"),
    ("registered-without-content", 409, "DOCUMENT_CONTENT_NOT_AVAILABLE"),
    ("corrupt-payload", 409, "DOCUMENT_CONTENT_INTEGRITY_FAILURE"),
    ("descriptor-without-payload", 409, "DOCUMENT_CONTENT_INTEGRITY_FAILURE"),
])
def test_managed_host_preserves_independent_content_state_outcomes(local, state, status, code):
    platform, _, save, counts, factory, _, storage, _ = local
    documents, contents = Documents(factory), Contents(factory)
    if state == "missing-document":
        identity = EntityId.new()
        assert documents.get(identity) is None
    elif state == "registered-without-content":
        document = Registrar(repository=documents).register(Registration(
            document_type="procedure", title="Registered without content",
            source_type="document_control", source_reference="TEST-ONLY",
        ))
        identity = document.id
        assert documents.get(identity) == document and contents.get(identity) is None
        assert payloads(storage) == {}
    else:
        document = save(b"original")
        identity = document.id
        assert contents.get(identity) is not None
        files = list(storage.rglob("*.bin"))
        assert len(files) == 1 and files[0].read_bytes() == b"original"
        if state == "corrupt-payload":
            files[0].write_bytes(b"Original")  # Fixture-owned temporary payload only.
        else:
            files[0].unlink()  # Fixture-owned temporary payload only; descriptor remains.
    before_document = documents.get(identity)
    before_content, before_payloads = contents.get(identity), payloads(storage)
    with TestClient(create_app(platform=platform)) as client:
        response = post(client, identity)
        assert response.status_code == status
        assert response.json() == {"detail": {"code": code}}
    assert counts() == (0, 0) and payloads(storage) == before_payloads
    assert documents.get(identity) == before_document and contents.get(identity) == before_content
    assert platform.runtime.is_request_admission_enabled is False


def test_managed_host_preserves_real_lineage_failure_rollback(local):
    platform, _, save, counts, _, _, _, _ = local
    document, observed = save(), []

    def fail(_mapper, connection, _target):
        observed.append(connection.scalar(select(func.count()).select_from(KnowledgeRow)))
        raise RuntimeError("PRIVATE SQL PATH")

    event.listen(LineageRow, "before_insert", fail)
    try:
        with TestClient(create_app(platform=platform)) as client:
            response = post(client, document.id)
    finally:
        event.remove(LineageRow, "before_insert", fail)
    assert response.status_code == 500 and "PRIVATE" not in response.text
    assert response.json()["detail"] == {"code": "INGESTION_FAILED",
        "persistence_outcome": "unknown", "retry_recommended": False}
    assert observed == [1] and counts() == (0, 0)
    assert platform.runtime.is_request_admission_enabled is False


def test_managed_host_reports_committed_cleanup_failure_without_retry(local):
    _, build, save, counts, _, _, _, engine = local
    document, closes = save(), []

    class ClosingSession(Session):
        def close(self):
            super().close()
            closes.append(1)
            raise RuntimeError("PRIVATE cleanup")

    platform = build(sessionmaker(bind=engine, class_=ClosingSession,
                                 expire_on_commit=False, autoflush=False))
    assert platform.runtime.is_request_admission_enabled is False
    with TestClient(create_app(platform=platform)) as client:
        response = post(client, document.id)
        assert response.status_code == 500
        assert response.json() == {"detail": {
            "code": "INGESTION_COMMITTED_CLEANUP_FAILED",
            "persistence_outcome": "committed", "retry_recommended": False}}
    assert "PRIVATE" not in response.text and closes == [1] and counts() == (1, 1)
    assert platform.runtime.is_request_admission_enabled is False


def test_managed_host_unknown_result_after_write_does_not_claim_rollback_or_retry(local, monkeypatch):
    platform, _, save, counts, _, _, _, _ = local
    document = save()
    facade = platform.application_facade
    actual, calls = facade.ingest_document_knowledge, []

    def wrong_result(request):
        calls.append(request)
        actual(request)
        return object()

    monkeypatch.setattr(facade, "ingest_document_knowledge", wrong_result)
    with TestClient(create_app(platform=platform)) as client:
        response = post(client, document.id)
    assert response.status_code == 500
    assert response.json()["detail"] == {"code": "INGESTION_FAILED",
        "persistence_outcome": "unknown", "retry_recommended": False}
    assert len(calls) == 1 and counts() == (1, 1)
    assert platform.runtime.is_request_admission_enabled is False
