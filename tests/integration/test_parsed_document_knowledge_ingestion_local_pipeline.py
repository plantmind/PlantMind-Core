"""RFC-079 real-adapter integration in isolated SQLite; not PostgreSQL certification."""
from io import BytesIO
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
    with TemporaryDirectory(prefix="PlantMind-RFC079-") as directory:
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
                return Service(parsing_service=parsing, ingestion_service=Ingestion(
                    document_repository=documents, transaction_coordinator=Coordinator(transaction_factory)))
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


def request(doc, title="Synthetic knowledge"):
    return Request(document_id=doc.id, kind="procedure", title=title)


def test_real_parse_then_atomic_knowledge_and_lineage(local):
    service, _, save, counts, factory, parsing, _, engine = local
    text = "  نص عربي\r\nSecond line  "
    doc = save(b"\xef\xbb\xbf" + text.encode("utf-8"))
    assert parsing.parse(DocumentContentParsingRequest(document_id=doc.id)).text == text
    assert counts() == (0, 0)  # Reading alone must not ingest.
    result = service.ingest(request(doc))
    assert result.lineage.document_id == doc.id
    assert result.lineage.knowledge_record_id == result.knowledge_record.id
    # The existing Knowledge domain owns its established outer-whitespace normalization.
    assert result.knowledge_record.content == text.strip()
    assert result.knowledge_record.provenance.source_reference == doc.source.source_reference
    engine.dispose()  # Verify persisted rows through a fresh database connection.
    assert counts() == (1, 1)
    with factory() as session:
        row = session.get(KnowledgeRow, result.knowledge_record.id.value)
        assert row.content == result.knowledge_record.content
        assert row.provenance_source_reference == "TEST-ONLY"
        assert session.get(LineageRow, (doc.id.value, result.knowledge_record.id.value)) is not None


@pytest.mark.parametrize("payload,media_type,error", [
    (b"", "text/plain", ValueError), (b" \n\t", "text/plain", ValueError),
    (b"\xff", "text/plain", DocumentContentParserInvalidContentError),
    (b"opaque", "application/octet-stream", DocumentContentParserUnsupportedMediaTypeError),
])
def test_rejected_content_creates_no_knowledge(local, payload, media_type, error):
    service, _, save, counts, *_ = local
    doc = save(payload, media_type)
    with pytest.raises(error):
        service.ingest(request(doc))
    assert counts() == (0, 0)


def test_missing_document_creates_nothing(local):
    service, _, _, counts, *_ = local
    with pytest.raises(DocumentContentAccessDocumentNotFoundError):
        service.ingest(Request(document_id=EntityId.new(), kind="procedure", title="x"))
    assert counts() == (0, 0)


def test_corrupt_payload_creates_nothing(local):
    service, _, save, counts, _, _, storage, _ = local
    doc = save(b"original")
    files = list(storage.rglob("*.bin"))
    assert len(files) == 1
    files[0].write_bytes(b"Original")  # Same size, wrong digest; temporary fixture only.
    with pytest.raises(DocumentContentAccessIntegrityError):
        service.ingest(request(doc))
    assert counts() == (0, 0)


def test_existing_domain_still_rejects_invalid_metadata(local):
    service, _, save, counts, *_ = local
    with pytest.raises(DomainException):
        service.ingest(request(save(), title=" "))
    assert counts() == (0, 0)


def test_repeated_explicit_calls_make_separate_records(local):
    service, _, save, counts, *_ = local
    doc = save()
    first, second = service.ingest(request(doc)), service.ingest(request(doc))
    assert first.knowledge_record.id != second.knowledge_record.id
    assert counts() == (2, 2)


def test_lineage_failure_rolls_back_prior_knowledge_write(local):
    service, _, save, counts, *_ = local
    doc, failure, observed = save(), RuntimeError("injected lineage failure"), []
    def fail(_mapper, connection, _target):
        observed.append(connection.scalar(select(func.count()).select_from(KnowledgeRow)))
        raise failure
    event.listen(LineageRow, "before_insert", fail)
    try:
        with pytest.raises(RuntimeError) as caught:
            service.ingest(request(doc))
        assert caught.value is failure
    finally:
        event.remove(LineageRow, "before_insert", fail)
    assert observed == [1] and counts() == (0, 0)


def test_post_commit_cleanup_failure_is_not_reported_as_rollback(local):
    _, build, save, counts, _, _, _, engine = local
    doc, failure, closes = save(), RuntimeError("injected close failure"), []
    class ClosingSession(Session):
        def close(self):
            super().close()
            closes.append(1)
            raise failure
    service = build(sessionmaker(bind=engine, class_=ClosingSession,
                                expire_on_commit=False, autoflush=False))
    with pytest.raises(KnowledgeLineageTransactionPostCommitCleanupError) as caught:
        service.ingest(request(doc))
    assert caught.value.__cause__ is failure
    assert closes == [1] and counts() == (1, 1)
