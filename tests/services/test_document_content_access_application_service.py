"""RFC-073 canonical Document Content access application tests."""

from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import FrozenInstanceError, fields
from hashlib import sha256
from inspect import Parameter, signature
from io import BytesIO
from typing import BinaryIO, cast

import pytest

from app.document.repository import EnterpriseDocumentRepository
from app.document_content.repository import DocumentContentRepository
from app.document_content.store import DocumentContentStore
from app.domain.base import EntityId
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
from app.services.document_content_access_application_service import (
    DocumentContentAccess,
    DocumentContentAccessApplicationService,
    DocumentContentAccessContentNotFoundError,
    DocumentContentAccessDocumentNotFoundError,
    DocumentContentAccessIntegrityError,
    DocumentContentAccessRequest,
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


class NonSeekablePayload:
    def __init__(
        self,
        payload: bytes,
    ) -> None:
        self._stream = BytesIO(payload)
        self.read_sizes: list[int] = []
        self.closed = False

    def read(
        self,
        size: int = -1,
    ) -> bytes:
        self.read_sizes.append(size)
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
        self._stream.close()


class ExplodingPayload(NonSeekablePayload):
    def __init__(
        self,
        payload: bytes,
        failure: Exception,
    ) -> None:
        super().__init__(payload)
        self.failure = failure

    def read(
        self,
        size: int = -1,
    ) -> bytes:
        self.read_sizes.append(size)
        raise self.failure


class PayloadContext(
    AbstractContextManager[BinaryIO]
):
    def __init__(
        self,
        stream: NonSeekablePayload,
        *,
        label: str,
        events: list[str] | None = None,
    ) -> None:
        self.stream = stream
        self.label = label
        self.events = events
        self.entered = False
        self.exited = False

    def __enter__(self) -> BinaryIO:
        self.entered = True

        if self.events is not None:
            self.events.append(
                f"enter:{self.label}"
            )

        return cast(
            BinaryIO,
            self.stream,
        )

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.exited = True

        if self.events is not None:
            self.events.append(
                f"exit:{self.label}"
            )

        self.stream.close()


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
        self.get_calls: list[EntityId] = []
        self.add_calls: list[EnterpriseDocument] = []

    def add(
        self,
        document: EnterpriseDocument,
    ) -> None:
        self.add_calls.append(document)

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
        descriptor: DocumentContentDescriptor | None,
        *,
        failure: Exception | None = None,
    ) -> None:
        self.descriptor = descriptor
        self.failure = failure
        self.get_calls: list[EntityId] = []
        self.add_calls: list[DocumentContentDescriptor] = []

    def add(
        self,
        descriptor: DocumentContentDescriptor,
    ) -> None:
        self.add_calls.append(descriptor)

    def get(
        self,
        document_id: EntityId,
    ) -> DocumentContentDescriptor | None:
        self.get_calls.append(document_id)

        if self.failure is not None:
            raise self.failure

        if (
            self.descriptor is not None
            and self.descriptor.document_id == document_id
        ):
            return self.descriptor

        return None


class RecordingContentStore(
    DocumentContentStore
):
    def __init__(
        self,
        opens: list[object],
        *,
        events: list[str] | None = None,
    ) -> None:
        self.opens = list(opens)
        self.events = events
        self.open_calls: list[EntityId] = []
        self.add_calls: list[EntityId] = []
        self.contexts: list[PayloadContext] = []

    def add(
        self,
        document_id: EntityId,
        source: BinaryIO,
    ) -> None:
        self.add_calls.append(document_id)

    def open(
        self,
        document_id: EntityId,
    ) -> AbstractContextManager[BinaryIO] | None:
        self.open_calls.append(document_id)
        position = len(self.open_calls)

        if self.events is not None:
            self.events.append(
                f"open:{position}"
            )

        if position > len(self.opens):
            raise AssertionError(
                "Unexpected additional DocumentContentStore.open() call."
            )

        planned = self.opens[
            position - 1
        ]

        if isinstance(
            planned,
            BaseException,
        ):
            raise planned

        if planned is None:
            return None

        if isinstance(
            planned,
            bytes,
        ):
            stream = NonSeekablePayload(
                planned
            )
        elif isinstance(
            planned,
            NonSeekablePayload,
        ):
            stream = planned
        else:
            raise TypeError(
                "Unsupported test payload plan."
            )

        context = PayloadContext(
            stream,
            label=str(position),
            events=self.events,
        )

        self.contexts.append(
            context
        )

        return context


def _service(
    *,
    document: EnterpriseDocument | None,
    descriptor: DocumentContentDescriptor | None = None,
    opens: list[object] | None = None,
    document_failure: Exception | None = None,
    content_failure: Exception | None = None,
    events: list[str] | None = None,
) -> tuple[
    DocumentContentAccessApplicationService,
    RecordingDocumentRepository,
    RecordingContentRepository,
    RecordingContentStore,
]:
    documents = RecordingDocumentRepository(
        document,
        failure=document_failure,
    )

    contents = RecordingContentRepository(
        descriptor,
        failure=content_failure,
    )

    store = RecordingContentStore(
        [] if opens is None else opens,
        events=events,
    )

    service = DocumentContentAccessApplicationService(
        document_repository=documents,
        content_repository=contents,
        content_store=store,
    )

    return (
        service,
        documents,
        contents,
        store,
    )


def _request(
    document_id: EntityId,
) -> DocumentContentAccessRequest:
    return DocumentContentAccessRequest(
        document_id=document_id
    )


def test_request_has_exact_immutable_keyword_only_contract() -> None:
    assert [
        field.name
        for field in fields(
            DocumentContentAccessRequest
        )
    ] == [
        "document_id",
    ]

    document_id = EntityId.new()
    request = _request(
        document_id
    )

    with pytest.raises(
        FrozenInstanceError
    ):
        request.document_id = EntityId.new()

    parameters = list(
        signature(
            DocumentContentAccessRequest
        ).parameters.values()
    )

    assert len(parameters) == 1
    assert (
        parameters[0].kind
        is Parameter.KEYWORD_ONLY
    )


def test_access_value_has_exact_immutable_contract() -> None:
    document_id = EntityId.new()

    descriptor = _descriptor(
        document_id,
        b"x",
    )

    access = DocumentContentAccess(
        descriptor=descriptor,
        payload=BytesIO(b"x"),
    )

    assert [
        field.name
        for field in fields(
            DocumentContentAccess
        )
    ] == [
        "descriptor",
        "payload",
    ]

    with pytest.raises(
        FrozenInstanceError
    ):
        access.descriptor = descriptor


def test_missing_document_stops_before_content_or_payload_access() -> None:
    document_id = EntityId.new()

    service, documents, contents, store = _service(
        document=None,
    )

    with pytest.raises(
        DocumentContentAccessDocumentNotFoundError
    ):
        with service.open(
            _request(document_id)
        ):
            raise AssertionError(
                "access must not be yielded"
            )

    assert documents.get_calls == [
        document_id
    ]
    assert contents.get_calls == []
    assert store.open_calls == []
    assert documents.add_calls == []
    assert contents.add_calls == []
    assert store.add_calls == []


def test_document_repository_failure_propagates_first() -> None:
    document_id = EntityId.new()
    failure = RuntimeError(
        "document read failed"
    )

    service, _, contents, store = _service(
        document=None,
        document_failure=failure,
    )

    with pytest.raises(
        RuntimeError
    ) as exc_info:
        with service.open(
            _request(document_id)
        ):
            pass

    assert exc_info.value is failure
    assert contents.get_calls == []
    assert store.open_calls == []


def test_content_repository_failure_propagates_before_store_access() -> None:
    document_id = EntityId.new()
    failure = RuntimeError(
        "descriptor read failed"
    )

    service, _, contents, store = _service(
        document=_document(
            document_id
        ),
        content_failure=failure,
    )

    with pytest.raises(
        RuntimeError
    ) as exc_info:
        with service.open(
            _request(document_id)
        ):
            pass

    assert exc_info.value is failure
    assert contents.get_calls == [
        document_id
    ]
    assert store.open_calls == []


def test_both_descriptor_and_payload_absent_is_content_not_found() -> None:
    document_id = EntityId.new()

    service, _, contents, store = _service(
        document=_document(
            document_id
        ),
        descriptor=None,
        opens=[
            None,
        ],
    )

    with pytest.raises(
        DocumentContentAccessContentNotFoundError
    ):
        with service.open(
            _request(document_id)
        ):
            pass

    assert contents.get_calls == [
        document_id
    ]
    assert store.open_calls == [
        document_id
    ]
    assert contents.add_calls == []
    assert store.add_calls == []


def test_descriptor_only_state_is_integrity_error() -> None:
    document_id = EntityId.new()

    descriptor = _descriptor(
        document_id,
        b"expected",
    )

    service, _, contents, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            None,
        ],
    )

    with pytest.raises(
        DocumentContentAccessIntegrityError
    ):
        with service.open(
            _request(document_id)
        ):
            pass

    assert contents.add_calls == []
    assert store.add_calls == []


def test_payload_only_state_is_fail_closed_and_context_is_closed() -> None:
    document_id = EntityId.new()

    service, _, contents, store = _service(
        document=_document(
            document_id
        ),
        descriptor=None,
        opens=[
            b"payload",
        ],
    )

    with pytest.raises(
        DocumentContentAccessIntegrityError
    ):
        with service.open(
            _request(document_id)
        ):
            pass

    assert len(
        store.contexts
    ) == 1
    assert store.contexts[0].entered is True
    assert store.contexts[0].exited is True
    assert (
        store.contexts[0].stream.read_sizes
        == []
    )
    assert contents.add_calls == []
    assert store.add_calls == []


def test_byte_length_mismatch_fails_before_delivery_reopen() -> None:
    document_id = EntityId.new()

    descriptor = _descriptor(
        document_id,
        b"expected-longer",
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            b"x",
        ],
    )

    with pytest.raises(
        DocumentContentAccessIntegrityError
    ):
        with service.open(
            _request(document_id)
        ):
            pass

    assert store.open_calls == [
        document_id
    ]
    assert store.contexts[0].exited is True


def test_digest_mismatch_fails_before_delivery_reopen() -> None:
    document_id = EntityId.new()

    descriptor = _descriptor(
        document_id,
        b"abc",
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            b"abd",
        ],
    )

    with pytest.raises(
        DocumentContentAccessIntegrityError
    ):
        with service.open(
            _request(document_id)
        ):
            pass

    assert store.open_calls == [
        document_id
    ]
    assert store.contexts[0].exited is True


def test_success_verifies_closes_reopens_then_delivers() -> None:
    document_id = EntityId.new()
    payload = b"canonical-payload"
    events: list[str] = []

    descriptor = _descriptor(
        document_id,
        payload,
    )

    service, documents, contents, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            payload,
            payload,
        ],
        events=events,
    )

    with service.open(
        _request(document_id)
    ) as access:
        assert access.descriptor is descriptor
        assert access.payload.read() == payload

        assert events == [
            "open:1",
            "enter:1",
            "exit:1",
            "open:2",
            "enter:2",
        ]

        assert store.contexts[0].exited is True
        assert store.contexts[1].exited is False

    assert events == [
        "open:1",
        "enter:1",
        "exit:1",
        "open:2",
        "enter:2",
        "exit:2",
    ]

    assert documents.get_calls == [
        document_id
    ]
    assert contents.get_calls == [
        document_id
    ]
    assert store.open_calls == [
        document_id,
        document_id,
    ]
    assert documents.add_calls == []
    assert contents.add_calls == []
    assert store.add_calls == []


def test_zero_byte_payload_verifies_and_delivers() -> None:
    document_id = EntityId.new()
    payload = b""

    descriptor = _descriptor(
        document_id,
        payload,
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            payload,
            payload,
        ],
    )

    with service.open(
        _request(document_id)
    ) as access:
        assert access.payload.read() == b""

    assert len(store.contexts) == 2
    assert all(
        context.exited
        for context in store.contexts
    )


def test_verification_is_incremental_and_requires_no_seekability() -> None:
    document_id = EntityId.new()

    payload = (
        b"a" * (1024 * 1024)
        + b"b" * (1024 * 1024)
        + b"end"
    )

    descriptor = _descriptor(
        document_id,
        payload,
    )

    verification_stream = NonSeekablePayload(
        payload
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            verification_stream,
            payload,
        ],
    )

    with service.open(
        _request(document_id)
    ) as access:
        assert access.payload.read(3) == b"aaa"

    assert verification_stream.read_sizes == [
        1024 * 1024,
        1024 * 1024,
        1024 * 1024,
        1024 * 1024,
    ]

    assert verification_stream.closed is True
    assert store.contexts[1].exited is True


def test_delivery_reopen_confirmed_absence_is_integrity_error() -> None:
    document_id = EntityId.new()
    payload = b"canonical"

    descriptor = _descriptor(
        document_id,
        payload,
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            payload,
            None,
        ],
    )

    with pytest.raises(
        DocumentContentAccessIntegrityError
    ):
        with service.open(
            _request(document_id)
        ):
            pass

    assert store.open_calls == [
        document_id,
        document_id,
    ]
    assert len(store.contexts) == 1
    assert store.contexts[0].exited is True


def test_verification_store_open_failure_propagates() -> None:
    document_id = EntityId.new()
    failure = RuntimeError(
        "store open failed"
    )

    descriptor = _descriptor(
        document_id,
        b"x",
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            failure,
        ],
    )

    with pytest.raises(
        RuntimeError
    ) as exc_info:
        with service.open(
            _request(document_id)
        ):
            pass

    assert exc_info.value is failure
    assert store.open_calls == [
        document_id
    ]


def test_verification_read_failure_propagates_and_closes_context() -> None:
    document_id = EntityId.new()
    failure = OSError(
        "verification read failed"
    )

    descriptor = _descriptor(
        document_id,
        b"x",
    )

    exploding = ExplodingPayload(
        b"x",
        failure,
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            exploding,
        ],
    )

    with pytest.raises(
        OSError
    ) as exc_info:
        with service.open(
            _request(document_id)
        ):
            pass

    assert exc_info.value is failure
    assert len(store.contexts) == 1
    assert store.contexts[0].exited is True
    assert exploding.closed is True


def test_delivery_open_failure_propagates_after_verification_close() -> None:
    document_id = EntityId.new()
    payload = b"x"
    failure = RuntimeError(
        "delivery open failed"
    )

    descriptor = _descriptor(
        document_id,
        payload,
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            payload,
            failure,
        ],
    )

    with pytest.raises(
        RuntimeError
    ) as exc_info:
        with service.open(
            _request(document_id)
        ):
            pass

    assert exc_info.value is failure
    assert len(store.contexts) == 1
    assert store.contexts[0].exited is True


def test_consumer_exception_closes_delivery_context() -> None:
    document_id = EntityId.new()
    payload = b"canonical"

    descriptor = _descriptor(
        document_id,
        payload,
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            payload,
            payload,
        ],
    )

    with pytest.raises(
        RuntimeError,
        match="consumer failed",
    ):
        with service.open(
            _request(document_id)
        ):
            raise RuntimeError(
                "consumer failed"
            )

    assert len(store.contexts) == 2
    assert all(
        context.exited
        for context in store.contexts
    )


def test_delivery_read_failure_propagates_and_closes_delivery() -> None:
    document_id = EntityId.new()
    payload = b"canonical"

    failure = OSError(
        "delivery read failed"
    )

    descriptor = _descriptor(
        document_id,
        payload,
    )

    delivery = ExplodingPayload(
        payload,
        failure,
    )

    service, _, _, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            payload,
            delivery,
        ],
    )

    with pytest.raises(
        OSError
    ) as exc_info:
        with service.open(
            _request(document_id)
        ) as access:
            access.payload.read()

    assert exc_info.value is failure
    assert len(store.contexts) == 2
    assert store.contexts[0].exited is True
    assert store.contexts[1].exited is True
    assert delivery.closed is True


def test_access_never_mutates_repository_or_store_state() -> None:
    document_id = EntityId.new()
    payload = b"canonical"

    descriptor = _descriptor(
        document_id,
        payload,
    )

    service, documents, contents, store = _service(
        document=_document(
            document_id
        ),
        descriptor=descriptor,
        opens=[
            payload,
            payload,
        ],
    )

    with service.open(
        _request(document_id)
    ) as access:
        assert access.payload.read() == payload

    assert documents.add_calls == []
    assert contents.add_calls == []
    assert store.add_calls == []
