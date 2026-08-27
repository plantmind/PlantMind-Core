"""Application boundary for canonical Document Content establishment."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import BinaryIO

from app.document.repository import EnterpriseDocumentRepository
from app.document_content.repository import (
    DocumentContentAlreadyExistsError,
    DocumentContentRepository,
)
from app.document_content.store import (
    DocumentContentPayloadAlreadyExistsError,
    DocumentContentStore,
)
from app.domain.base import EntityId
from app.domain.document_content import (
    DocumentContentDescriptor,
    DocumentContentDigest,
    DocumentContentMediaType,
)


_READ_CHUNK_SIZE = 1024 * 1024


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentEstablishmentRequest:
    """Immutable input for one canonical Document Content establishment."""

    document_id: EntityId
    media_type: str
    source: BinaryIO


class DocumentContentEstablishmentDocumentNotFoundError(Exception):
    """Raised when the requested canonical Enterprise Document is absent."""


class DocumentContentEstablishmentConflictError(Exception):
    """Raised when the request conflicts with canonical Document Content."""


class DocumentContentEstablishmentIntegrityError(Exception):
    """Raised when persisted canonical Document Content is inconsistent."""


class _MeasuringBinarySource:
    """Read-through source measuring exactly the bytes yielded downstream."""

    def __init__(
        self,
        source: BinaryIO,
    ) -> None:
        self._source = source
        self._byte_length = 0
        self._digest = sha256()

    def read(
        self,
        size: int = -1,
    ) -> bytes:
        chunk = self._source.read(size)

        if not isinstance(chunk, bytes):
            raise TypeError(
                "Binary source read() must return bytes."
            )

        self._byte_length += len(chunk)
        self._digest.update(chunk)

        return chunk

    def readinto(
        self,
        buffer: bytearray | memoryview,
    ) -> int:
        chunk = self.read(len(buffer))
        length = len(chunk)
        buffer[:length] = chunk

        return length

    @property
    def byte_length(self) -> int:
        return self._byte_length

    @property
    def digest_hex(self) -> str:
        return self._digest.hexdigest()


def _measure_stream(
    source: BinaryIO,
) -> tuple[int, str]:
    digest = sha256()
    byte_length = 0

    while True:
        chunk = source.read(_READ_CHUNK_SIZE)

        if not isinstance(chunk, bytes):
            raise TypeError(
                "Binary source read() must return bytes."
            )

        if chunk == b"":
            break

        byte_length += len(chunk)
        digest.update(chunk)

    return byte_length, digest.hexdigest()


class DocumentContentEstablishmentApplicationService:
    """Coordinate canonical descriptor and binary-content establishment."""

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

    def establish(
        self,
        request: DocumentContentEstablishmentRequest,
    ) -> DocumentContentDescriptor:
        """Establish or verify one coherent canonical Document Content state."""
        document = self._document_repository.get(
            request.document_id
        )

        if document is None:
            raise DocumentContentEstablishmentDocumentNotFoundError(
                f"Enterprise Document '{request.document_id}' was not found."
            )

        descriptor = self._content_repository.get(
            request.document_id
        )

        opened_payload = self._content_store.open(
            request.document_id
        )

        if opened_payload is None:
            if descriptor is not None:
                raise DocumentContentEstablishmentIntegrityError(
                    "Canonical Document Content descriptor exists "
                    "while its binary payload is absent."
                )

            return self._establish_fresh(request)

        with opened_payload as payload:
            if descriptor is None:
                return self._recover_payload_only(
                    request,
                    payload,
                )

            return self._verify_complete(
                request,
                descriptor,
                payload,
            )

    def _establish_fresh(
        self,
        request: DocumentContentEstablishmentRequest,
    ) -> DocumentContentDescriptor:
        media_type = DocumentContentMediaType(
            value=request.media_type
        )

        measured_source = _MeasuringBinarySource(
            request.source
        )

        try:
            self._content_store.add(
                request.document_id,
                measured_source,  # type: ignore[arg-type]
            )
        except DocumentContentPayloadAlreadyExistsError as exc:
            raise DocumentContentEstablishmentConflictError(
                "Binary Document Content was established concurrently."
            ) from exc

        descriptor = DocumentContentDescriptor(
            document_id=request.document_id,
            media_type=media_type,
            byte_length=measured_source.byte_length,
            digest=DocumentContentDigest(
                value=measured_source.digest_hex
            ),
        )

        return self._persist_or_reconcile_descriptor(
            descriptor
        )

    def _recover_payload_only(
        self,
        request: DocumentContentEstablishmentRequest,
        payload: BinaryIO,
    ) -> DocumentContentDescriptor:
        payload_length, payload_digest = _measure_stream(
            payload
        )

        source_length, source_digest = _measure_stream(
            request.source
        )

        if (
            source_length != payload_length
            or source_digest != payload_digest
        ):
            raise DocumentContentEstablishmentConflictError(
                "Caller content differs from the canonical binary payload."
            )

        media_type = DocumentContentMediaType(
            value=request.media_type
        )

        descriptor = DocumentContentDescriptor(
            document_id=request.document_id,
            media_type=media_type,
            byte_length=payload_length,
            digest=DocumentContentDigest(
                value=payload_digest
            ),
        )

        return self._persist_or_reconcile_descriptor(
            descriptor
        )

    def _verify_complete(
        self,
        request: DocumentContentEstablishmentRequest,
        descriptor: DocumentContentDescriptor,
        payload: BinaryIO,
    ) -> DocumentContentDescriptor:
        requested_media_type = DocumentContentMediaType(
            value=request.media_type
        )

        if requested_media_type != descriptor.media_type:
            raise DocumentContentEstablishmentConflictError(
                "Requested media type differs from canonical "
                "Document Content."
            )

        payload_length, payload_digest = _measure_stream(
            payload
        )

        if (
            payload_length != descriptor.byte_length
            or payload_digest != descriptor.digest.value
        ):
            raise DocumentContentEstablishmentIntegrityError(
                "Canonical Document Content descriptor and payload "
                "do not agree."
            )

        source_length, source_digest = _measure_stream(
            request.source
        )

        if (
            source_length != payload_length
            or source_digest != payload_digest
        ):
            raise DocumentContentEstablishmentConflictError(
                "Caller content differs from canonical Document Content."
            )

        return descriptor

    def _persist_or_reconcile_descriptor(
        self,
        descriptor: DocumentContentDescriptor,
    ) -> DocumentContentDescriptor:
        try:
            self._content_repository.add(
                descriptor
            )
        except DocumentContentAlreadyExistsError as exc:
            observed = self._content_repository.get(
                descriptor.document_id
            )

            if observed == descriptor:
                return observed

            raise DocumentContentEstablishmentConflictError(
                "Canonical Document Content descriptor was established "
                "concurrently with different or unverifiable state."
            ) from exc

        return descriptor
