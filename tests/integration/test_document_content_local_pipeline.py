"""Regression tests for existing components; temporary SQLite, not PostgreSQL.

Each test owns an isolated filesystem store and disposable database. No default
host wiring, project database, credentials or external network are used.
"""
from __future__ import annotations

from collections.abc import Iterator
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory, gettempdir

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.base import EntityId
from app.infrastructure.document.models import EnterpriseDocumentRow
from app.infrastructure.document.repository import (
    SQLAlchemyEnterpriseDocumentRepository as Documents,
)
from app.infrastructure.document_content.models import DocumentContentDescriptorRow
from app.infrastructure.document_content.repository import (
    SQLAlchemyDocumentContentRepository as Contents,
)
from app.infrastructure.document_content.filesystem_store import (
    FilesystemDocumentContentStore as Store,
)
from app.services.enterprise_document_registration_application_service import (
    EnterpriseDocumentRegistrationApplicationService as Registrar,
    EnterpriseDocumentRegistrationRequest as Registration,
)
from app.services.document_content_establishment_application_service import (
    DocumentContentEstablishmentApplicationService as Establishment,
    DocumentContentEstablishmentRequest as EstablishRequest,
)
from app.services.document_content_access_application_service import (
    DocumentContentAccessApplicationService as Access,
    DocumentContentAccessDocumentNotFoundError,
    DocumentContentAccessIntegrityError,
)
from app.core.composition.document_content_parsing import (
    build_document_content_parsing_composition as compose,
)
from app.services.document_content_parsing_application_service import (
    DocumentContentParsingRequest as ParseRequest,
)
from app.document_parsing.parser import (
    DocumentContentParserInvalidContentError,
    DocumentContentParserUnsupportedMediaTypeError,
)


class _LocalPipeline:
    """Test-owned composition using real repository and filesystem adapters."""

    def __init__(self, folder: Path) -> None:
        self.storage = folder / "payloads"
        self.storage.mkdir()
        self.url = "sqlite+pysqlite:///" + str(folder / "probe.sqlite")
        self.engine = create_engine(self.url)

    def setup(self) -> None:
        EnterpriseDocumentRow.__table__.create(self.engine)
        DocumentContentDescriptorRow.__table__.create(self.engine)
        self._bind()

    def _bind(self) -> None:
        factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.documents = Documents(factory)
        self.contents = Contents(factory)
        self.store = Store(self.storage)
        self.registrar = Registrar(repository=self.documents)
        self.establishment = Establishment(
            document_repository=self.documents,
            content_repository=self.contents,
            content_store=self.store,
        )
        access = Access(
            document_repository=self.documents,
            content_repository=self.contents,
            content_store=self.store,
        )
        self.service = compose(content_access_service=access).application_service

    def reopen(self) -> None:
        self.engine.dispose()
        self.engine = create_engine(self.url)
        self._bind()

    def save(self, payload: bytes, media_type: str = "text/plain"):
        document = self.registrar.register(Registration(
            document_type="procedure", title="Synthetic regression fixture",
            source_type="document_control", source_reference="TEST-ONLY",
        ))
        with BytesIO(payload) as stream:
            descriptor = self.establishment.establish(EstablishRequest(
                document_id=document.id, media_type=media_type, source=stream,
            ))
        return document, descriptor

    def parse(self, document_id: EntityId):
        return self.service.parse(ParseRequest(document_id=document_id))


@pytest.fixture
def pipeline() -> Iterator[_LocalPipeline]:
    project = Path(__file__).resolve().parents[2]
    assert not Path(gettempdir()).resolve().is_relative_to(project)
    with TemporaryDirectory(prefix="PlantMind-regression-") as directory:
        local = _LocalPipeline(Path(directory).resolve())
        try:
            local.setup()
            yield local
        finally:
            local.engine.dispose()


def test_sqlite_and_filesystem_round_trip(pipeline: _LocalPipeline) -> None:
    document, descriptor = pipeline.save(b"Persistent synthetic text")
    assert any(pipeline.storage.rglob("*.bin"))
    pipeline.reopen()
    assert pipeline.documents.get(document.id) == document
    assert pipeline.contents.get(document.id) == descriptor
    result = pipeline.parse(document.id)
    assert result.text == "Persistent synthetic text"
    assert result.descriptor == descriptor


def test_arabic_bom_and_newlines(pipeline: _LocalPipeline) -> None:
    expected = "PlantMind\r\nنص عربي تجريبي\rEnd\n"
    payload = b"\xef\xbb\xbf" + expected.encode("utf-8")
    document, descriptor = pipeline.save(payload)
    pipeline.reopen()
    result = pipeline.parse(document.id)
    assert result.text == expected
    assert result.descriptor == descriptor
    assert descriptor.byte_length == len(payload)
    assert descriptor.digest.value == sha256(payload).hexdigest()


def test_repeated_read_preserves_content(pipeline: _LocalPipeline) -> None:
    document, descriptor = pipeline.save(b"Read-only synthetic content")
    pipeline.reopen()
    before = {p: p.read_bytes() for p in pipeline.storage.rglob("*.bin")}
    first = pipeline.parse(document.id)
    second = pipeline.parse(document.id)
    assert first == second
    assert first.text == "Read-only synthetic content"
    assert pipeline.documents.get(document.id) == document
    assert pipeline.contents.get(document.id) == descriptor
    assert before == {p: p.read_bytes() for p in pipeline.storage.rglob("*.bin")}


def test_empty_text(pipeline: _LocalPipeline) -> None:
    document, descriptor = pipeline.save(b"")
    result = pipeline.parse(document.id)
    assert result.text == ""
    assert result.descriptor == descriptor
    assert descriptor.byte_length == 0


def test_invalid_utf8_is_rejected(pipeline: _LocalPipeline) -> None:
    document, _ = pipeline.save(b"\xff\xfe")
    with pytest.raises(DocumentContentParserInvalidContentError) as caught:
        pipeline.parse(document.id)
    assert isinstance(caught.value.__cause__, UnicodeDecodeError)


def test_unsupported_media_type_is_rejected(pipeline: _LocalPipeline) -> None:
    document, _ = pipeline.save(b"test-only", "application/octet-stream")
    with pytest.raises(DocumentContentParserUnsupportedMediaTypeError):
        pipeline.parse(document.id)


def test_missing_document_is_rejected(pipeline: _LocalPipeline) -> None:
    with pytest.raises(DocumentContentAccessDocumentNotFoundError):
        pipeline.parse(EntityId.new())


def test_same_length_payload_change_is_rejected(pipeline: _LocalPipeline) -> None:
    payload = b"original synthetic text"
    document, descriptor = pipeline.save(payload)
    assert pipeline.parse(document.id).text == payload.decode("utf-8")
    files = [p for p in pipeline.storage.rglob("*.bin") if p.read_bytes() == payload]
    assert len(files) == 1
    changed = b"O" + payload[1:]
    assert len(changed) == len(payload) and changed != payload
    files[0].write_bytes(changed)  # Only the fixture's temporary file.
    with pytest.raises(DocumentContentAccessIntegrityError):
        pipeline.parse(document.id)
    assert pipeline.contents.get(document.id) == descriptor
    assert files[0].read_bytes() == changed  # No automatic repair.
