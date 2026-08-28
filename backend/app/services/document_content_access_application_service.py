"""Application boundary for verified canonical Document Content access."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from dataclasses import dataclass
from hashlib import sha256
from typing import BinaryIO

from app.document.repository import EnterpriseDocumentRepository
from app.document_content.repository import DocumentContentRepository
from app.document_content.store import DocumentContentStore
from app.domain.base import EntityId
from app.domain.document_content import DocumentContentDescriptor


_READ_CHUNK_SIZE = 1024 * 1024


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentAccessRequest:
    """Immutable input for one canonical Document Content access."""

    document_id: EntityId


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentAccess:
    """Verified canonical descriptor and context-bound binary payload."""

    descriptor: DocumentContentDescriptor
    payload: BinaryIO


class DocumentContentAccessDocumentNotFoundError(Exception):
    """Raised when the requested canonical Enterprise Document is absent."""


class DocumentContentAccessContentNotFoundError(Exception):
    """Raised when canonical Document Content is currently absent."""


class DocumentContentAccessIntegrityError(Exception):
    """Raised when observed canonical content is unsafe for delivery."""


def _measure_stream(
    source: BinaryIO,
) -> tuple[int, str]:
    digest = sha256()
    byte_length = 0

    while True:
        chunk = source.read(_READ_CHUNK_SIZE)

        if not isinstance(chunk, bytes):
            raise TypeError(
                "Binary payload read() must return bytes."
            )

        if chunk == b"":
            break

        byte_length += len(chunk)
        digest.update(chunk)

    return byte_length, digest.hexdigest()


class DocumentContentAccessApplicationService:
    """Provide verified read-only access to canonical Document Content."""

    def __init__(
        self,
        *,
        document_repository: EnterpriseDocumentRepository,
        content_repository: DocumentContentRepository,
        content_store: DocumentContentStore,
    ) -> None:
        self._document_repository = document_repository
        self._content_repository = content_repository
        self._content_store = content_store

    def open(
        self,
        request: DocumentContentAccessRequest,
    ) -> AbstractContextManager[DocumentContentAccess]:
        """Return one context-managed verified canonical content access."""
        return self._open(request)

    @contextmanager
    def _open(
        self,
        request: DocumentContentAccessRequest,
    ) -> Iterator[DocumentContentAccess]:
        document = self._document_repository.get(
            request.document_id
        )

        if document is None:
            raise DocumentContentAccessDocumentNotFoundError(
                f"Enterprise Document '{request.document_id}' was not found."
            )

        descriptor = self._content_repository.get(
            request.document_id
        )

        opened_payload = self._content_store.open(
            request.document_id
        )

        if opened_payload is None:
            if descriptor is None:
                raise DocumentContentAccessContentNotFoundError(
                    "Canonical Document Content is not present."
                )

            raise DocumentContentAccessIntegrityError(
                "Canonical Document Content descriptor exists "
                "while its binary payload is absent."
            )

        with opened_payload as verification_payload:
            if descriptor is None:
                raise DocumentContentAccessIntegrityError(
                    "Canonical binary Document Content exists "
                    "while its descriptor is absent."
                )

            payload_length, payload_digest = _measure_stream(
                verification_payload
            )

            if (
                payload_length != descriptor.byte_length
                or payload_digest != descriptor.digest.value
            ):
                raise DocumentContentAccessIntegrityError(
                    "Canonical Document Content descriptor and payload "
                    "do not agree."
                )

        delivery_payload = self._content_store.open(
            request.document_id
        )

        if delivery_payload is None:
            raise DocumentContentAccessIntegrityError(
                "Verified canonical Document Content became unavailable "
                "before delivery access."
            )

        with delivery_payload as payload:
            yield DocumentContentAccess(
                descriptor=descriptor,
                payload=payload,
            )
