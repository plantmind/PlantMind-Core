"""RFC-078 document parsing composition behavior tests."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import FrozenInstanceError
from hashlib import sha256
from importlib import import_module
from io import BytesIO
from typing import BinaryIO, Callable, Iterator, cast

import pytest

from app.document_parsing.parser import (
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
    DocumentContentAccessApplicationService,
    DocumentContentAccessRequest,
)
from app.services.document_content_parsing_application_service import (
    DocumentContentParsingRequest,
)


UTF8_BOM = b"\xef\xbb\xbf"


def _module():
    return import_module(
        "app.core.composition.document_content_parsing"
    )


def _descriptor(
    *,
    payload: bytes,
    media_type: str = "text/plain",
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


class StaticContentAccessService(
    DocumentContentAccessApplicationService
):
    def __init__(
        self,
        *,
        descriptor: DocumentContentDescriptor,
        payload_factory: Callable[[], BinaryIO],
        failure: BaseException | None = None,
    ) -> None:
        self.descriptor = descriptor
        self.payload_factory = payload_factory
        self.failure = failure
        self.requests: list[DocumentContentAccessRequest] = []
        self.payloads: list[BinaryIO] = []

    @contextmanager
    def open(
        self,
        request: DocumentContentAccessRequest,
    ) -> Iterator[DocumentContentAccess]:
        self.requests.append(request)

        if self.failure is not None:
            raise self.failure

        payload = self.payload_factory()
        self.payloads.append(payload)

        yield DocumentContentAccess(
            descriptor=self.descriptor,
            payload=payload,
        )


class GuardedPayload:
    def __init__(self) -> None:
        self.read_calls = 0

    def read(self, size: int = -1) -> bytes:
        self.read_calls += 1
        raise AssertionError(
            "unsupported media type must fail before payload read"
        )


class FailingPayload:
    def __init__(self, failure: BaseException) -> None:
        self.failure = failure
        self.read_calls = 0

    def read(self, size: int = -1) -> bytes:
        self.read_calls += 1
        raise self.failure


def _access_service(
    *,
    payload: bytes = b"PlantMind",
    media_type: str = "text/plain",
    payload_factory: Callable[[], BinaryIO] | None = None,
    failure: BaseException | None = None,
) -> StaticContentAccessService:
    descriptor = _descriptor(
        payload=payload,
        media_type=media_type,
    )

    if payload_factory is None:
        payload_factory = lambda: BytesIO(payload)

    return StaticContentAccessService(
        descriptor=descriptor,
        payload_factory=payload_factory,
        failure=failure,
    )


def _build(
    service: DocumentContentAccessApplicationService,
):
    return _module().build_document_content_parsing_composition(
        content_access_service=service,
    )


def test_builder_returns_expected_composition_type() -> None:
    composition = _build(
        _access_service(),
    )

    assert isinstance(
        composition,
        _module().DocumentContentParsingComposition,
    )


def test_composition_is_frozen_after_construction() -> None:
    composition = _build(
        _access_service(),
    )

    with pytest.raises(FrozenInstanceError):
        composition.dispatcher = object()


def test_invalid_access_service_fails_before_graph_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()

    def forbidden_parser_constructor() -> object:
        raise AssertionError(
            "parser graph construction must not start"
        )

    monkeypatch.setattr(
        module,
        "Utf8PlainTextDocumentContentParser",
        forbidden_parser_constructor,
    )

    with pytest.raises(
        TypeError,
        match="DocumentContentAccessApplicationService",
    ):
        module.build_document_content_parsing_composition(
            content_access_service=object(),
        )


def test_builder_constructs_graph_in_exact_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    service = _access_service()
    order: list[str] = []

    original_parser = module.Utf8PlainTextDocumentContentParser
    original_media_type = module.DocumentContentMediaType
    original_binding = module.DocumentContentParserBinding
    original_resolver = (
        module.RegistryBackedDocumentContentParserResolver
    )
    original_dispatcher = module.DispatchingDocumentContentParser
    original_application_service = (
        module.DocumentContentParsingApplicationService
    )
    original_composition = module.DocumentContentParsingComposition

    def parser_factory():
        order.append("plain_text_parser")
        return original_parser()

    def media_type_factory(*, value: str):
        order.append("media_type")
        return original_media_type(value=value)

    def binding_factory(*, media_type: object, factory: object):
        order.append("binding")
        return original_binding(
            media_type=media_type,
            factory=factory,
        )

    def resolver_factory(*, bindings: object):
        order.append("resolver")
        return original_resolver(
            bindings=bindings,
        )

    def dispatcher_factory(*, resolver: object):
        order.append("dispatcher")
        return original_dispatcher(
            resolver=resolver,
        )

    def application_service_factory(
        *,
        content_access_service: object,
        parser: object,
    ):
        order.append("application_service")
        return original_application_service(
            content_access_service=content_access_service,
            parser=parser,
        )

    def composition_factory(**kwargs: object):
        order.append("composition")
        return original_composition(**kwargs)

    monkeypatch.setattr(
        module,
        "Utf8PlainTextDocumentContentParser",
        parser_factory,
    )
    monkeypatch.setattr(
        module,
        "DocumentContentMediaType",
        media_type_factory,
    )
    monkeypatch.setattr(
        module,
        "DocumentContentParserBinding",
        binding_factory,
    )
    monkeypatch.setattr(
        module,
        "RegistryBackedDocumentContentParserResolver",
        resolver_factory,
    )
    monkeypatch.setattr(
        module,
        "DispatchingDocumentContentParser",
        dispatcher_factory,
    )
    monkeypatch.setattr(
        module,
        "DocumentContentParsingApplicationService",
        application_service_factory,
    )
    monkeypatch.setattr(
        module,
        "DocumentContentParsingComposition",
        composition_factory,
    )

    composition = module.build_document_content_parsing_composition(
        content_access_service=service,
    )

    assert isinstance(
        composition,
        original_composition,
    )
    assert order == [
        "plain_text_parser",
        "media_type",
        "binding",
        "resolver",
        "dispatcher",
        "application_service",
        "composition",
    ]


def test_construction_performs_no_content_access_or_payload_read() -> None:
    def forbidden_payload_factory() -> BinaryIO:
        raise AssertionError(
            "composition construction must not request a payload"
        )

    service = _access_service(
        payload_factory=forbidden_payload_factory,
    )

    _build(service)

    assert service.requests == []
    assert service.payloads == []


def test_composition_exposes_exact_graph_identity() -> None:
    service = _access_service()
    composition = _build(service)

    assert (
        composition.application_service._content_access_service
        is service
    )
    assert (
        composition.application_service._parser
        is composition.dispatcher
    )
    assert (
        composition.dispatcher._resolver
        is composition.resolver
    )


def test_plain_text_binding_is_exact_and_returns_owned_parser() -> None:
    composition = _build(
        _access_service(),
    )

    assert (
        composition.plain_text_binding.media_type.value
        == "text/plain"
    )
    assert (
        composition.plain_text_binding.factory()
        is composition.plain_text_parser
    )


def test_resolver_contains_one_binding_and_returns_owned_parser() -> None:
    composition = _build(
        _access_service(),
    )

    assert composition.resolver._registry.registered() == (
        "text/plain",
    )
    assert (
        composition.resolver.resolve(
            media_type=DocumentContentMediaType(
                value="text/plain",
            ),
        )
        is composition.plain_text_parser
    )


def test_two_builds_create_isolated_object_graphs() -> None:
    service = _access_service()

    first = _build(service)
    second = _build(service)

    assert first is not second
    assert first.plain_text_parser is not second.plain_text_parser
    assert first.plain_text_binding is not second.plain_text_binding
    assert first.resolver is not second.resolver
    assert first.dispatcher is not second.dispatcher
    assert first.application_service is not second.application_service
    assert (
        first.application_service._content_access_service
        is service
    )
    assert (
        second.application_service._content_access_service
        is service
    )


def test_valid_utf8_plain_text_succeeds_end_to_end() -> None:
    text = "PlantMind — العربية — 日本語 — 🙂"
    payload = text.encode("utf-8")
    service = _access_service(
        payload=payload,
    )
    composition = _build(service)

    result = composition.application_service.parse(
        DocumentContentParsingRequest(
            document_id=service.descriptor.document_id,
        )
    )

    assert result.descriptor is service.descriptor
    assert result.text == text


def test_bom_and_mixed_newlines_are_preserved_end_to_end() -> None:
    text = "A\r\nB\rC\nD"
    payload = UTF8_BOM + text.encode("utf-8")
    service = _access_service(
        payload=payload,
    )
    composition = _build(service)

    result = composition.application_service.parse(
        DocumentContentParsingRequest(
            document_id=service.descriptor.document_id,
        )
    )

    assert result.text == text


def test_empty_plain_text_succeeds_end_to_end() -> None:
    service = _access_service(
        payload=b"",
    )
    composition = _build(service)

    result = composition.application_service.parse(
        DocumentContentParsingRequest(
            document_id=service.descriptor.document_id,
        )
    )

    assert result.text == ""


def test_unsupported_media_type_fails_closed_without_payload_read() -> None:
    payload = b"%PDF"
    guarded_payload = GuardedPayload()
    service = _access_service(
        payload=payload,
        media_type="application/pdf",
        payload_factory=lambda: cast(
            BinaryIO,
            guarded_payload,
        ),
    )
    composition = _build(service)

    with pytest.raises(
        DocumentContentParserUnsupportedMediaTypeError
    ):
        composition.application_service.parse(
            DocumentContentParsingRequest(
                document_id=service.descriptor.document_id,
            )
        )

    assert guarded_payload.read_calls == 0


def test_invalid_utf8_failure_and_cause_propagate_end_to_end() -> None:
    payload = b"\xff"
    service = _access_service(
        payload=payload,
    )
    composition = _build(service)

    with pytest.raises(
        DocumentContentParserInvalidContentError
    ) as exc_info:
        composition.application_service.parse(
            DocumentContentParsingRequest(
                document_id=service.descriptor.document_id,
            )
        )

    assert isinstance(
        exc_info.value.__cause__,
        UnicodeDecodeError,
    )


def test_payload_operational_failure_propagates_same_instance() -> None:
    failure = OSError("payload failure")
    failing_payload = FailingPayload(failure)
    service = _access_service(
        payload=b"text",
        payload_factory=lambda: cast(
            BinaryIO,
            failing_payload,
        ),
    )
    composition = _build(service)

    with pytest.raises(OSError) as exc_info:
        composition.application_service.parse(
            DocumentContentParsingRequest(
                document_id=service.descriptor.document_id,
            )
        )

    assert exc_info.value is failure
    assert failing_payload.read_calls == 1


def test_content_access_failure_propagates_same_instance() -> None:
    failure = RuntimeError("content access failure")
    service = _access_service(
        failure=failure,
    )
    composition = _build(service)

    with pytest.raises(RuntimeError) as exc_info:
        composition.application_service.parse(
            DocumentContentParsingRequest(
                document_id=service.descriptor.document_id,
            )
        )

    assert exc_info.value is failure


def test_access_service_receives_exact_document_identity() -> None:
    service = _access_service()
    composition = _build(service)

    composition.application_service.parse(
        DocumentContentParsingRequest(
            document_id=service.descriptor.document_id,
        )
    )

    assert len(service.requests) == 1
    assert (
        service.requests[0].document_id
        is service.descriptor.document_id
    )


def test_result_preserves_descriptor_identity() -> None:
    service = _access_service()
    composition = _build(service)

    result = composition.application_service.parse(
        DocumentContentParsingRequest(
            document_id=service.descriptor.document_id,
        )
    )

    assert result.descriptor is service.descriptor
