"""AD-070 HTTP preparation and explicit ingestion with caller-owned local resources."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory, gettempdir
from types import SimpleNamespace

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session, sessionmaker

from app.api.document_knowledge_ingestion_host import create_app
from app.core.composition.composition_root import CompositionRoot, build_platform_composition
from app.core.composition.document_content_parsing import (
    build_document_content_parsing_composition as compose_parsing,
)
from app.document_content.repository import DocumentContentAlreadyExistsError
from app.domain.base import DomainException, EntityId
from app.domain.document_content import (
    DocumentContentDescriptor,
    DocumentContentDigest,
    DocumentContentMediaType,
)
from app.infrastructure.document.models import EnterpriseDocumentRow
from app.infrastructure.document.repository import SQLAlchemyEnterpriseDocumentRepository as Documents
from app.infrastructure.document_content.filesystem_store import FilesystemDocumentContentStore as Store
from app.infrastructure.document_content.models import DocumentContentDescriptorRow
from app.infrastructure.document_content.repository import SQLAlchemyDocumentContentRepository as Contents
from app.infrastructure.document_knowledge_lineage.models import DocumentKnowledgeLineageRow as LineageRow
from app.infrastructure.knowledge.models import KnowledgeRecordRow as KnowledgeRow
from app.infrastructure.knowledge_lineage_transaction.coordinator import (
    SQLAlchemyKnowledgeLineageTransactionCoordinator as Coordinator,
)
from app.services.document_content_access_application_service import (
    DocumentContentAccessApplicationService as Access,
)
from app.services.document_content_establishment_application_service import (
    DocumentContentEstablishmentApplicationService as Establishment,
    DocumentContentEstablishmentRequest as EstablishRequest,
)
from app.services.document_content_parsing_application_service import DocumentContentParsingRequest
from app.services.document_knowledge_ingestion_application_service import (
    DocumentKnowledgeIngestionApplicationService as Ingestion,
)
from app.services.enterprise_document_registration_application_service import (
    EnterpriseDocumentRegistrationApplicationService as Registrar,
    EnterpriseDocumentRegistrationRequest as Registration,
)
from app.services.parsed_document_knowledge_ingestion_application_service import (
    ParsedDocumentKnowledgeIngestionApplicationService as ParsedIngestion,
)


ADMISSION_CLOSED = {"detail": "PlantMind is not accepting operational requests."}


@pytest.fixture(params=(CompositionRoot.build, build_platform_composition),
                ids=("composition-root", "compatibility-factory"))
def composition_builder(request):
    return request.param


@pytest.fixture
def local(composition_builder):
    """Build infrastructure/services only; each HTTP journey creates its own document."""
    assert not Path(gettempdir()).resolve().is_relative_to(Path(__file__).resolve().parents[2])
    with TemporaryDirectory(prefix="PlantMind-RFC084-") as directory:
        root = Path(directory).resolve()
        storage = root / "payloads"
        storage.mkdir()
        engine = create_engine("sqlite+pysqlite:///" + str(root / "local.sqlite"))
        try:
            rows = (EnterpriseDocumentRow, DocumentContentDescriptorRow, KnowledgeRow, LineageRow)
            for row in rows:
                row.__table__.create(engine)
            factory = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
            documents, contents, store = Documents(factory), Contents(factory), Store(storage)
            registrar = Registrar(repository=documents)
            establishment = Establishment(document_repository=documents,
                content_repository=contents, content_store=store)
            parsing = compose_parsing(content_access_service=Access(
                document_repository=documents, content_repository=contents,
                content_store=store)).application_service

            def build(*, configured=True, transaction_factory=factory):
                if not configured:
                    return composition_builder()
                return composition_builder(parsed_document_knowledge_ingestion_service=ParsedIngestion(
                    parsing_service=parsing, ingestion_service=Ingestion(document_repository=documents,
                        transaction_coordinator=Coordinator(transaction_factory))))

            def counts():
                with factory() as session:
                    return tuple(session.scalar(select(func.count()).select_from(row)) for row in rows)

            yield SimpleNamespace(platform=build(), build=build, documents=documents,
                contents=contents, store=store, registrar=registrar, establishment=establishment,
                parsing=parsing, factory=factory, storage=storage, engine=engine, counts=counts)
        finally:
            engine.dispose()


def host(local, *, platform=None, registrar=None, establishment=None):
    return create_app(platform=local.platform if platform is None else platform,
        document_registration_service=local.registrar if registrar is None else registrar,
        document_content_establishment_service=(
            local.establishment if establishment is None else establishment))


def metadata(**changes):
    return {"document_type": " Procedure ", "title": "  Synthetic procedure  ",
        "source_type": " DOCUMENT_CONTROL ", "source_reference": " TEST-ONLY ", **changes}


def register(client, **changes):
    return client.post("/documents", json=metadata(**changes))


def identity(response):
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"document_id", "document_type", "title", "source_type", "source_reference"}
    result = EntityId.from_string(body["document_id"])
    assert str(result) == body["document_id"]
    assert "location" not in response.headers
    return result


def put(client, document_id, payload, media="text/plain"):
    return client.put(f"/documents/{document_id}/content", content=payload,
                      headers={"Content-Type": media})


def ingest(client, document_id):
    return client.post(f"/documents/{document_id}/knowledge",
        json={"kind": "procedure", "title": "Synthetic knowledge"})


def payload_snapshot(storage):
    return {str(path.relative_to(storage)): (path.read_bytes(), path.stat().st_ino,
            path.stat().st_mtime_ns) for path in storage.rglob("*.bin")}


def assert_content_response(response, document_id, payload, media="text/plain"):
    assert response.status_code == 200
    assert response.json() == {"document_id": str(document_id), "media_type": media,
        "byte_length": len(payload), "digest": sha256(payload).hexdigest()}


def assert_error(response, status, code):
    assert response.status_code == status
    assert response.json() == {"detail": {"code": code}}
    assert "PRIVATE" not in response.text


def test_full_managed_http_journey_preserves_caller_graph_and_exact_payload(local, monkeypatch):
    text = "  نص عربي\r\nSecond line  "
    payload = b"\xef\xbb\xbf" + text.encode("utf-8")
    platform = local.platform
    calls, sources, disposals, operational = [], [], [], []
    real_register = local.registrar.register
    real_establish = local.establishment.establish
    real_ingest = platform.application_facade.ingest_document_knowledge

    def registered(request):
        calls.append("register")
        return real_register(request)

    def established(request):
        calls.append("establish")
        sources.append(request.source)
        assert request.source.tell() == 0 and not request.source.closed
        return real_establish(request)

    def ingested(request):
        calls.append("ingest")
        return real_ingest(request)

    def forbidden_operational(*args, **kwargs):
        operational.append((args, kwargs))
        raise AssertionError("Preparation/ingestion must not request an operational transition.")

    with monkeypatch.context() as patch:
        real_dispose = local.engine.dispose

        def disposed(*args, **kwargs):
            disposals.append((args, kwargs))
            return real_dispose(*args, **kwargs)

        patch.setattr(local.registrar, "register", registered)
        patch.setattr(local.establishment, "establish", established)
        patch.setattr(platform.application_facade, "ingest_document_knowledge", ingested)
        patch.setattr(platform.operational_transition_application_service,
                      "request_operational", forbidden_operational)
        patch.setattr(local.engine, "dispose", disposed)
        assert local.counts() == (0, 0, 0, 0) and payload_snapshot(local.storage) == {}
        assert platform.runtime.is_request_admission_enabled is False
        app = host(local)
        assert calls == sources == disposals == operational == []

        with local.factory() as caller_session:
            assert caller_session.execute(select(1)).scalar_one() == 1
            with TestClient(app) as client:
                assert platform.runtime.is_request_admission_enabled is True
                assert client.get("/").json()["runtime"]["status"] == platform.runtime.state.value
                assert client.get("/health").json() == jsonable_encoder(platform.health.get_status())
                assert calls == [] and local.counts() == (0, 0, 0, 0)
                response = register(client)
                document_id = identity(response)
                assert response.json() == {"document_id": str(document_id),
                    "document_type": "procedure", "title": "Synthetic procedure",
                    "source_type": "document_control", "source_reference": "TEST-ONLY"}
                document = local.documents.get(document_id)
                assert document is not None and document.id == document_id
                assert document.document_type.value == "procedure"
                assert document.title == "Synthetic procedure"
                assert document.source.source_type.value == "document_control"
                assert document.source.source_reference == "TEST-ONLY"
                assert calls == ["register"] and local.counts() == (1, 0, 0, 0)
                assert payload_snapshot(local.storage) == {}

                response = put(client, document_id, payload, " Text/Plain ")
                assert_content_response(response, document_id, payload)
                descriptor = local.contents.get(document_id)
                assert descriptor == DocumentContentDescriptor(document_id=document_id,
                    media_type=DocumentContentMediaType(value="text/plain"), byte_length=len(payload),
                    digest=DocumentContentDigest(value=sha256(payload).hexdigest()))
                with local.store.open(document_id) as stored:
                    assert stored.read() == payload
                assert calls == ["register", "establish"] and local.counts() == (1, 1, 0, 0)
                assert len(sources) == 1 and sources[0].closed
                before = payload_snapshot(local.storage)

                response = ingest(client, document_id)
                assert response.status_code == 201
                assert set(response.json()) == {"document_id", "knowledge_record_id"}
                assert response.json()["document_id"] == str(document_id)
                knowledge_id = EntityId.from_string(response.json()["knowledge_record_id"])
                assert str(knowledge_id) == response.json()["knowledge_record_id"]
                assert calls == ["register", "establish", "ingest"]
                assert local.counts() == (1, 1, 1, 1)

            assert platform.runtime.is_request_admission_enabled is False
            assert calls == ["register", "establish", "ingest"]
            assert operational == disposals == []
            assert caller_session.execute(select(1)).scalar_one() == 1
            knowledge = caller_session.get(KnowledgeRow, knowledge_id.value)
            assert knowledge is not None and knowledge.content == text.strip()
            assert knowledge.provenance_source_reference == "TEST-ONLY"
            assert caller_session.get(LineageRow, (document_id.value, knowledge_id.value)) is not None

        with local.engine.connect() as connection:
            assert connection.scalar(select(1)) == 1
        assert local.documents.get(document_id) == document
        assert local.contents.get(document_id) == descriptor
        assert local.parsing.parse(DocumentContentParsingRequest(document_id=document_id)).text == text
        assert payload_snapshot(local.storage) == before and disposals == []

    # Explicit caller use after host shutdown still owns the same usable resources.
    later = local.registrar.register(Registration(document_type="procedure", title="Later caller use",
        source_type="document_control", source_reference="CALLER-AFTER-SHUTDOWN"))
    with BytesIO(b"Caller-owned resources remain usable") as source:
        local.establishment.establish(EstablishRequest(document_id=later.id,
            media_type="text/plain", source=source))
    assert local.parsing.parse(DocumentContentParsingRequest(document_id=later.id)).text == (
        "Caller-owned resources remain usable")
    assert local.counts() == (2, 2, 1, 1)


def test_equal_source_reference_does_not_deduplicate_http_registration(local):
    with TestClient(host(local)) as client:
        first = identity(register(client))
        second = identity(register(client))
    assert first != second
    first_document, second_document = local.documents.get(first), local.documents.get(second)
    assert first_document.source == second_document.source
    assert first_document.title == second_document.title == "Synthetic procedure"
    assert local.counts() == (2, 0, 0, 0) and payload_snapshot(local.storage) == {}


@pytest.mark.parametrize("payload,media", [
    (b"", "text/plain"),
    (b"\x00\xff\r\n\x80", "application/octet-stream"),
    (b"\xef\xbb\xbf" + "نص\r\n ".encode("utf-8"), "text/plain"),
])
def test_complete_repeat_and_conflicts_preserve_content_without_overwrite(local, payload, media):
    with TestClient(host(local)) as client:
        document_id = identity(register(client))
        assert_content_response(put(client, document_id, payload, media), document_id, payload, media)
        descriptor = local.contents.get(document_id)
        before = payload_snapshot(local.storage)
        assert_content_response(put(client, document_id, payload, media), document_id, payload, media)
        assert_error(put(client, document_id, payload + b"!", media), 409, "DOCUMENT_CONTENT_CONFLICT")
        assert_error(put(client, document_id, payload, "application/x-different"),
                     409, "DOCUMENT_CONTENT_CONFLICT")
    assert local.contents.get(document_id) == descriptor
    assert payload_snapshot(local.storage) == before and local.counts() == (1, 1, 0, 0)


def test_missing_document_and_descriptor_only_state_are_distinct(local):
    with TestClient(host(local)) as client:
        assert_error(put(client, EntityId.new(), b"absent"), 404, "DOCUMENT_NOT_FOUND")
        assert local.counts() == (0, 0, 0, 0) and payload_snapshot(local.storage) == {}
        document_id = identity(register(client))
        payload = b"descriptor exists without its payload"
        descriptor = DocumentContentDescriptor(document_id=document_id,
            media_type=DocumentContentMediaType(value="text/plain"), byte_length=len(payload),
            digest=DocumentContentDigest(value=sha256(payload).hexdigest()))
        local.contents.add(descriptor)
        assert_error(put(client, document_id, payload), 409, "DOCUMENT_CONTENT_INTEGRITY_FAILURE")
    assert local.documents.get(document_id) is not None
    assert local.contents.get(document_id) == descriptor
    assert payload_snapshot(local.storage) == {} and local.counts() == (1, 1, 0, 0)


def test_payload_only_mismatch_preserves_payload_and_matching_explicit_put_recovers(local):
    payload = b"immutable payload waiting for its descriptor\r\n"
    with TestClient(host(local)) as client:
        document_id = identity(register(client))
        with BytesIO(payload) as source:
            local.store.add(document_id, source)
        before = payload_snapshot(local.storage)
        assert local.contents.get(document_id) is None
        assert_error(put(client, document_id, b"different"), 409, "DOCUMENT_CONTENT_CONFLICT")
        assert local.contents.get(document_id) is None
        assert payload_snapshot(local.storage) == before and local.counts() == (1, 0, 0, 0)
        assert_content_response(put(client, document_id, payload), document_id, payload)
    assert local.contents.get(document_id).digest.value == sha256(payload).hexdigest()
    assert payload_snapshot(local.storage) == before and local.counts() == (1, 1, 0, 0)


def test_corrupted_complete_payload_is_reported_without_automatic_repair(local):
    with TestClient(host(local)) as client:
        document_id = identity(register(client))
        assert_content_response(put(client, document_id, b"original"), document_id, b"original")
        descriptor = local.contents.get(document_id)
        files = list(local.storage.rglob("*.bin"))
        assert len(files) == 1 and files[0].read_bytes() == b"original"
        files[0].write_bytes(b"Original")  # Fixture-owned temporary content only.
        before = payload_snapshot(local.storage)
        assert_error(put(client, document_id, b"original"), 409, "DOCUMENT_CONTENT_INTEGRITY_FAILURE")
        assert_error(ingest(client, document_id), 409, "DOCUMENT_CONTENT_INTEGRITY_FAILURE")
    assert local.contents.get(document_id) == descriptor
    assert payload_snapshot(local.storage) == before and local.counts() == (1, 1, 0, 0)


@pytest.mark.parametrize("phase", (
    "before-payload-publication", "after-payload-publication",
    "during-descriptor-persistence", "after-descriptor-commit",
))
def test_establishment_failure_retains_actual_state_and_requires_explicit_recovery(local, monkeypatch, phase):
    payload = b"exact content with a deliberately injected boundary failure\r\n"
    failures = []
    with TestClient(host(local)) as client:
        document_id = identity(register(client))
        with monkeypatch.context() as patch:
            if phase in ("before-payload-publication", "after-payload-publication"):
                real_add = local.store.add

                def failing_add(identity_, source):
                    failures.append(phase)
                    if phase == "after-payload-publication":
                        real_add(identity_, source)
                    raise RuntimeError("PRIVATE store boundary")

                patch.setattr(local.store, "add", failing_add)
                response = put(client, document_id, payload)
            elif phase == "during-descriptor-persistence":
                def fail_insert(_mapper, _connection, _target):
                    failures.append(phase)
                    raise RuntimeError("PRIVATE descriptor insert")

                event.listen(DocumentContentDescriptorRow, "before_insert", fail_insert)
                try:
                    response = put(client, document_id, payload)
                finally:
                    event.remove(DocumentContentDescriptorRow, "before_insert", fail_insert)
            else:
                real_add = local.contents.add

                def committed_then_failed(descriptor):
                    real_add(descriptor)
                    failures.append(phase)
                    raise RuntimeError("PRIVATE failure after descriptor commit")

                patch.setattr(local.contents, "add", committed_then_failed)
                response = put(client, document_id, payload)

        assert_error(response, 500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN")
        assert failures == [phase]
        assert local.documents.get(document_id) is not None
        descriptor = local.contents.get(document_id)
        persisted = payload_snapshot(local.storage)
        if phase == "before-payload-publication":
            assert descriptor is None and persisted == {}
            assert local.counts() == (1, 0, 0, 0)
        else:
            assert len(persisted) == 1 and next(iter(persisted.values()))[0] == payload
            if phase == "after-descriptor-commit":
                assert descriptor is not None and local.counts() == (1, 1, 0, 0)
            else:
                assert descriptor is None and local.counts() == (1, 0, 0, 0)
            assert_error(put(client, document_id, b"different"), 409, "DOCUMENT_CONTENT_CONFLICT")
            assert local.contents.get(document_id) == descriptor
            assert payload_snapshot(local.storage) == persisted

        assert failures == [phase]  # No HTTP-layer retry or compensation occurred.
        assert_content_response(put(client, document_id, payload), document_id, payload)
        assert local.counts() == (1, 1, 0, 0)
        if persisted:
            assert payload_snapshot(local.storage) == persisted
        assert failures == [phase]


def test_descriptor_conflict_after_payload_publication_does_not_imply_rollback(local, monkeypatch):
    payload, conflicts = b"payload already published before the descriptor conflict", []
    real_add = local.contents.add

    def conflicting_descriptor(descriptor):
        other = DocumentContentDescriptor(document_id=descriptor.document_id,
            media_type=DocumentContentMediaType(value="application/x-concurrent"),
            byte_length=descriptor.byte_length, digest=descriptor.digest)
        real_add(other)
        conflicts.append(other)
        raise DocumentContentAlreadyExistsError("PRIVATE concurrent descriptor")

    with TestClient(host(local)) as client:
        document_id = identity(register(client))
        with monkeypatch.context() as patch:
            patch.setattr(local.contents, "add", conflicting_descriptor)
            response = put(client, document_id, payload)
        assert_error(response, 409, "DOCUMENT_CONTENT_CONFLICT")
        assert len(conflicts) == 1 and local.contents.get(document_id) == conflicts[0]
        before = payload_snapshot(local.storage)
        assert len(before) == 1 and next(iter(before.values()))[0] == payload
        assert local.counts() == (1, 1, 0, 0)
        assert_error(put(client, document_id, payload), 409, "DOCUMENT_CONTENT_CONFLICT")
    assert local.contents.get(document_id) == conflicts[0]
    assert payload_snapshot(local.storage) == before and len(conflicts) == 1


@pytest.mark.parametrize("failure", ("exception", "invalid-result"))
def test_unknown_registration_after_write_preserves_document_and_does_not_retry(local, monkeypatch, failure):
    real_register, persisted = local.registrar.register, []

    def write_then_fail(request):
        document = real_register(request)
        persisted.append(document)
        if failure == "exception":
            raise DomainException("PRIVATE registration after successful write")
        return object()

    with TestClient(host(local)) as client:
        with monkeypatch.context() as patch:
            patch.setattr(local.registrar, "register", write_then_fail)
            response = register(client)
        assert_error(response, 500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN")
        assert len(persisted) == 1 and local.documents.get(persisted[0].id) == persisted[0]
        assert local.counts() == (1, 0, 0, 0) and payload_snapshot(local.storage) == {}
        later_id = identity(register(client))  # A distinct explicit request, not an adapter retry.
        assert later_id != persisted[0].id
    assert local.counts() == (2, 0, 0, 0) and len(persisted) == 1


def test_real_lineage_insert_failure_keeps_http_preparation_and_rolls_back_knowledge_pair(local):
    observed = []

    def fail_lineage(_mapper, connection, _target):
        observed.append(connection.scalar(select(func.count()).select_from(KnowledgeRow)))
        raise RuntimeError("PRIVATE lineage write")

    with TestClient(host(local)) as client:
        document_id = identity(register(client))
        payload = b"Preparation must survive a subsequent knowledge transaction failure"
        assert_content_response(put(client, document_id, payload), document_id, payload)
        document, descriptor = local.documents.get(document_id), local.contents.get(document_id)
        before = payload_snapshot(local.storage)
        event.listen(LineageRow, "before_insert", fail_lineage)
        try:
            response = ingest(client, document_id)
        finally:
            event.remove(LineageRow, "before_insert", fail_lineage)
        assert response.status_code == 500 and "PRIVATE" not in response.text
        assert response.json() == {"detail": {"code": "INGESTION_FAILED",
            "persistence_outcome": "unknown", "retry_recommended": False}}
    assert observed == [1] and local.counts() == (1, 1, 0, 0)
    assert local.documents.get(document_id) == document and local.contents.get(document_id) == descriptor
    assert payload_snapshot(local.storage) == before


def test_postcommit_knowledge_cleanup_failure_retains_preparation_and_committed_lineage(local):
    closes = []

    class ClosingSession(Session):
        def close(self):
            super().close()
            closes.append(1)
            raise RuntimeError("PRIVATE postcommit cleanup")

    platform = local.build(transaction_factory=sessionmaker(bind=local.engine,
        class_=ClosingSession, expire_on_commit=False, autoflush=False))
    with TestClient(host(local, platform=platform)) as client:
        document_id = identity(register(client))
        payload = b"The three HTTP operations are not one transaction"
        assert_content_response(put(client, document_id, payload), document_id, payload)
        document, descriptor = local.documents.get(document_id), local.contents.get(document_id)
        before = payload_snapshot(local.storage)
        response = ingest(client, document_id)
        assert response.status_code == 500 and "PRIVATE" not in response.text
        assert response.json() == {"detail": {"code": "INGESTION_COMMITTED_CLEANUP_FAILED",
            "persistence_outcome": "committed", "retry_recommended": False}}
    assert closes == [1] and local.counts() == (1, 1, 1, 1)
    assert local.documents.get(document_id) == document and local.contents.get(document_id) == descriptor
    assert payload_snapshot(local.storage) == before
    assert platform.runtime.is_request_admission_enabled is False


def test_preparation_pair_does_not_configure_ingestion(local):
    platform = local.build(configured=False)
    with TestClient(host(local, platform=platform)) as client:
        assert platform.runtime.is_request_admission_enabled is True
        document_id = identity(register(client))
        payload = b"Preparation succeeds without an ingestion dependency"
        assert_content_response(put(client, document_id, payload), document_id, payload)
        before = payload_snapshot(local.storage)
        assert_error(ingest(client, document_id), 503, "INGESTION_NOT_CONFIGURED")
    assert platform.runtime.is_request_admission_enabled is False
    assert local.counts() == (1, 1, 0, 0) and payload_snapshot(local.storage) == before


def test_managed_lifecycle_and_live_admission_gate_preparation_without_implicit_calls(local, monkeypatch):
    platform, calls = local.platform, []
    real_register, real_establish = local.registrar.register, local.establishment.establish

    def registered(request):
        calls.append("register")
        return real_register(request)

    def established(request):
        calls.append("establish")
        return real_establish(request)

    monkeypatch.setattr(local.registrar, "register", registered)
    monkeypatch.setattr(local.establishment, "establish", established)
    app = host(local)
    client = TestClient(app)
    try:
        for response in (
            client.post("/documents", content=b"malformed", headers={"Content-Encoding": "gzip"}),
            client.put("/documents/not-a-uuid/content", content=b"malformed"),
        ):
            assert response.status_code == 503 and response.json() == ADMISSION_CLOSED
        assert client.get("/").status_code == client.get("/health").status_code == 200
    finally:
        client.close()
    assert calls == [] and local.counts() == (0, 0, 0, 0)

    with TestClient(app) as client:
        assert platform.runtime.is_request_admission_enabled is True
        assert_error(register(client, title=" "), 422, "DOCUMENT_REGISTRATION_INVALID")
        assert calls == [] and local.counts() == (0, 0, 0, 0)
        document_id = identity(register(client))
        assert calls == ["register"] and local.counts() == (1, 0, 0, 0)
        assert_error(put(client, document_id, b"x", "text/plain; charset=utf-8"),
                     422, "DOCUMENT_CONTENT_MEDIA_TYPE_INVALID")
        platform.runtime.disable_request_admission()
        response = put(client, document_id, b"x")
        assert response.status_code == 503 and response.json() == ADMISSION_CLOSED
        assert calls == ["register"] and local.counts() == (1, 0, 0, 0)
        platform.runtime.enable_request_admission()
        assert_content_response(put(client, document_id, b"x"), document_id, b"x")
        assert calls == ["register", "establish"] and local.counts() == (1, 1, 0, 0)
    assert platform.runtime.is_request_admission_enabled is False
    assert calls == ["register", "establish"] and local.counts() == (1, 1, 0, 0)
