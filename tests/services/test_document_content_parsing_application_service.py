"""RFC-074 Document Content parsing Application boundary tests."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from dataclasses import FrozenInstanceError, fields
from hashlib import sha256
from io import BytesIO
from typing import BinaryIO, cast

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
    DocumentContentAccessApplicationService,
    DocumentContentAccessRequest,
)
from app.services.document_content_parsing_application_service import (
    DocumentContentParsingApplicationService,
    DocumentContentParsingRequest,
    DocumentContentParsingResult,
)


def _descriptor(
    document_id: EntityId,
    payload: bytes,
) -> DocumentContentDescriptor:
    return DocumentContentDescriptor(
        document_id=document_id,
        media_type=DocumentContentMediaType(
            value="application/pdf"
        ),
        byte_length=len(payload),
        digest=DocumentContentDigest(
            value=sha256(payload).hexdigest()
        ),
    )


class RecordingAccessService:
    def __init__(
        self,
        *,
        descriptor: DocumentContentDescriptor,
        payload: bytes,
    ) -> None:
        self.descriptor = descriptor
        self.payload = BytesIO(payload)
        self.requests: list[DocumentContentAccessRequest] = []
        self.active = False
        self.exit_count = 0

    def open(
        self,
        request: DocumentContentAccessRequest,
    ) -> AbstractContextManager[DocumentContentAccess]:
        self.requests.append(request)
        return self._open()

    @contextmanager
    def _open(self) -> Iterator[DocumentContentAccess]:
        self.active = True

        try:
            yield DocumentContentAccess(
                descriptor=self.descriptor,
                payload=self.payload,
            )
        finally:
            self.active = False
            self.exit_count += 1
            self.payload.close()


class RecordingParser(DocumentContentParser):
    def __init__(
        self,
        access_service: RecordingAccessService,
        outcome: object,
    ) -> None:
        self._access_service = access_service
        self._outcome = outcome
        self.calls = 0
        self.descriptor: DocumentContentDescriptor | None = None
        self.payload_id: int | None = None
        self.active_during_parse = False
        self.payload_closed_during_parse = True

    def parse(
        self,
        *,
        descriptor: DocumentContentDescriptor,
        payload: BinaryIO,
    ) -> str:
        self.calls += 1
        self.descriptor = descriptor
        self.payload_id = id(payload)
        self.active_during_parse = self._access_service.active
        self.payload_closed_during_parse = payload.closed

        if isinstance(self._outcome, BaseException):
            raise self._outcome

        return cast(str, self._outcome)


class ExplodingStringConversion:
    def __str__(self) -> str:
        raise AssertionError(
            "RFC-074 must not coerce parser output through str()."
        )


class FailingAccessService:
    def __init__(self, failure: BaseException) -> None:
        self.failure = failure

    def open(
        self,
        request: DocumentContentAccessRequest,
    ) -> AbstractContextManager[DocumentContentAccess]:
        del request
        raise self.failure


def _service(
    access_service: object,
    parser: DocumentContentParser,
) -> DocumentContentParsingApplicationService:
    return DocumentContentParsingApplicationService(
        content_access_service=cast(
            DocumentContentAccessApplicationService,
            access_service,
        ),
        parser=parser,
    )


def test_request_contract_is_exact_and_immutable() -> None:
    assert [
        field.name
        for field in fields(DocumentContentParsingRequest)
    ] == ["document_id"]

    request = DocumentContentParsingRequest(
        document_id=EntityId.new()
    )

    with pytest.raises(FrozenInstanceError):
        request.document_id = EntityId.new()  # type: ignore[misc]


def test_result_contract_is_exact_and_immutable() -> None:
    assert [
        field.name
        for field in fields(DocumentContentParsingResult)
    ] == ["descriptor", "text"]

    document_id = EntityId.new()
    payload = b"canonical"

    result = DocumentContentParsingResult(
        descriptor=_descriptor(document_id, payload),
        text="parsed",
    )

    with pytest.raises(FrozenInstanceError):
        result.text = "changed"  # type: ignore[misc]


def test_parser_port_has_exact_abstract_operation() -> None:
    assert DocumentContentParser.__abstractmethods__ == frozenset(
        {"parse"}
    )
    assert getattr(
        DocumentContentParser.parse,
        "__isabstractmethod__",
        False,
    )


def test_parsing_uses_verified_access_context_and_preserves_text() -> None:
    document_id = EntityId.new()
    payload = b"verified-content"
    descriptor = _descriptor(document_id, payload)

    access = RecordingAccessService(
        descriptor=descriptor,
        payload=payload,
    )
    parser = RecordingParser(
        access,
        "  parsed\ntext  ",
    )
    service = _service(access, parser)

    result = service.parse(
        DocumentContentParsingRequest(
            document_id=document_id
        )
    )

    assert result.descriptor is descriptor
    assert result.text == "  parsed\ntext  "

    assert access.requests == [
        DocumentContentAccessRequest(
            document_id=document_id
        )
    ]

    assert parser.calls == 1
    assert parser.descriptor is descriptor
    assert parser.payload_id == id(access.payload)
    assert parser.active_during_parse is True
    assert parser.payload_closed_during_parse is False

    assert access.active is False
    assert access.exit_count == 1
    assert access.payload.closed is True


def test_empty_text_is_valid_success() -> None:
    document_id = EntityId.new()
    payload = b"verified"
    descriptor = _descriptor(document_id, payload)

    access = RecordingAccessService(
        descriptor=descriptor,
        payload=payload,
    )
    parser = RecordingParser(access, "")
    service = _service(access, parser)

    result = service.parse(
        DocumentContentParsingRequest(
            document_id=document_id
        )
    )

    assert result.text == ""
    assert access.exit_count == 1
    assert access.payload.closed is True


def test_non_str_parser_result_fails_without_coercion() -> None:
    document_id = EntityId.new()
    payload = b"verified"
    descriptor = _descriptor(document_id, payload)

    access = RecordingAccessService(
        descriptor=descriptor,
        payload=payload,
    )
    parser = RecordingParser(
        access,
        ExplodingStringConversion(),
    )
    service = _service(access, parser)

    with pytest.raises(
        TypeError,
        match="Document Content parser must return str",
    ):
        service.parse(
            DocumentContentParsingRequest(
                document_id=document_id
            )
        )

    assert access.active is False
    assert access.exit_count == 1
    assert access.payload.closed is True


@pytest.mark.parametrize(
    "failure",
    [
        DocumentContentParserUnsupportedMediaTypeError(
            "unsupported"
        ),
        DocumentContentParserInvalidContentError(
            "invalid"
        ),
    ],
)
def test_parser_contract_failures_propagate_unchanged(
    failure: Exception,
) -> None:
    document_id = EntityId.new()
    payload = b"verified"
    descriptor = _descriptor(document_id, payload)

    access = RecordingAccessService(
        descriptor=descriptor,
        payload=payload,
    )
    parser = RecordingParser(access, failure)
    service = _service(access, parser)

    with pytest.raises(type(failure)) as exc_info:
        service.parse(
            DocumentContentParsingRequest(
                document_id=document_id
            )
        )

    assert exc_info.value is failure
    assert access.active is False
    assert access.exit_count == 1
    assert access.payload.closed is True


def test_operational_parser_failure_propagates_unchanged() -> None:
    document_id = EntityId.new()
    payload = b"verified"
    descriptor = _descriptor(document_id, payload)
    failure = OSError("parser infrastructure failed")

    access = RecordingAccessService(
        descriptor=descriptor,
        payload=payload,
    )
    parser = RecordingParser(access, failure)
    service = _service(access, parser)

    with pytest.raises(OSError) as exc_info:
        service.parse(
            DocumentContentParsingRequest(
                document_id=document_id
            )
        )

    assert exc_info.value is failure
    assert access.exit_count == 1
    assert access.payload.closed is True


def test_access_failure_propagates_unchanged() -> None:
    failure = RuntimeError("access failed")

    parser = cast(
        DocumentContentParser,
        object(),
    )
    service = _service(
        FailingAccessService(failure),
        parser,
    )

    with pytest.raises(RuntimeError) as exc_info:
        service.parse(
            DocumentContentParsingRequest(
                document_id=EntityId.new()
            )
        )

    assert exc_info.value is failure


def test_application_result_never_exposes_payload() -> None:
    assert "payload" not in {
        field.name
        for field in fields(DocumentContentParsingResult)
    }
