"""RFC-077 strict UTF-8 plain-text parser behavior tests."""

from __future__ import annotations

from hashlib import sha256
from importlib import import_module
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


READ_SIZE = 1024 * 1024
UTF8_BOM = b"\xef\xbb\xbf"


def _module():
    return import_module(
        "app.infrastructure.document_parsing.utf8_plain_text_parser"
    )


def _parser() -> DocumentContentParser:
    return _module().Utf8PlainTextDocumentContentParser()


def _descriptor(
    *,
    payload: bytes = b"",
    media_type: str = "text/plain",
    byte_length: int | None = None,
    digest: str | None = None,
) -> DocumentContentDescriptor:
    return DocumentContentDescriptor(
        document_id=EntityId.new(),
        media_type=DocumentContentMediaType(
            value=media_type,
        ),
        byte_length=(
            len(payload)
            if byte_length is None
            else byte_length
        ),
        digest=DocumentContentDigest(
            value=(
                sha256(payload).hexdigest()
                if digest is None
                else digest
            ),
        ),
    )


class NeverReadPayload:
    def read(self, size: int = -1) -> bytes:
        raise AssertionError("payload must not be read")


class ScriptedPayload:
    def __init__(self, chunks: list[object]) -> None:
        self._chunks = list(chunks)
        self.read_sizes: list[int] = []
        self.read_calls = 0

    def read(self, size: int = -1) -> object:
        self.read_calls += 1
        self.read_sizes.append(size)

        if self._chunks:
            return self._chunks.pop(0)

        return b""


class OneBytePayload:
    def __init__(self, payload: bytes) -> None:
        self._payload = payload
        self._index = 0
        self.read_sizes: list[int] = []

    def read(self, size: int = -1) -> bytes:
        self.read_sizes.append(size)

        if self._index >= len(self._payload):
            return b""

        result = self._payload[
            self._index:self._index + 1
        ]
        self._index += 1
        return result


class FailingPayload:
    def __init__(self, failure: BaseException) -> None:
        self.failure = failure
        self.read_sizes: list[int] = []

    def read(self, size: int = -1) -> bytes:
        self.read_sizes.append(size)
        raise self.failure


class ForbiddenLifecyclePayload:
    def __init__(self, payload: bytes) -> None:
        self._payload = payload
        self._offset = 0
        self.read_sizes: list[int] = []

    def read(self, size: int = -1) -> bytes:
        self.read_sizes.append(size)

        if self._offset >= len(self._payload):
            return b""

        result = self._payload[
            self._offset:self._offset + size
        ]
        self._offset += len(result)
        return result

    def seek(self, *args: object, **kwargs: object) -> int:
        raise AssertionError("parser must not seek")

    def tell(self) -> int:
        raise AssertionError("parser must not tell")

    def fileno(self) -> int:
        raise AssertionError("parser must not require fileno")

    def close(self) -> None:
        raise AssertionError("parser must not close")


class SinglePassPayload:
    def __init__(self, chunks: list[bytes]) -> None:
        self._chunks = list(chunks)
        self.eof_returned = False
        self.read_sizes: list[int] = []

    def read(self, size: int = -1) -> bytes:
        self.read_sizes.append(size)

        if self.eof_returned:
            raise AssertionError("parser attempted a read after EOF")

        if self._chunks:
            return self._chunks.pop(0)

        self.eof_returned = True
        return b""


def test_parser_implements_existing_port() -> None:
    parser = _parser()

    assert isinstance(
        parser,
        DocumentContentParser,
    )


def test_parser_is_stateless_and_reusable() -> None:
    parser = _parser()

    first_payload = UTF8_BOM + "أول".encode("utf-8")
    second_payload = "ثانٍ".encode("utf-8")

    assert vars(parser) == {}

    assert parser.parse(
        descriptor=_descriptor(payload=first_payload),
        payload=BytesIO(first_payload),
    ) == "أول"

    assert parser.parse(
        descriptor=_descriptor(payload=second_payload),
        payload=BytesIO(second_payload),
    ) == "ثانٍ"

    assert vars(parser) == {}


def test_non_descriptor_fails_before_payload_read() -> None:
    with pytest.raises(
        TypeError,
        match="descriptor must be a DocumentContentDescriptor",
    ):
        _parser().parse(
            descriptor=cast(
                DocumentContentDescriptor,
                object(),
            ),
            payload=cast(
                BinaryIO,
                NeverReadPayload(),
            ),
        )


def test_unsupported_media_type_fails_before_payload_read() -> None:
    descriptor = _descriptor(
        payload=b"text",
        media_type="application/pdf",
    )

    with pytest.raises(
        DocumentContentParserUnsupportedMediaTypeError,
        match="text/plain",
    ):
        _parser().parse(
            descriptor=descriptor,
            payload=cast(
                BinaryIO,
                NeverReadPayload(),
            ),
        )


def test_empty_payload_returns_empty_string() -> None:
    payload = ScriptedPayload([b""])

    result = _parser().parse(
        descriptor=_descriptor(),
        payload=cast(BinaryIO, payload),
    )

    assert result == ""
    assert payload.read_sizes == [READ_SIZE]


def test_ascii_text_decodes_exactly() -> None:
    raw = b"PlantMind plain text"

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=BytesIO(raw),
    )

    assert result == "PlantMind plain text"


def test_multilingual_utf8_decodes_exactly() -> None:
    text = "PlantMind — العربية — 日本語 — 🙂"
    raw = text.encode("utf-8")

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=BytesIO(raw),
    )

    assert result == text


def test_multibyte_codepoints_decode_across_one_byte_reads() -> None:
    text = "A🙂ب漢"
    raw = text.encode("utf-8")
    payload = OneBytePayload(raw)

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=cast(BinaryIO, payload),
    )

    assert result == text
    assert set(payload.read_sizes) == {READ_SIZE}


def test_utf8_without_bom_is_unchanged() -> None:
    text = "\ufeff-not-at-byte-zero"
    raw = ("X" + text).encode("utf-8")

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=BytesIO(raw),
    )

    assert result == "X" + text


def test_one_leading_utf8_bom_is_removed() -> None:
    raw = UTF8_BOM + "text".encode("utf-8")

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=BytesIO(raw),
    )

    assert result == "text"


def test_split_leading_utf8_bom_is_removed() -> None:
    raw = UTF8_BOM + b"A"
    payload = ScriptedPayload(
        [
            b"\xef",
            b"\xbb",
            b"\xbfA",
            b"",
        ]
    )

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=cast(BinaryIO, payload),
    )

    assert result == "A"
    assert payload.read_sizes == [
        READ_SIZE,
        READ_SIZE,
        READ_SIZE,
        READ_SIZE,
    ]


def test_second_leading_bom_is_preserved() -> None:
    raw = UTF8_BOM + UTF8_BOM + b"text"

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=BytesIO(raw),
    )

    assert result == "\ufefftext"


def test_internal_ufeff_is_preserved() -> None:
    raw = b"A" + UTF8_BOM + b"B"

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=BytesIO(raw),
    )

    assert result == "A\ufeffB"


def test_newline_sequences_are_preserved_exactly() -> None:
    text = "A\r\nB\rC\nD\r\n\nE"
    raw = text.encode("utf-8")

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=BytesIO(raw),
    )

    assert result == text


def test_whitespace_tabs_nul_and_controls_are_preserved() -> None:
    text = " \tA\x00B\x01C \n"
    raw = text.encode("utf-8")

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=BytesIO(raw),
    )

    assert result == text


def test_invalid_utf8_maps_to_invalid_content_with_cause() -> None:
    raw = b"\xff"

    with pytest.raises(
        DocumentContentParserInvalidContentError
    ) as exc_info:
        _parser().parse(
            descriptor=_descriptor(payload=raw),
            payload=BytesIO(raw),
        )

    assert isinstance(
        exc_info.value.__cause__,
        UnicodeDecodeError,
    )


def test_invalid_content_message_does_not_expose_raw_bytes() -> None:
    raw = b"\xffsecret"

    with pytest.raises(
        DocumentContentParserInvalidContentError
    ) as exc_info:
        _parser().parse(
            descriptor=_descriptor(payload=raw),
            payload=BytesIO(raw),
        )

    message = str(exc_info.value)

    assert "secret" not in message
    assert "\\xff" not in message
    assert "b'" not in message


def test_valid_prefix_followed_by_invalid_tail_fails() -> None:
    raw = b"valid-prefix-" + b"\xff"

    with pytest.raises(
        DocumentContentParserInvalidContentError
    ):
        _parser().parse(
            descriptor=_descriptor(payload=raw),
            payload=cast(
                BinaryIO,
                ScriptedPayload(
                    [
                        b"valid-prefix-",
                        b"\xff",
                        b"",
                    ]
                ),
            ),
        )


def test_incomplete_trailing_sequence_fails_on_final_flush() -> None:
    raw = b"valid" + b"\xf0\x9f"

    with pytest.raises(
        DocumentContentParserInvalidContentError
    ) as exc_info:
        _parser().parse(
            descriptor=_descriptor(payload=raw),
            payload=cast(
                BinaryIO,
                ScriptedPayload(
                    [
                        b"valid",
                        b"\xf0\x9f",
                        b"",
                    ]
                ),
            ),
        )

    assert isinstance(
        exc_info.value.__cause__,
        UnicodeDecodeError,
    )


def test_utf16_bom_fails_as_invalid_utf8() -> None:
    raw = b"\xff\xfeA\x00"

    with pytest.raises(
        DocumentContentParserInvalidContentError
    ):
        _parser().parse(
            descriptor=_descriptor(payload=raw),
            payload=BytesIO(raw),
        )


def test_utf32_bom_fails_as_invalid_utf8() -> None:
    raw = b"\xff\xfe\x00\x00A\x00\x00\x00"

    with pytest.raises(
        DocumentContentParserInvalidContentError
    ):
        _parser().parse(
            descriptor=_descriptor(payload=raw),
            payload=BytesIO(raw),
        )


def test_non_bytes_read_result_raises_typeerror() -> None:
    payload = ScriptedPayload(
        [
            bytearray(b"text"),
        ]
    )

    with pytest.raises(
        TypeError,
        match="read must return exact bytes",
    ):
        _parser().parse(
            descriptor=_descriptor(payload=b"text"),
            payload=cast(BinaryIO, payload),
        )


def test_memoryview_read_result_raises_typeerror() -> None:
    payload = ScriptedPayload(
        [
            memoryview(b"text"),
        ]
    )

    with pytest.raises(
        TypeError,
        match="read must return exact bytes",
    ):
        _parser().parse(
            descriptor=_descriptor(payload=b"text"),
            payload=cast(BinaryIO, payload),
        )


def test_payload_oserror_propagates_same_instance() -> None:
    failure = OSError("payload read failure")
    payload = FailingPayload(failure)

    with pytest.raises(OSError) as exc_info:
        _parser().parse(
            descriptor=_descriptor(),
            payload=cast(BinaryIO, payload),
        )

    assert exc_info.value is failure


def test_payload_unicode_decode_error_propagates_same_instance() -> None:
    failure = UnicodeDecodeError(
        "payload-reader",
        b"x",
        0,
        1,
        "operational reader failure",
    )
    payload = FailingPayload(failure)

    with pytest.raises(UnicodeDecodeError) as exc_info:
        _parser().parse(
            descriptor=_descriptor(),
            payload=cast(BinaryIO, payload),
        )

    assert exc_info.value is failure


def test_every_read_uses_fixed_positive_bounded_size() -> None:
    payload = ScriptedPayload(
        [
            b"A",
            b"B",
            b"",
        ]
    )

    result = _parser().parse(
        descriptor=_descriptor(payload=b"AB"),
        payload=cast(BinaryIO, payload),
    )

    assert result == "AB"
    assert payload.read_sizes == [
        READ_SIZE,
        READ_SIZE,
        READ_SIZE,
    ]
    assert all(size > 0 for size in payload.read_sizes)


def test_parser_starts_at_current_payload_position() -> None:
    raw = b"ignored-prefix" + UTF8_BOM + b"body"
    payload = BytesIO(raw)
    payload.seek(len(b"ignored-prefix"))

    result = _parser().parse(
        descriptor=_descriptor(payload=UTF8_BOM + b"body"),
        payload=payload,
    )

    assert result == "body"


def test_parser_never_uses_seek_tell_fileno_or_close() -> None:
    raw = b"text"
    payload = ForbiddenLifecyclePayload(raw)

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=cast(BinaryIO, payload),
    )

    assert result == "text"
    assert payload.read_sizes == [
        READ_SIZE,
        READ_SIZE,
    ]


def test_parser_does_not_reverify_descriptor_length_or_digest() -> None:
    raw = b"text"
    descriptor = _descriptor(
        payload=raw,
        byte_length=999_999,
        digest="0" * 64,
    )

    result = _parser().parse(
        descriptor=descriptor,
        payload=BytesIO(raw),
    )

    assert result == "text"
    assert descriptor.byte_length == 999_999
    assert descriptor.digest.value == "0" * 64


def test_each_parse_performs_one_forward_pass() -> None:
    raw = b"AB"
    payload = SinglePassPayload(
        [
            b"A",
            b"B",
        ]
    )

    result = _parser().parse(
        descriptor=_descriptor(payload=raw),
        payload=cast(BinaryIO, payload),
    )

    assert result == "AB"
    assert payload.eof_returned is True
    assert payload.read_sizes == [
        READ_SIZE,
        READ_SIZE,
        READ_SIZE,
    ]


def test_parser_retains_no_descriptor_or_payload_after_failure() -> None:
    parser = _parser()
    raw = b"\xff"
    descriptor = _descriptor(payload=raw)
    payload = BytesIO(raw)

    with pytest.raises(
        DocumentContentParserInvalidContentError
    ):
        parser.parse(
            descriptor=descriptor,
            payload=payload,
        )

    assert vars(parser) == {}
