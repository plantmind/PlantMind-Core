"""Strict UTF-8 parser for canonical plain-text Document Content."""

from __future__ import annotations

from codecs import getincrementaldecoder
from typing import BinaryIO

from app.document_parsing.parser import (
    DocumentContentParser,
    DocumentContentParserInvalidContentError,
    DocumentContentParserUnsupportedMediaTypeError,
)
from app.domain.document_content import DocumentContentDescriptor


_READ_SIZE = 1024 * 1024
_ENCODING = "utf-8-sig"
_ERRORS = "strict"


class Utf8PlainTextDocumentContentParser(
    DocumentContentParser
):
    """Decode canonical ``text/plain`` payloads as strict UTF-8."""

    __slots__ = ()

    def parse(
        self,
        *,
        descriptor: DocumentContentDescriptor,
        payload: BinaryIO,
    ) -> str:
        """Decode one borrowed payload from its current position to EOF."""
        if not isinstance(
            descriptor,
            DocumentContentDescriptor,
        ):
            raise TypeError(
                "Document Content plain-text parser descriptor must be "
                "a DocumentContentDescriptor."
            )

        if descriptor.media_type.value != "text/plain":
            raise DocumentContentParserUnsupportedMediaTypeError(
                "UTF-8 plain-text parser supports only canonical "
                "'text/plain'."
            )

        decoder = getincrementaldecoder(
            _ENCODING
        )(
            errors=_ERRORS,
        )
        decoded_parts: list[str] = []

        while True:
            chunk = payload.read(_READ_SIZE)

            if type(chunk) is not bytes:
                raise TypeError(
                    "Document Content plain-text payload read must "
                    "return exact bytes."
                )

            if chunk == b"":
                break

            try:
                decoded = decoder.decode(
                    chunk,
                    final=False,
                )
            except UnicodeDecodeError as exc:
                raise DocumentContentParserInvalidContentError(
                    "Document Content plain-text payload is not "
                    "valid strict UTF-8."
                ) from exc

            if decoded:
                decoded_parts.append(decoded)

        try:
            final_text = decoder.decode(
                b"",
                final=True,
            )
        except UnicodeDecodeError as exc:
            raise DocumentContentParserInvalidContentError(
                "Document Content plain-text payload is not "
                "valid strict UTF-8."
            ) from exc

        if final_text:
            decoded_parts.append(final_text)

        return "".join(decoded_parts)
