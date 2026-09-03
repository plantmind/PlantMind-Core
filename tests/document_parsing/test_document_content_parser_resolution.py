"""RFC-075 canonical Document Content parser resolution/dispatch tests."""

from __future__ import annotations

from contextlib import contextmanager
from hashlib import sha256
from importlib import import_module
from io import BytesIO
from typing import BinaryIO, Iterator, cast

import pytest

from app.document_parsing.parser import (
    DocumentContentParser,
    DocumentContentParserInvalidContentError,
    DocumentContentParserUnsupportedMediaTypeError,
)
from app.domain.base import EntityId
from app.domain.document_content import (
    DocumentContentDescriptor,
    DocumentContentDigest,
    DocumentContentMediaType,
)
from app.services.document_content_access_application_service import (
    DocumentContentAccess,
)
from app.services.document_content_parsing_application_service import (
    DocumentContentParsingApplicationService,
    DocumentContentParsingRequest,
)


def _resolver_module():
    return import_module("app.document_parsing.resolver")


def _dispatcher_module():
    return import_module("app.document_parsing.dispatching_parser")


def _descriptor(
    *,
    payload: bytes = b"verified payload",
    media_type: str = "application/pdf",
) -> DocumentContentDescriptor:
    return DocumentContentDescriptor(
        document_id=EntityId.new(),
        media_type=DocumentContentMediaType(
            value=media_type,
        ),
        byte_length=len(payload),
        digest=DocumentContentDigest(
            value=sha256(payload).hexdigest(),
        ),
    )


class RecordingParser(DocumentContentParser):
    def __init__(
        self,
        *,
        result: object = "parsed text",
        failure: Exception | None = None,
    ) -> None:
        self.result = result
        self.failure = failure
        self.calls: list[
            tuple[DocumentContentDescriptor, BinaryIO]
        ] = []

    def parse(
        self,
        *,
        descriptor: DocumentContentDescriptor,
        payload: BinaryIO,
    ) -> str:
        self.calls.append(
            (
                descriptor,
                payload,
            )
        )

        if self.failure is not None:
            raise self.failure

        return cast(str, self.result)


class RecordingResolver:
    def __init__(
        self,
        parser: DocumentContentParser | None = None,
        *,
        failure: Exception | None = None,
    ) -> None:
        self.parser = parser
        self.failure = failure
        self.calls: list[DocumentContentMediaType] = []

    def resolve(
        self,
        *,
        media_type: DocumentContentMediaType,
    ) -> DocumentContentParser:
        self.calls.append(media_type)

        if self.failure is not None:
            raise self.failure

        if self.parser is None:
            raise AssertionError(
                "Test resolver requires a parser or explicit failure."
            )

        return self.parser


class GuardedPayload:
    """Payload that fails if the dispatcher performs lifecycle/IO work."""

    def read(
        self,
        size: int = -1,
    ) -> bytes:
        raise AssertionError(
            "dispatcher must not read the borrowed payload"
        )

    def seek(
        self,
        *args: object,
        **kwargs: object,
    ) -> int:
        raise AssertionError(
            "dispatcher must not seek the borrowed payload"
        )

    def tell(self) -> int:
        raise AssertionError(
            "dispatcher must not inspect payload position"
        )

    def fileno(self) -> int:
        raise AssertionError(
            "dispatcher must not require a payload fileno"
        )

    def close(self) -> None:
        raise AssertionError(
            "dispatcher must not close the borrowed payload"
        )


class StaticAccessService:
    def __init__(
        self,
        *,
        descriptor: DocumentContentDescriptor,
        payload: BinaryIO,
    ) -> None:
        self.descriptor = descriptor
        self.payload = payload

    @contextmanager
    def open(
        self,
        request: object,
    ) -> Iterator[DocumentContentAccess]:
        yield DocumentContentAccess(
            descriptor=self.descriptor,
            payload=self.payload,
        )


def _dispatcher(
    resolver: object,
) -> DocumentContentParser:
    dispatcher_type = (
        _dispatcher_module()
        .DispatchingDocumentContentParser
    )

    return dispatcher_type(
        resolver=resolver,
    )


def test_dispatcher_implements_existing_parser_port() -> None:
    dispatcher = _dispatcher(
        RecordingResolver(
            RecordingParser()
        )
    )

    assert isinstance(
        dispatcher,
        DocumentContentParser,
    )


def test_dispatcher_resolves_from_exact_descriptor_media_type() -> None:
    descriptor = _descriptor(
        media_type=" APPLICATION/PDF "
    )
    payload = cast(
        BinaryIO,
        GuardedPayload(),
    )
    parser = RecordingParser()
    resolver = RecordingResolver(parser)
    dispatcher = _dispatcher(resolver)

    result = dispatcher.parse(
        descriptor=descriptor,
        payload=payload,
    )

    assert result == "parsed text"
    assert resolver.calls == [
        descriptor.media_type,
    ]
    assert resolver.calls[0] is descriptor.media_type


def test_resolver_is_called_exactly_once() -> None:
    descriptor = _descriptor()
    parser = RecordingParser()
    resolver = RecordingResolver(parser)

    _dispatcher(resolver).parse(
        descriptor=descriptor,
        payload=BytesIO(b"payload"),
    )

    assert len(resolver.calls) == 1


def test_resolved_parser_is_called_exactly_once() -> None:
    descriptor = _descriptor()
    payload = BytesIO(b"payload")
    parser = RecordingParser()

    _dispatcher(
        RecordingResolver(parser)
    ).parse(
        descriptor=descriptor,
        payload=payload,
    )

    assert parser.calls == [
        (
            descriptor,
            payload,
        )
    ]


def test_dispatch_preserves_descriptor_and_payload_identity() -> None:
    descriptor = _descriptor()
    payload = BytesIO(b"payload")
    parser = RecordingParser()

    _dispatcher(
        RecordingResolver(parser)
    ).parse(
        descriptor=descriptor,
        payload=payload,
    )

    observed_descriptor, observed_payload = parser.calls[0]

    assert observed_descriptor is descriptor
    assert observed_payload is payload


def test_dispatcher_performs_no_payload_io_or_lifecycle_operation() -> None:
    descriptor = _descriptor()
    payload = cast(
        BinaryIO,
        GuardedPayload(),
    )
    parser = RecordingParser()

    result = _dispatcher(
        RecordingResolver(parser)
    ).parse(
        descriptor=descriptor,
        payload=payload,
    )

    assert result == "parsed text"
    assert parser.calls[0][1] is payload


def test_unresolved_media_type_fails_closed_without_fallback() -> None:
    descriptor = _descriptor(
        media_type="application/x-unsupported"
    )
    failure = (
        DocumentContentParserUnsupportedMediaTypeError(
            "unsupported canonical media type"
        )
    )
    resolver = RecordingResolver(
        failure=failure,
    )

    with pytest.raises(
        DocumentContentParserUnsupportedMediaTypeError
    ) as exc_info:
        _dispatcher(resolver).parse(
            descriptor=descriptor,
            payload=BytesIO(b"payload"),
        )

    assert exc_info.value is failure
    assert resolver.calls == [
        descriptor.media_type,
    ]


def test_delegate_unsupported_media_type_failure_propagates_unchanged() -> None:
    descriptor = _descriptor()
    failure = (
        DocumentContentParserUnsupportedMediaTypeError(
            "delegate unsupported"
        )
    )
    parser = RecordingParser(
        failure=failure,
    )

    with pytest.raises(
        DocumentContentParserUnsupportedMediaTypeError
    ) as exc_info:
        _dispatcher(
            RecordingResolver(parser)
        ).parse(
            descriptor=descriptor,
            payload=BytesIO(b"payload"),
        )

    assert exc_info.value is failure


def test_invalid_content_failure_propagates_unchanged() -> None:
    descriptor = _descriptor()
    failure = DocumentContentParserInvalidContentError(
        "invalid content"
    )
    parser = RecordingParser(
        failure=failure,
    )

    with pytest.raises(
        DocumentContentParserInvalidContentError
    ) as exc_info:
        _dispatcher(
            RecordingResolver(parser)
        ).parse(
            descriptor=descriptor,
            payload=BytesIO(b"payload"),
        )

    assert exc_info.value is failure


def test_operational_parser_failure_propagates_unchanged() -> None:
    descriptor = _descriptor()
    failure = OSError("parser runtime failure")
    parser = RecordingParser(
        failure=failure,
    )

    with pytest.raises(OSError) as exc_info:
        _dispatcher(
            RecordingResolver(parser)
        ).parse(
            descriptor=descriptor,
            payload=BytesIO(b"payload"),
        )

    assert exc_info.value is failure


def test_empty_text_passes_through_unchanged() -> None:
    descriptor = _descriptor()
    parser = RecordingParser(
        result="",
    )

    result = _dispatcher(
        RecordingResolver(parser)
    ).parse(
        descriptor=descriptor,
        payload=BytesIO(b"payload"),
    )

    assert result == ""


def test_dispatcher_does_not_coerce_non_string_delegate_result() -> None:
    descriptor = _descriptor()
    marker = object()
    parser = RecordingParser(
        result=marker,
    )

    result = _dispatcher(
        RecordingResolver(parser)
    ).parse(
        descriptor=descriptor,
        payload=BytesIO(b"payload"),
    )

    assert result is marker


def test_existing_rfc074_application_boundary_still_rejects_non_string() -> None:
    descriptor = _descriptor()
    payload = BytesIO(b"payload")
    marker = object()
    parser = RecordingParser(
        result=marker,
    )
    dispatcher = _dispatcher(
        RecordingResolver(parser)
    )

    service = DocumentContentParsingApplicationService(
        content_access_service=cast(
            object,
            StaticAccessService(
                descriptor=descriptor,
                payload=payload,
            ),
        ),
        parser=dispatcher,
    )

    request = DocumentContentParsingRequest(
        document_id=descriptor.document_id,
    )

    with pytest.raises(
        TypeError,
        match="Document Content parser must return str",
    ):
        service.parse(request)


def test_resolver_contract_is_abstract_and_media_type_only() -> None:
    from abc import ABC
    from inspect import Parameter, signature
    from typing import get_type_hints

    resolver_type = (
        _resolver_module()
        .DocumentContentParserResolver
    )

    assert issubclass(
        resolver_type,
        ABC,
    )

    assert resolver_type.__abstractmethods__ == {
        "resolve",
    }

    operation = resolver_type.resolve
    operation_signature = signature(operation)
    parameters = list(
        operation_signature.parameters.values()
    )

    assert [parameter.name for parameter in parameters] == [
        "self",
        "media_type",
    ]

    assert parameters[1].kind is Parameter.KEYWORD_ONLY

    hints = get_type_hints(operation)

    assert hints["media_type"] is DocumentContentMediaType
    assert hints["return"] is DocumentContentParser
