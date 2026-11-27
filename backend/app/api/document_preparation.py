"""Explicit bounded HTTP transport for canonical Document preparation."""

from __future__ import annotations

from hashlib import sha256
from io import BytesIO
import json
import re
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response
from starlette.concurrency import run_in_threadpool

from app.core.runtime import Runtime
from app.document.repository import EnterpriseDocumentAlreadyExistsError
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
from app.services.enterprise_document_registration_application_service import (
    EnterpriseDocumentRegistrationApplicationService,
    EnterpriseDocumentRegistrationRequest,
)


_METADATA_LIMIT = 65_536
_CONTENT_LIMIT = 8_388_608
_REGISTRATION_FIELDS = frozenset({
    "document_type", "title", "source_type", "source_reference",
})
_ADMISSION_DETAIL = "PlantMind is not accepting operational requests."


def _error(status_code: int, code: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code})


def _require_admission(runtime: Runtime) -> None:
    if not runtime.is_request_admission_enabled:
        raise HTTPException(status_code=503, detail=_ADMISSION_DETAIL)


def _check_encoding(request: Request) -> None:
    values = request.headers.getlist("content-encoding")
    if values and (len(values) != 1 or values[0].strip(" \t").lower() != "identity"):
        raise _error(415, "DOCUMENT_TRANSPORT_ENCODING_UNSUPPORTED")


def _check_registration_media_type(request: Request) -> None:
    values = request.headers.getlist("content-type")
    if len(values) != 1 or re.fullmatch(
        r'application/json(?:[ \t]*;[ \t]*charset[ \t]*=[ \t]*(?:utf-8|"utf-8"))?',
        values[0].strip(" \t"), flags=re.IGNORECASE | re.ASCII,
    ) is None:
        raise _error(415, "DOCUMENT_REGISTRATION_MEDIA_TYPE_UNSUPPORTED")


async def _read_limited(request: Request, limit: int) -> bytes:
    body = bytearray()
    async for chunk in request.stream():
        if len(body) + len(chunk) > limit:
            raise _error(413, "DOCUMENT_REQUEST_TOO_LARGE")
        body.extend(chunk)
    return bytes(body)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError("Duplicate JSON key.")
        result[name] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ValueError("Non-JSON numeric constant.")


def _registration_input(
    body: bytes,
) -> tuple[EnterpriseDocumentRegistrationRequest, tuple[str, str, str, str]]:
    try:
        values = json.loads(
            body.decode("utf-8"), object_pairs_hook=_unique_object,
            parse_constant=_invalid_constant,
        )
    except (UnicodeDecodeError, ValueError, RecursionError) as exc:
        raise _error(422, "DOCUMENT_REGISTRATION_INVALID") from exc
    if not isinstance(values, dict) or set(values) != _REGISTRATION_FIELDS:
        raise _error(422, "DOCUMENT_REGISTRATION_INVALID")
    if any(not isinstance(value, str) or not value.strip() for value in values.values()):
        raise _error(422, "DOCUMENT_REGISTRATION_INVALID")
    try:
        document_type = DocumentType(value=values["document_type"])
        source = DocumentSource(
            source_type=DocumentSourceType(value=values["source_type"]),
            source_reference=values["source_reference"],
        )
    except DomainException as exc:
        raise _error(422, "DOCUMENT_REGISTRATION_INVALID") from exc
    expected = (document_type.value, values["title"].strip(),
                source.source_type.value, source.source_reference)
    return EnterpriseDocumentRegistrationRequest(**values), expected


def _canonical_uuid(identity: EntityId) -> str:
    if not isinstance(identity, EntityId) or not isinstance(identity.value, UUID):
        raise TypeError("Expected a canonical EntityId containing a UUID.")
    return str(UUID(int=identity.value.int))


def _registration_response(
    document: EnterpriseDocument, expected: tuple[str, str, str, str],
) -> Response:
    if not isinstance(document, EnterpriseDocument):
        raise TypeError("Expected a canonical EnterpriseDocument.")
    document_id = _canonical_uuid(document.id)
    document_type, title, source = document.document_type, document.title, document.source
    if not isinstance(document_type, DocumentType) or not isinstance(source, DocumentSource):
        raise TypeError("Expected canonical document value objects.")
    source_type, source_reference = source.source_type, source.source_reference
    if not isinstance(source_type, DocumentSourceType):
        raise TypeError("Expected a canonical source classification.")
    actual = (document_type.value, title, source_type.value, source_reference)
    if any(type(value) is not str for value in actual) or actual != expected:
        raise ValueError("Returned document metadata differs from the request.")
    payload = {
        "document_id": document_id, "document_type": actual[0], "title": actual[1],
        "source_type": actual[2], "source_reference": actual[3],
    }
    return Response(
        content=json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8"),
        status_code=201, media_type="application/json",
    )


def _register(
    service: EnterpriseDocumentRegistrationApplicationService, runtime: Runtime,
    request: EnterpriseDocumentRegistrationRequest, expected: tuple[str, str, str, str],
) -> Response:
    _require_admission(runtime)
    try:
        document = service.register(request)
    except EnterpriseDocumentAlreadyExistsError as exc:
        raise _error(409, "DOCUMENT_IDENTITY_CONFLICT") from exc
    except Exception as exc:
        raise _error(500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN") from exc
    try:
        return _registration_response(document, expected)
    except Exception as exc:
        raise _error(500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN") from exc


def _content_response(
    descriptor: DocumentContentDescriptor, document_id: EntityId,
    media_type: DocumentContentMediaType, body: bytes,
) -> Response:
    if not isinstance(descriptor, DocumentContentDescriptor):
        raise TypeError("Expected a canonical DocumentContentDescriptor.")
    returned_id = _canonical_uuid(descriptor.document_id)
    returned_media, length, digest = descriptor.media_type, descriptor.byte_length, descriptor.digest
    if not isinstance(returned_media, DocumentContentMediaType) or not isinstance(digest, DocumentContentDigest):
        raise TypeError("Expected canonical content value objects.")
    media_value, digest_value = returned_media.value, digest.value
    if type(media_value) is not str or type(digest_value) is not str:
        raise TypeError("Expected canonical content strings.")
    if (DocumentContentMediaType(value=media_value).value != media_value
            or DocumentContentDigest(value=digest_value).value != digest_value):
        raise ValueError("Returned content values are not normalized.")
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError("Expected a nonnegative integer content length.")
    length = int.__int__(length)
    if length < 0:
        raise ValueError("Expected a nonnegative content length.")
    if (returned_id != _canonical_uuid(document_id) or media_value != media_type.value
            or length != len(body) or digest_value != sha256(body).hexdigest()):
        raise ValueError("Returned content descriptor differs from the received content.")
    payload = {
        "document_id": returned_id, "media_type": media_value,
        "byte_length": length, "digest": digest_value,
    }
    return Response(
        content=json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8"),
        status_code=200, media_type="application/json",
    )


def _establish(
    service: DocumentContentEstablishmentApplicationService, runtime: Runtime,
    document_id: EntityId, media_type: DocumentContentMediaType, body: bytes,
) -> Response:
    with BytesIO(body) as source:
        request = DocumentContentEstablishmentRequest(
            document_id=document_id, media_type=media_type.value, source=source,
        )
        _require_admission(runtime)
        try:
            descriptor = service.establish(request)
        except DocumentContentEstablishmentDocumentNotFoundError as exc:
            raise _error(404, "DOCUMENT_NOT_FOUND") from exc
        except DocumentContentEstablishmentConflictError as exc:
            raise _error(409, "DOCUMENT_CONTENT_CONFLICT") from exc
        except DocumentContentEstablishmentIntegrityError as exc:
            raise _error(409, "DOCUMENT_CONTENT_INTEGRITY_FAILURE") from exc
        except Exception as exc:
            raise _error(500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN") from exc
        try:
            return _content_response(descriptor, document_id, media_type, body)
        except Exception as exc:
            raise _error(500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN") from exc


def create_router(
    *,
    document_registration_service: EnterpriseDocumentRegistrationApplicationService,
    document_content_establishment_service: DocumentContentEstablishmentApplicationService,
    runtime: Runtime,
) -> APIRouter:
    if not isinstance(document_registration_service, EnterpriseDocumentRegistrationApplicationService):
        raise TypeError("document_registration_service must be canonical.")
    if not isinstance(document_content_establishment_service, DocumentContentEstablishmentApplicationService):
        raise TypeError("document_content_establishment_service must be canonical.")
    if not isinstance(runtime, Runtime):
        raise TypeError("runtime must be canonical.")
    router = APIRouter()

    @router.post("/documents", status_code=201)
    async def register_document(request: Request) -> Response:
        _require_admission(runtime)
        _check_encoding(request)
        _check_registration_media_type(request)
        body = await _read_limited(request, _METADATA_LIMIT)
        registration, expected = _registration_input(body)
        return await run_in_threadpool(
            _register, document_registration_service, runtime, registration, expected,
        )

    @router.put("/documents/{document_id}/content", status_code=200)
    async def establish_content(request: Request) -> Response:
        _require_admission(runtime)
        _check_encoding(request)
        try:
            document_id = EntityId.from_string(request.path_params["document_id"])
        except DomainException as exc:
            raise _error(422, "DOCUMENT_ID_INVALID") from exc
        values = request.headers.getlist("content-type")
        if len(values) != 1:
            raise _error(422, "DOCUMENT_CONTENT_MEDIA_TYPE_INVALID")
        try:
            media_type = DocumentContentMediaType(value=values[0])
        except DomainException as exc:
            raise _error(422, "DOCUMENT_CONTENT_MEDIA_TYPE_INVALID") from exc
        body = await _read_limited(request, _CONTENT_LIMIT)
        return await run_in_threadpool(
            _establish, document_content_establishment_service, runtime, document_id, media_type, body,
        )

    return router
