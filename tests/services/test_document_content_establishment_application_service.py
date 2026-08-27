"""RFC-072 canonical Document Content establishment application tests."""

from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import FrozenInstanceError, fields
from hashlib import sha256
from inspect import Parameter, signature
from io import BytesIO
from typing import BinaryIO

import pytest

from app.document.repository import EnterpriseDocumentRepository
from app.document_content.repository import (
    DocumentContentAlreadyExistsError,
    DocumentContentRepository,
)
from app.document_content.store import (
    DocumentContentPayloadAlreadyExistsError,
    DocumentContentStore,
)
from app.domain.base import DomainException, EntityId
from app.domain.document import (
    DocumentSource,
    DocumentSourceType,
    DocumentType,
    EnterpriseDocument,
)
from app.domain.document_content import (
    DocumentContentDescriptor,
    DocumentContentDigest,
    DocumentContentMediaType,
)
from app.services.document_content_establishment_application_service import (
    DocumentContentEstablishmentApplicationService,
    DocumentContentEstablishmentConflictError,
    DocumentContentEstablishmentDocumentNotFoundError,
    DocumentContentEstablishmentIntegrityError,
    DocumentContentEstablishmentRequest,
)


def _digest(payload: bytes) -> DocumentContentDigest:
    return DocumentContentDigest(
        value=sha256(payload).hexdigest()
    )


def _descriptor(
    document_id: EntityId,
    payload: bytes,
    *,
    media_type: str = "application/pdf",
) -> DocumentContentDescriptor:
    return DocumentContentDescriptor(
        document_id=document_id,
        media_type=DocumentContentMediaType(
            value=media_type
        ),
        byte_length=len(payload),
        digest=_digest(payload),
    )


def _document(
    document_id: EntityId,
) -> EnterpriseDocument:
    return EnterpriseDocument(
        id=document_id,
        document_type=DocumentType(
            value="procedure"
        ),
        title="Compressor Start Procedure",
        source=DocumentSource(
            source_type=DocumentSourceType(
                value="document_control"
            ),
            source_reference="PROC-001",
        ),
    )


class NonSeekableSource:
    def __init__(
        self,
        payload: bytes,
    ) -> None:
        self._stream = BytesIO(payload)
        self.closed = False
        self.read_calls = 0

    def read(
        self,
        size: int = -1,
    ) -> bytes:
        self.read_calls += 1
        return self._stream.read(size)

    def seek(
        self,
        *args: object,
        **kwargs: object,
    ) -> None:
        raise AssertionError(
            "seek() must not be required"
        )

    def tell(self) -> int:
        raise AssertionError(
            "tell() must not be required"
        )

    def fileno(self) -> int:
        raise AssertionError(
            "fileno() must not be required"
        )

    def close(self) -> None:
        self.closed = True


class ExplodingSource(NonSeekableSource):
    def read(
        self,
        size: int = -1,
    ) -> bytes:
        self.read_calls += 1
        raise OSError("source read failed")


class RecordingDocumentRepository(
    EnterpriseDocumentRepository
):
    def __init__(
        self,
        document: EnterpriseDocument | None,
        *,
        failure: Exception | None = None,
    ) -> None:
        self.document = document
        self.failure = failure
        self.add_calls = 0
        self.get_calls: list[EntityId] = []

    def add(
        self,
        document: EnterpriseDocument,
    ) -> None:
        self.add_calls += 1

    def get(
        self,
        document_id: EntityId,
    ) -> EnterpriseDocument | None:
        self.get_calls.append(document_id)

        if self.failure is not None:
            raise self.failure

        if (
            self.document is not None
            and self.document.id == document_id
        ):
            return self.document

        return None


class RecordingContentRepository(
    DocumentContentRepository
):
    def __init__(
        self,
        descriptor: DocumentContentDescriptor | None = None,
        *,
        events: list[str] | None = None,
    ) -> None:
        self.descriptor = descriptor
        self.events = events
        self.get_calls: list[EntityId] = []
        self.add_calls: list[DocumentContentDescriptor] = []
        self.add_failure: Exception | None = None
        self.duplicate_observed: (
            DocumentContentDescriptor | None
        ) = None
        self.persist_before_add_failure = False

    def add(
        self,
        descriptor: DocumentContentDescriptor,
    ) -> None:
        self.add_calls.append(descriptor)

        if self.events is not None:
            self.events.append("descriptor_add")

        if self.add_failure is not None:
            if isinstance(
                self.add_failure,
                DocumentContentAlreadyExistsError,
            ):
                self.descriptor = self.duplicate_observed
            elif self.persist_before_add_failure:
                self.descriptor = descriptor

            raise self.add_failure

        self.descriptor = descriptor

    def get(
        self,
        document_id: EntityId,
    ) -> DocumentContentDescriptor | None:
        self.get_calls.append(document_id)

        if (
            self.descriptor is not None
            and self.descriptor.document_id == document_id
        ):
            return self.descriptor

        return None


class PayloadContext(
    AbstractContextManager[BinaryIO]
):
    def __init__(
        self,
        payload: bytes,
    ) -> None:
        self.stream = BytesIO(payload)
        self.entered = False
        self.exited = False

    def __enter__(self) -> BinaryIO:
        self.entered = True
        return self.stream

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.exited = True
        self.stream.close()


class RecordingContentStore(
    DocumentContentStore
):
    def __init__(
        self,
        payload: bytes | None = None,
        *,
        events: list[str] | None = None,
    ) -> None:
        self.payload = payload
        self.events = events
        self.open_calls: list[EntityId] = []
        self.add_calls: list[EntityId] = []
        self.open_failure: Exception | None = None
        self.add_failure: Exception | None = None
        self.consume_before_add_failure = False
        self.publish_before_add_failure = False
        self.last_context: PayloadContext | None = None

    def add(
        self,
        document_id: EntityId,
        source: BinaryIO,
    ) -> None:
        self.add_calls.append(document_id)

        if self.events is not None:
            self.events.append("payload_add")

        chunks: list[bytes] = []

        while True:
            chunk = source.read(3)

            if chunk == b"":
                break

            chunks.append(chunk)

        candidate = b"".join(chunks)

        if self.add_failure is not None:
            if (
                self.consume_before_add_failure
                or self.publish_before_add_failure
            ):
                self.payload = candidate

            raise self.add_failure

        if self.payload is not None:
            raise DocumentContentPayloadAlreadyExistsError(
                "payload already exists"
            )

        self.payload = candidate

    def open(
        self,
        document_id: EntityId,
    ) -> AbstractContextManager[BinaryIO] | None:
        self.open_calls.append(document_id)

        if self.open_failure is not None:
            raise self.open_failure

        if self.payload is None:
            return None

        self.last_context = PayloadContext(
            self.payload
        )

        return self.last_context


def _service(
    *,
    document: EnterpriseDocument | None,
    descriptor: DocumentContentDescriptor | None = None,
    payload: bytes | None = None,
    events: list[str] | None = None,
) -> tuple[
    DocumentContentEstablishmentApplicationService,
    RecordingDocumentRepository,
    RecordingContentRepository,
    RecordingContentStore,
]:
    document_repository = RecordingDocumentRepository(
        document
    )
    content_repository = RecordingContentRepository(
        descriptor,
        events=events,
    )
    content_store = RecordingContentStore(
        payload,
        events=events,
    )

    service = DocumentContentEstablishmentApplicationService(
        document_repository=document_repository,
        content_repository=content_repository,
        content_store=content_store,
    )

    return (
        service,
        document_repository,
        content_repository,
        content_store,
    )


def _request(
    document_id: EntityId,
    source: BinaryIO,
    *,
    media_type: str = " Application/PDF ",
) -> DocumentContentEstablishmentRequest:
    return DocumentContentEstablishmentRequest(
        document_id=document_id,
        media_type=media_type,
        source=source,
    )


def test_request_has_exact_immutable_keyword_only_contract() -> None:
    assert [
        field.name
        for field in fields(
            DocumentContentEstablishmentRequest
        )
    ] == [
        "document_id",
        "media_type",
        "source",
    ]

    request = _request(
        EntityId.new(),
        BytesIO(b"x"),
    )

    with pytest.raises(FrozenInstanceError):
        request.media_type = "text/plain"

    with pytest.raises(TypeError):
        DocumentContentEstablishmentRequest(
            EntityId.new(),
            "application/pdf",
            BytesIO(b"x"),
        )


def test_service_constructor_has_exact_dependency_contract() -> None:
    parameters = list(
        signature(
            DocumentContentEstablishmentApplicationService.__init__
        ).parameters.values()
    )

    assert [
        parameter.name
        for parameter in parameters
    ] == [
        "self",
        "document_repository",
        "content_repository",
        "content_store",
    ]

    assert all(
        parameter.kind is Parameter.KEYWORD_ONLY
        for parameter in parameters[1:]
    )


def test_establish_has_exact_operation_contract() -> None:
    parameters = list(
        signature(
            DocumentContentEstablishmentApplicationService.establish
        ).parameters.values()
    )

    assert [
        parameter.name
        for parameter in parameters
    ] == [
        "self",
        "request",
    ]

    assert (
        parameters[1].kind
        is Parameter.POSITIONAL_OR_KEYWORD
    )


def test_missing_document_stops_before_content_or_source_access() -> None:
    document_id = EntityId.new()
    source = NonSeekableSource(b"payload")

    service, documents, contents, store = _service(
        document=None
    )

    with pytest.raises(
        DocumentContentEstablishmentDocumentNotFoundError
    ):
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
            )
        )

    assert documents.get_calls == [document_id]
    assert contents.get_calls == []
    assert contents.add_calls == []
    assert store.open_calls == []
    assert store.add_calls == []
    assert source.read_calls == 0
    assert source.closed is False


def test_document_repository_failure_propagates_before_other_boundaries() -> None:
    document_id = EntityId.new()
    failure = RuntimeError("document read failed")

    documents = RecordingDocumentRepository(
        None,
        failure=failure,
    )
    contents = RecordingContentRepository()
    store = RecordingContentStore()
    source = NonSeekableSource(b"x")

    service = DocumentContentEstablishmentApplicationService(
        document_repository=documents,
        content_repository=contents,
        content_store=store,
    )

    with pytest.raises(RuntimeError) as exc_info:
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
            )
        )

    assert exc_info.value is failure
    assert contents.get_calls == []
    assert store.open_calls == []
    assert source.read_calls == 0


def test_fresh_establishment_is_payload_first_and_exact() -> None:
    document_id = EntityId.new()
    events: list[str] = []
    source = BytesIO(b"prefix-payload")
    source.seek(len(b"prefix-"))

    service, _, contents, store = _service(
        document=_document(document_id),
        events=events,
    )

    descriptor = service.establish(
        _request(
            document_id,
            source,
        )
    )

    assert events == [
        "payload_add",
        "descriptor_add",
    ]
    assert store.payload == b"payload"
    assert descriptor == contents.descriptor
    assert descriptor.document_id == document_id
    assert descriptor.media_type.value == "application/pdf"
    assert descriptor.byte_length == len(b"payload")
    assert descriptor.digest == _digest(b"payload")
    assert not source.closed


def test_fresh_nonseekable_source_is_supported_and_not_closed() -> None:
    document_id = EntityId.new()
    source = NonSeekableSource(
        b"streamed-content"
    )

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    descriptor = service.establish(
        _request(
            document_id,
            source,  # type: ignore[arg-type]
        )
    )

    assert store.payload == b"streamed-content"
    assert descriptor == contents.descriptor
    assert source.closed is False


def test_fresh_zero_byte_payload_is_valid() -> None:
    document_id = EntityId.new()

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    descriptor = service.establish(
        _request(
            document_id,
            BytesIO(b""),
        )
    )

    assert store.payload == b""
    assert descriptor.byte_length == 0
    assert descriptor.digest == _digest(b"")
    assert contents.descriptor == descriptor


def test_fresh_invalid_media_type_prevents_payload_write() -> None:
    document_id = EntityId.new()

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    with pytest.raises(DomainException):
        service.establish(
            _request(
                document_id,
                BytesIO(b"x"),
                media_type="invalid",
            )
        )

    assert store.add_calls == []
    assert contents.add_calls == []


def test_racing_store_duplicate_maps_to_application_conflict() -> None:
    document_id = EntityId.new()
    source = NonSeekableSource(b"winner")

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    duplicate = DocumentContentPayloadAlreadyExistsError(
        "concurrent payload"
    )

    store.add_failure = duplicate
    store.consume_before_add_failure = True

    with pytest.raises(
        DocumentContentEstablishmentConflictError
    ) as exc_info:
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
            )
        )

    assert exc_info.value.__cause__ is duplicate
    assert source.read_calls > 0
    assert source.closed is False
    assert contents.add_calls == []
    assert store.payload == b"winner"


def test_store_operational_failure_propagates_without_descriptor_write() -> None:
    document_id = EntityId.new()
    failure = RuntimeError("store failed")

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    store.add_failure = failure

    with pytest.raises(RuntimeError) as exc_info:
        service.establish(
            _request(
                document_id,
                BytesIO(b"x"),
            )
        )

    assert exc_info.value is failure
    assert contents.add_calls == []


def test_store_postpublication_failure_propagates_without_descriptor_write() -> None:
    document_id = EntityId.new()
    failure = RuntimeError(
        "postpublication cleanup failed"
    )

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    store.add_failure = failure
    store.publish_before_add_failure = True

    with pytest.raises(RuntimeError) as exc_info:
        service.establish(
            _request(
                document_id,
                BytesIO(b"published"),
            )
        )

    assert exc_info.value is failure
    assert store.payload == b"published"
    assert contents.add_calls == []


def test_descriptor_operational_failure_propagates_after_payload() -> None:
    document_id = EntityId.new()
    failure = RuntimeError("descriptor failed")

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    contents.add_failure = failure

    with pytest.raises(RuntimeError) as exc_info:
        service.establish(
            _request(
                document_id,
                BytesIO(b"payload"),
            )
        )

    assert exc_info.value is failure
    assert store.payload == b"payload"
    assert len(contents.add_calls) == 1


def test_descriptor_postcommit_failure_propagates_without_inferred_success() -> None:
    document_id = EntityId.new()
    failure = RuntimeError(
        "descriptor cleanup failed"
    )

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    contents.add_failure = failure
    contents.persist_before_add_failure = True

    with pytest.raises(RuntimeError) as exc_info:
        service.establish(
            _request(
                document_id,
                BytesIO(b"payload"),
            )
        )

    assert exc_info.value is failure
    assert store.payload == b"payload"
    assert contents.descriptor is not None


def test_descriptor_duplicate_exact_value_reconciles_successfully() -> None:
    document_id = EntityId.new()
    payload = b"payload"

    expected = _descriptor(
        document_id,
        payload,
    )

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    duplicate = DocumentContentAlreadyExistsError(
        "concurrent descriptor"
    )

    contents.add_failure = duplicate
    contents.duplicate_observed = expected

    result = service.establish(
        _request(
            document_id,
            BytesIO(payload),
        )
    )

    assert result == expected
    assert store.payload == payload
    assert contents.get_calls == [
        document_id,
        document_id,
    ]


def test_descriptor_duplicate_different_value_is_conflict() -> None:
    document_id = EntityId.new()
    payload = b"payload"

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    duplicate = DocumentContentAlreadyExistsError(
        "concurrent descriptor"
    )

    contents.add_failure = duplicate
    contents.duplicate_observed = _descriptor(
        document_id,
        b"different",
    )

    with pytest.raises(
        DocumentContentEstablishmentConflictError
    ) as exc_info:
        service.establish(
            _request(
                document_id,
                BytesIO(payload),
            )
        )

    assert exc_info.value.__cause__ is duplicate
    assert store.payload == payload


def test_descriptor_only_state_is_integrity_error_without_source_consumption() -> None:
    document_id = EntityId.new()

    descriptor = _descriptor(
        document_id,
        b"expected",
    )

    source = NonSeekableSource(b"expected")

    service, _, contents, store = _service(
        document=_document(document_id),
        descriptor=descriptor,
        payload=None,
    )

    with pytest.raises(
        DocumentContentEstablishmentIntegrityError
    ):
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
            )
        )

    assert source.read_calls == 0
    assert source.closed is False
    assert store.add_calls == []
    assert contents.add_calls == []


def test_payload_only_matching_source_recovers_descriptor() -> None:
    document_id = EntityId.new()
    payload = b"payload"
    source = NonSeekableSource(payload)

    service, _, contents, store = _service(
        document=_document(document_id),
        payload=payload,
    )

    descriptor = service.establish(
        _request(
            document_id,
            source,  # type: ignore[arg-type]
        )
    )

    assert descriptor == _descriptor(
        document_id,
        payload,
    )

    assert contents.descriptor == descriptor
    assert contents.add_calls == [descriptor]
    assert source.read_calls > 0
    assert source.closed is False
    assert store.last_context is not None
    assert store.last_context.exited is True


def test_payload_only_mismatching_source_is_conflict_without_descriptor() -> None:
    document_id = EntityId.new()
    source = NonSeekableSource(b"caller")

    service, _, contents, store = _service(
        document=_document(document_id),
        payload=b"canonical",
    )

    with pytest.raises(
        DocumentContentEstablishmentConflictError
    ):
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
            )
        )

    assert contents.add_calls == []
    assert store.last_context is not None
    assert store.last_context.exited is True


def test_payload_only_source_failure_propagates_and_closes_payload() -> None:
    document_id = EntityId.new()
    source = ExplodingSource(b"unused")

    service, _, contents, store = _service(
        document=_document(document_id),
        payload=b"canonical",
    )

    with pytest.raises(
        OSError,
        match="source read failed",
    ):
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
            )
        )

    assert contents.add_calls == []
    assert store.last_context is not None
    assert store.last_context.exited is True
    assert source.closed is False


def test_complete_exact_repeat_returns_existing_descriptor() -> None:
    document_id = EntityId.new()
    payload = b"canonical"

    descriptor = _descriptor(
        document_id,
        payload,
    )

    source = NonSeekableSource(payload)

    service, _, contents, store = _service(
        document=_document(document_id),
        descriptor=descriptor,
        payload=payload,
    )

    result = service.establish(
        _request(
            document_id,
            source,  # type: ignore[arg-type]
        )
    )

    assert result is descriptor
    assert contents.add_calls == []
    assert store.add_calls == []
    assert source.closed is False
    assert store.last_context is not None
    assert store.last_context.exited is True


def test_complete_media_type_conflict_does_not_consume_source_and_closes_payload() -> None:
    document_id = EntityId.new()
    payload = b"canonical"

    descriptor = _descriptor(
        document_id,
        payload,
    )

    source = NonSeekableSource(payload)

    service, _, _, store = _service(
        document=_document(document_id),
        descriptor=descriptor,
        payload=payload,
    )

    with pytest.raises(
        DocumentContentEstablishmentConflictError
    ):
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
                media_type="text/plain",
            )
        )

    assert source.read_calls == 0
    assert store.last_context is not None
    assert store.last_context.exited is True


def test_complete_persisted_mismatch_is_integrity_error_before_source_read() -> None:
    document_id = EntityId.new()

    descriptor = _descriptor(
        document_id,
        b"descriptor-bytes",
    )

    source = NonSeekableSource(
        b"different-caller"
    )

    service, _, contents, store = _service(
        document=_document(document_id),
        descriptor=descriptor,
        payload=b"different-payload",
    )

    with pytest.raises(
        DocumentContentEstablishmentIntegrityError
    ):
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
            )
        )

    assert source.read_calls == 0
    assert contents.add_calls == []
    assert store.last_context is not None
    assert store.last_context.exited is True


def test_complete_caller_mismatch_is_conflict() -> None:
    document_id = EntityId.new()
    payload = b"canonical"

    descriptor = _descriptor(
        document_id,
        payload,
    )

    service, _, contents, store = _service(
        document=_document(document_id),
        descriptor=descriptor,
        payload=payload,
    )

    with pytest.raises(
        DocumentContentEstablishmentConflictError
    ):
        service.establish(
            _request(
                document_id,
                BytesIO(b"caller"),
            )
        )

    assert contents.add_calls == []
    assert store.add_calls == []


def test_store_open_operational_failure_propagates_without_source_read() -> None:
    document_id = EntityId.new()
    failure = RuntimeError("open failed")
    source = NonSeekableSource(b"x")

    service, _, contents, store = _service(
        document=_document(document_id)
    )

    store.open_failure = failure

    with pytest.raises(RuntimeError) as exc_info:
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
            )
        )

    assert exc_info.value is failure
    assert source.read_calls == 0
    assert contents.add_calls == []


def test_invalid_media_type_in_complete_state_closes_payload_without_source_read() -> None:
    document_id = EntityId.new()
    payload = b"canonical"

    descriptor = _descriptor(
        document_id,
        payload,
    )

    source = NonSeekableSource(payload)

    service, _, _, store = _service(
        document=_document(document_id),
        descriptor=descriptor,
        payload=payload,
    )

    with pytest.raises(DomainException):
        service.establish(
            _request(
                document_id,
                source,  # type: ignore[arg-type]
                media_type="invalid",
            )
        )

    assert source.read_calls == 0
    assert store.last_context is not None
    assert store.last_context.exited is True
