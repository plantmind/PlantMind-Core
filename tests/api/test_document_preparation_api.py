"""RFC-084 bounded transport, dispatch, admission and outcome contracts."""

from __future__ import annotations

import asyncio
from hashlib import sha256
from importlib import import_module, util
from inspect import Parameter, signature
import json
from pathlib import Path
from threading import get_ident
from types import SimpleNamespace
from typing import get_type_hints
from unittest.mock import Mock
from uuid import UUID

import pytest
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.requests import ClientDisconnect

from app.core.runtime import Runtime
from app.document.repository import EnterpriseDocumentAlreadyExistsError
from app.domain.base import DomainException, EntityId
from app.domain.document import DocumentSource, DocumentSourceType, DocumentType, EnterpriseDocument
from app.domain.document_content import DocumentContentDescriptor, DocumentContentDigest, DocumentContentMediaType
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


MODULE = "app.api.document_preparation"
HOST = "app.api.document_knowledge_ingestion_host"
IDENTITY = "1b7e117a-43cf-4eac-b394-f5413810dd69"
ADMISSION = {"detail": "PlantMind is not accepting operational requests."}
SECRET = "do-not-leak /private/documents/body database-password"


def test_preparation_router_factory_is_available():
    """TDD red imports the new module only when this node executes."""
    module = import_module(MODULE)
    assert callable(module.create_router)


def test_existing_host_has_optional_preparation_inputs():
    """Independent TDD red for the existing host's new optional inputs."""
    host = import_module(HOST)
    parameters = signature(host.create_app).parameters
    assert tuple(parameters) == (
        "platform", "document_registration_service", "document_content_establishment_service",
    ), "RFC084_OPTIONAL_PREPARATION_INPUTS_MISSING"
    assert parameters["platform"].default is Parameter.empty
    assert all(item.kind is Parameter.KEYWORD_ONLY for item in parameters.values())
    assert all(parameters[name].default is None for name in tuple(parameters)[1:])


def metadata():
    return {
        "document_type": "  Custom SOP  ", "title": "  Pump تشغيل  ",
        "source_type": "  Manual Import  ", "source_reference": "  opaque://plant/401/file  ",
    }


def document_for(request, identity=None):
    return EnterpriseDocument(
        id=identity if identity is not None else EntityId.new(),
        document_type=DocumentType(value=request.document_type), title=request.title,
        source=DocumentSource(
            source_type=DocumentSourceType(value=request.source_type),
            source_reference=request.source_reference,
        ),
    )


def descriptor_for(request, body):
    return DocumentContentDescriptor(
        document_id=request.document_id,
        media_type=DocumentContentMediaType(value=request.media_type), byte_length=len(body),
        digest=DocumentContentDigest(value=sha256(body).hexdigest()),
    )


class RegistrationSpy(EnterpriseDocumentRegistrationApplicationService):
    def __init__(self):
        self.calls, self.threads = [], []
        self.effect = None

    def register(self, request):
        self.calls.append(request)
        self.threads.append(get_ident())
        if isinstance(self.effect, BaseException):
            raise self.effect
        return self.effect(request) if self.effect is not None else document_for(request)


class EstablishmentSpy(DocumentContentEstablishmentApplicationService):
    def __init__(self):
        self.calls, self.threads, self.bodies, self.positions = [], [], [], []
        self.effect = None

    def establish(self, request):
        self.calls.append(request)
        self.threads.append(get_ident())
        self.positions.append(request.source.tell())
        body = request.source.read()
        self.bodies.append(body)
        if isinstance(self.effect, BaseException):
            raise self.effect
        return self.effect(request, body) if self.effect is not None else descriptor_for(request, body)


@pytest.fixture
def http():
    module = import_module(MODULE)
    runtime = Runtime()
    runtime.enable_request_admission()
    registration, establishment = RegistrationSpy(), EstablishmentSpy()
    app = FastAPI()
    app.include_router(module.create_router(
        document_registration_service=registration,
        document_content_establishment_service=establishment, runtime=runtime,
    ))
    with TestClient(app) as client:
        yield SimpleNamespace(module=module, runtime=runtime, registration=registration,
                              establishment=establishment, app=app, client=client)


def post(http, values=None, *, body=None, headers=None):
    return http.client.post(
        "/documents", content=body if body is not None else json.dumps(
            metadata() if values is None else values,
        ).encode(), headers={"content-type": "application/json"} if headers is None else headers,
    )


def put(http, body=b"payload", *, identity=IDENTITY, headers=None):
    return http.client.put(
        f"/documents/{identity}/content", content=body,
        headers={"content-type": "text/plain"} if headers is None else headers,
    )


def fixed(response, status, code):
    assert response.status_code == status
    assert response.json() == {"detail": {"code": code}}
    assert SECRET not in response.text


def asgi(http, method, path, chunks, headers=(), on_receive=None):
    """Exercise real ASGI chunks, without a client's buffering/header defaults."""
    output, received = [], []
    messages = list(chunks)

    async def receive():
        index = len(received)
        received.append(index)
        if on_receive is not None:
            on_receive(index)
        message = messages[index]
        if isinstance(message, BaseException):
            raise message
        if isinstance(message, dict):
            return message
        return {"type": "http.request", "body": message, "more_body": index + 1 < len(messages)}

    async def send(message):
        output.append(message)

    scope = {
        "type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
        "method": method, "scheme": "http", "path": path, "raw_path": path.encode(),
        "query_string": b"", "headers": list(headers),
        "client": ("127.0.0.1", 1234), "server": ("testserver", 80), "root_path": "",
    }
    asyncio.run(http.app(scope, receive, send))
    status = next(item["status"] for item in output if item["type"] == "http.response.start")
    body = b"".join(item.get("body", b"") for item in output if item["type"] == "http.response.body")
    return status, json.loads(body), received


def test_router_factory_has_exact_required_keyword_only_canonical_inputs(http):
    parameters = signature(http.module.create_router).parameters
    assert tuple(parameters) == (
        "document_registration_service", "document_content_establishment_service", "runtime",
    )
    assert all(p.kind is Parameter.KEYWORD_ONLY and p.default is Parameter.empty for p in parameters.values())
    assert get_type_hints(http.module.create_router) == {
        "document_registration_service": EnterpriseDocumentRegistrationApplicationService,
        "document_content_establishment_service": DocumentContentEstablishmentApplicationService,
        "runtime": Runtime, "return": APIRouter,
    }
    with pytest.raises(TypeError):
        http.module.create_router()
    with pytest.raises(TypeError):
        http.module.create_router(http.registration, http.establishment, http.runtime)


class DuckInput:
    def __bool__(self):
        raise AssertionError("No input truthiness is needed.")

    def __getattr__(self, name):
        raise AssertionError("No duck input inspection is needed.")


@pytest.mark.parametrize("name", ["document_registration_service", "document_content_establishment_service", "runtime"])
@pytest.mark.parametrize("value", [None, False, 0, "service", object(), pytest.param(DuckInput(), id="duck-input")])
def test_invalid_router_inputs_fail_before_construction(http, monkeypatch, name, value):
    constructor = Mock(side_effect=AssertionError("Router was constructed."))
    monkeypatch.setattr(http.module, "APIRouter", constructor)
    inputs = dict(document_registration_service=http.registration,
                  document_content_establishment_service=http.establishment, runtime=http.runtime)
    inputs[name] = value
    with pytest.raises(TypeError):
        http.module.create_router(**inputs)
    constructor.assert_not_called()
    assert http.registration.calls == http.establishment.calls == []


def test_falsey_canonical_inputs_are_preserved_and_assembly_performs_no_work(http):
    class FalseyRegistration(RegistrationSpy):
        def __bool__(self):
            raise AssertionError("Canonical service truthiness must not be read.")

    class FalseyEstablishment(EstablishmentSpy):
        def __bool__(self):
            raise AssertionError("Canonical service truthiness must not be read.")

    class FalseyRuntime(Runtime):
        def __bool__(self):
            raise AssertionError("Canonical runtime truthiness must not be read.")

    registration, establishment, runtime = FalseyRegistration(), FalseyEstablishment(), FalseyRuntime()
    before = runtime.state
    app = FastAPI()
    router = http.module.create_router(document_registration_service=registration,
        document_content_establishment_service=establishment, runtime=runtime)
    assert registration.calls == establishment.calls == []
    assert runtime.state is before and runtime.is_request_admission_enabled is False
    app.include_router(router)
    with TestClient(app) as client:
        assert client.post("/documents", content=b"bad").json() == ADMISSION
        runtime.enable_request_admission()
        assert client.post("/documents", json=metadata()).status_code == 201
        assert client.put(f"/documents/{IDENTITY}/content", content=b"x",
                          headers={"content-type": "text/plain"}).status_code == 200
    assert len(registration.calls) == len(establishment.calls) == 1


def test_import_does_not_construct_router_services_or_runtime(http, monkeypatch):
    import fastapi
    constructors = []
    for owner, name in ((fastapi, "APIRouter"),
        (EnterpriseDocumentRegistrationApplicationService, "__init__"),
        (DocumentContentEstablishmentApplicationService, "__init__"), (Runtime, "__init__")):
        blocked = Mock(side_effect=AssertionError("Import acquired a collaborator."))
        monkeypatch.setattr(owner, name, blocked)
        constructors.append(blocked)
    specification = util.spec_from_file_location("rfc084_import_probe", Path(http.module.__file__))
    isolated = util.module_from_spec(specification)
    specification.loader.exec_module(isolated)
    assert callable(isolated.create_router)
    for constructor in constructors:
        constructor.assert_not_called()


@pytest.mark.parametrize("media", ["application/json", "Application/JSON", "application/json; charset=utf-8",
                                  ' application/json ; CHARSET="UTF-8" '])
def test_registration_normalizes_canonical_result_and_calls_only_registration(http, media):
    values = metadata()
    response = post(http, values, headers={"content-type": media})
    assert response.status_code == 201
    actual = response.json()
    assert set(actual) == {"document_id", "document_type", "title", "source_type", "source_reference"}
    identity = actual.pop("document_id")
    assert str(UUID(identity)) == identity
    assert actual == {"document_type": "custom sop", "title": "Pump تشغيل",
                      "source_type": "manual import", "source_reference": "opaque://plant/401/file"}
    assert len(http.registration.calls) == 1 and http.establishment.calls == []
    assert http.registration.calls[0] == EnterpriseDocumentRegistrationRequest(**values)
    assert "location" not in response.headers


def test_repeating_metadata_performs_explicit_registrations_without_dedup(http):
    first, second = post(http), post(http)
    assert first.status_code == second.status_code == 201
    assert first.json()["document_id"] != second.json()["document_id"]
    assert len(http.registration.calls) == 2 and http.establishment.calls == []


@pytest.mark.parametrize("field", ["document_type", "title", "source_type", "source_reference"])
@pytest.mark.parametrize("value", [None, True, False, 0, 2.5, [], {}, "", " \t\r\n "])
def test_metadata_fields_are_required_strict_nonempty_strings(http, field, value):
    values = metadata()
    values[field] = value
    fixed(post(http, values), 422, "DOCUMENT_REGISTRATION_INVALID")
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("field", ["document_type", "title", "source_type", "source_reference"])
def test_missing_metadata_field_is_rejected(http, field):
    values = metadata()
    del values[field]
    fixed(post(http, values), 422, "DOCUMENT_REGISTRATION_INVALID")
    assert http.registration.calls == []


@pytest.mark.parametrize("field", ["document_id", "digest", "byte_length", "storage_location", "content", "extra"])
def test_caller_cannot_supply_additional_metadata_fields(http, field):
    values = dict(metadata(), **{field: SECRET})
    fixed(post(http, values), 422, "DOCUMENT_REGISTRATION_INVALID")
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("body", [b"", b"{", b"[]", b"null", b"true", b"42", b'"text"', b"\xff", b"[" * 3000 + b"]" * 3000,
    b'{"document_type":"sop","title":"one","title":"two","source_type":"manual","source_reference":"opaque"}',
    b'{"document_type":"sop","title":NaN,"source_type":"manual","source_reference":"opaque"}',
    b'{"document_type":"sop","title":"ok","source_type":"manual","source_reference":{"a":1,"a":2}}',
])
def test_invalid_json_utf8_or_duplicate_keys_never_dispatch(http, body):
    fixed(post(http, body=body), 422, "DOCUMENT_REGISTRATION_INVALID")
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("headers", [{}, {"content-type": ""}, {"content-type": "text/plain"},
    {"content-type": "application/problem+json"}, {"content-type": "multipart/form-data; boundary=x"},
    {"content-type": "application/json; charset=latin-1"}, {"content-type": "application/json; charset=utf8"},
    {"content-type": "application/json; charset=utf-8; charset=utf-8"},
    {"content-type": "application/json; extra=x"}, {"content-type": "application/json, application/json"},
    [("content-type", "application/json"), ("content-type", "application/json")]])
def test_registration_requires_unambiguous_utf8_json_media_type(http, headers):
    fixed(post(http, headers=headers), 415, "DOCUMENT_REGISTRATION_MEDIA_TYPE_UNSUPPORTED")
    assert http.registration.calls == http.establishment.calls == []


def test_canonical_domain_validation_occurs_without_allocating_identity(http, monkeypatch):
    identity_source = Mock(side_effect=AssertionError("Transport validation allocated an identity."))
    domain_validation = Mock(side_effect=DomainException(SECRET))
    monkeypatch.setattr(EntityId, "new", identity_source)
    monkeypatch.setattr(http.module, "DocumentSource", domain_validation)
    fixed(post(http), 422, "DOCUMENT_REGISTRATION_INVALID")
    domain_validation.assert_called_once()
    identity_source.assert_not_called()
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("body", [b"", b"\x00\xff\x01", b"\xef\xbb\xbf" + "  نص عربي\r\nSecond line  ".encode()])
def test_content_preserves_every_byte_and_closes_its_stream(http, body):
    response = put(http, body, headers={"content-type": "  Application/Octet-Stream  "})
    assert response.status_code == 200
    assert response.json() == {"document_id": IDENTITY, "media_type": "application/octet-stream",
                               "byte_length": len(body), "digest": sha256(body).hexdigest()}
    assert len(http.establishment.calls) == 1 and http.registration.calls == []
    request = http.establishment.calls[0]
    assert isinstance(request, DocumentContentEstablishmentRequest)
    assert request.document_id == EntityId.from_string(IDENTITY)
    assert request.media_type == "application/octet-stream"
    assert http.establishment.positions == [0] and http.establishment.bodies == [body]
    assert request.source.closed


@pytest.mark.parametrize("identity", [IDENTITY, IDENTITY.upper(), IDENTITY.replace("-", ""), "{" + IDENTITY + "}", "urn:uuid:" + IDENTITY])
def test_content_uses_canonical_entity_id_parsing_and_uuid_serialization(http, identity):
    response = put(http, identity=identity)
    assert response.status_code == 200 and response.json()["document_id"] == IDENTITY
    assert http.establishment.calls[0].document_id == EntityId.from_string(IDENTITY)


@pytest.mark.parametrize("identity", ["bad", "123", "not-a-uuid", "g" * 32, "1" * 33])
def test_invalid_document_identifier_is_fixed_422_before_dispatch(http, identity):
    fixed(put(http, identity=identity), 422, "DOCUMENT_ID_INVALID")
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("headers", [{}, {"content-type": ""}, {"content-type": " \t"},
    {"content-type": "text/plain; charset=utf-8"}, {"content-type": "plain"},
    {"content-type": "/plain"}, {"content-type": "text/"}, {"content-type": "te xt/plain"},
    {"content-type": "a/b/c"}, [("content-type", "text/plain"), ("content-type", "text/plain")]])
def test_content_media_type_follows_single_header_canonical_contract(http, headers):
    fixed(put(http, headers=headers), 422, "DOCUMENT_CONTENT_MEDIA_TYPE_INVALID")
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("operation", ["registration", "content"])
@pytest.mark.parametrize("encodings", [["gzip"], ["br"], [""], ["identity, gzip"],
                                       ["identity, identity"], ["identity", "identity"], ["gzip", "identity"]])
def test_nonidentity_duplicate_or_combined_encoding_is_rejected(http, operation, encodings):
    headers = [("content-type", "application/json" if operation == "registration" else "text/plain")]
    headers.extend(("content-encoding", value) for value in encodings)
    response = post(http, headers=headers) if operation == "registration" else put(http, headers=headers)
    fixed(response, 415, "DOCUMENT_TRANSPORT_ENCODING_UNSUPPORTED")
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("operation", ["registration", "content"])
def test_single_case_insensitive_identity_encoding_is_supported(http, operation):
    headers = {"content-type": "application/json" if operation == "registration" else "text/plain",
               "content-encoding": " IdEnTiTy "}
    response = post(http, headers=headers) if operation == "registration" else put(http, headers=headers)
    assert response.status_code == (201 if operation == "registration" else 200)


@pytest.mark.parametrize("operation", ["registration", "content"])
@pytest.mark.parametrize("encoding", [b"identity\x0b", b"identity\xa0", b"\ridentity"])
def test_identity_encoding_accepts_only_http_optional_whitespace(http, operation, encoding):
    body = json.dumps(metadata()).encode() if operation == "registration" else b"body"
    path = "/documents" if operation == "registration" else f"/documents/{IDENTITY}/content"
    headers = [(b"content-type", b"application/json" if operation == "registration" else b"text/plain"),
               (b"content-encoding", encoding)]
    status, payload, received = asgi(http, "POST" if operation == "registration" else "PUT", path, [body], headers)
    assert status == 415 and payload == {"detail": {"code": "DOCUMENT_TRANSPORT_ENCODING_UNSUPPORTED"}}
    assert received == [] and http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("operation,limit", [("registration", 65_536), ("content", 8_388_608)])
@pytest.mark.parametrize("extra", [0, 1])
@pytest.mark.parametrize("declared", [None, b"1", b"99999999"])
def test_actual_body_limits_ignore_missing_or_misleading_content_length(http, operation, limit, extra, declared):
    prefix = json.dumps(metadata()).encode() if operation == "registration" else b"raw\x00\xff"
    body = prefix + b" " * (limit + extra - len(prefix))
    path = "/documents" if operation == "registration" else f"/documents/{IDENTITY}/content"
    headers = [(b"content-type", b"application/json" if operation == "registration" else b"text/plain")]
    if declared is not None:
        headers.append((b"content-length", declared))
    status, payload, received = asgi(http, "POST" if operation == "registration" else "PUT",
                                    path, [body[:limit], body[limit:]], headers)
    calls = http.registration.calls if operation == "registration" else http.establishment.calls
    if extra:
        assert status == 413 and payload == {"detail": {"code": "DOCUMENT_REQUEST_TOO_LARGE"}}
        assert calls == []
    else:
        assert status == (201 if operation == "registration" else 200) and len(calls) == 1
    assert received == [0, 1]


@pytest.mark.parametrize("operation,limit", [("registration", 65_536), ("content", 8_388_608)])
def test_oversized_chunk_is_not_retained_and_later_chunks_are_not_read(http, monkeypatch, operation, limit):
    retained = []

    class MeasuredBuffer(bytearray):
        def extend(self, chunk):
            assert len(self) + len(chunk) <= limit
            retained.append(len(chunk))
            return super().extend(chunk)

    monkeypatch.setattr(http.module, "bytearray", MeasuredBuffer, raising=False)
    path = "/documents" if operation == "registration" else f"/documents/{IDENTITY}/content"
    headers = [(b"content-type", b"application/json" if operation == "registration" else b"text/plain")]
    status, payload, received = asgi(http, "POST" if operation == "registration" else "PUT",
                                    path, [b"x" * limit, b"!", b"must-not-read"], headers)
    assert status == 413 and payload == {"detail": {"code": "DOCUMENT_REQUEST_TOO_LARGE"}}
    assert received == [0, 1] and retained == [limit]
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("method,path", [("POST", "/documents"), ("PUT", "/documents/invalid/content")])
def test_closed_admission_precedes_body_headers_and_identifier_validation(http, method, path):
    http.runtime.disable_request_admission()
    before = http.runtime.state
    status, payload, received = asgi(http, method, path, [AssertionError("Body must not be read.")],
                                    [(b"content-type", b"bad"), (b"content-encoding", b"gzip")])
    assert status == 503 and payload == ADMISSION and received == []
    assert http.registration.calls == http.establishment.calls == []
    assert http.runtime.state is before and http.runtime.is_request_admission_enabled is False


def test_each_request_reads_the_same_live_runtime(http):
    http.runtime.disable_request_admission()
    assert post(http).json() == ADMISSION
    http.runtime.enable_request_admission()
    assert post(http).status_code == 201
    http.runtime.disable_request_admission()
    assert put(http).json() == ADMISSION
    http.runtime.enable_request_admission()
    assert put(http).status_code == 200
    assert len(http.registration.calls) == len(http.establishment.calls) == 1


@pytest.mark.parametrize("operation", ["registration", "content"])
def test_admission_closing_during_upload_blocks_dispatch(http, operation):
    body = json.dumps(metadata()).encode() if operation == "registration" else b"body"
    path = "/documents" if operation == "registration" else f"/documents/{IDENTITY}/content"
    headers = [(b"content-type", b"application/json" if operation == "registration" else b"text/plain")]

    def close_on_second_chunk(index):
        if index == 1:
            http.runtime.disable_request_admission()

    status, payload, received = asgi(http, "POST" if operation == "registration" else "PUT", path,
                                    [body[:2], body[2:]], headers, close_on_second_chunk)
    assert status == 503 and payload == ADMISSION and received == [0, 1]
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("operation", ["registration", "content"])
def test_queued_worker_rechecks_admission_outside_unknown_outcome_mapping(http, monkeypatch, operation):
    actual_dispatch, dispatched = http.module.run_in_threadpool, []

    async def close_before_worker(function, *args, **kwargs):
        dispatched.append(function)
        http.runtime.disable_request_admission()
        return await actual_dispatch(function, *args, **kwargs)

    monkeypatch.setattr(http.module, "run_in_threadpool", close_before_worker)
    response = post(http) if operation == "registration" else put(http)
    assert response.status_code == 503 and response.json() == ADMISSION
    assert len(dispatched) == 1 and http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("operation", ["registration", "content"])
def test_service_work_runs_off_the_asgi_event_loop_thread(http, operation):
    body = json.dumps(metadata()).encode() if operation == "registration" else b"body"
    path = "/documents" if operation == "registration" else f"/documents/{IDENTITY}/content"
    headers = [(b"content-type", b"application/json" if operation == "registration" else b"text/plain")]
    receive_threads = []
    status, _, _ = asgi(http, "POST" if operation == "registration" else "PUT", path,
                        [body], headers, lambda index: receive_threads.append(get_ident()))
    service = http.registration if operation == "registration" else http.establishment
    assert status == (201 if operation == "registration" else 200)
    assert receive_threads == [get_ident()] and len(service.threads) == 1
    assert service.threads[0] != receive_threads[0]


@pytest.mark.parametrize("operation", ["registration", "content"])
@pytest.mark.parametrize("failure", ["cancel", "disconnect"])
def test_cancel_or_disconnect_before_complete_body_makes_no_application_call(http, operation, failure):
    path = "/documents" if operation == "registration" else f"/documents/{IDENTITY}/content"
    headers = [(b"content-type", b"application/json" if operation == "registration" else b"text/plain")]
    last = asyncio.CancelledError() if failure == "cancel" else {"type": "http.disconnect"}
    expected = asyncio.CancelledError if failure == "cancel" else ClientDisconnect
    with pytest.raises(expected):
        asgi(http, "POST" if operation == "registration" else "PUT", path, [b"x", last], headers)
    assert http.registration.calls == http.establishment.calls == []


@pytest.mark.parametrize("error,status,code", [
    (EnterpriseDocumentAlreadyExistsError, 409, "DOCUMENT_IDENTITY_CONFLICT"),
    (DomainException, 500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN"),
    (ValueError, 500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN"),
    (TypeError, 500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN"),
    (RuntimeError, 500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN"),
    (OSError, 500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN"),
])
def test_registration_service_errors_have_fixed_scoped_translation(http, error, status, code):
    http.registration.effect = error(SECRET)
    fixed(post(http), status, code)
    assert len(http.registration.calls) == 1 and http.establishment.calls == []


@pytest.mark.parametrize("error,status,code", [
    (DocumentContentEstablishmentDocumentNotFoundError, 404, "DOCUMENT_NOT_FOUND"),
    (DocumentContentEstablishmentConflictError, 409, "DOCUMENT_CONTENT_CONFLICT"),
    (DocumentContentEstablishmentIntegrityError, 409, "DOCUMENT_CONTENT_INTEGRITY_FAILURE"),
    (DomainException, 500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN"),
    (ValueError, 500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN"),
    (TypeError, 500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN"),
    (RuntimeError, 500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN"),
    (OSError, 500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN"),
])
def test_content_service_errors_have_fixed_scoped_translation_and_close_stream(http, error, status, code):
    http.establishment.effect = error(SECRET)
    fixed(put(http), status, code)
    assert len(http.establishment.calls) == 1 and http.registration.calls == []
    assert http.establishment.calls[0].source.closed


@pytest.mark.parametrize("defect", ["none", "duck", "id-type", "id-value", "type-object", "type-value",
    "title", "source-object", "source-type", "source-reference"])
def test_malformed_or_mismatching_registration_results_are_unknown(http, defect):
    def malformed(request):
        document = document_for(request)
        if defect == "none":
            return None
        if defect == "duck":
            return SimpleNamespace(**{field: getattr(document, field) for field in ("id", "document_type", "title", "source")})
        if defect == "id-type":
            object.__setattr__(document, "id", IDENTITY)
        elif defect == "id-value":
            object.__setattr__(document, "id", EntityId(value=IDENTITY))
        elif defect == "type-object":
            object.__setattr__(document, "document_type", "custom sop")
        elif defect == "type-value":
            object.__setattr__(document.document_type, "value", "WRONG")
        elif defect == "title":
            object.__setattr__(document, "title", "Different " + SECRET)
        elif defect == "source-object":
            object.__setattr__(document, "source", object())
        elif defect == "source-type":
            object.__setattr__(document.source, "source_type", "manual import")
        elif defect == "source-reference":
            object.__setattr__(document.source, "source_reference", SECRET)
        return document

    http.registration.effect = malformed
    fixed(post(http), 500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN")
    assert len(http.registration.calls) == 1 and http.establishment.calls == []


@pytest.mark.parametrize("defect", ["none", "duck", "id-type", "id-value", "id-mismatch", "media-object",
    "media-value", "media-normalization", "length-bool", "length-negative", "length-float", "length-mismatch", "length-subclass",
    "digest-object", "digest-value", "digest-normalization"])
def test_invalid_content_results_are_unknown_and_close_the_stream(http, defect):
    def malformed(request, body):
        descriptor = descriptor_for(request, body)
        if defect == "none":
            return None
        if defect == "duck":
            return SimpleNamespace(**{field: getattr(descriptor, field) for field in ("document_id", "media_type", "byte_length", "digest")})
        if defect == "id-type":
            object.__setattr__(descriptor, "document_id", IDENTITY)
        elif defect == "id-value":
            object.__setattr__(descriptor, "document_id", EntityId(value=IDENTITY))
        elif defect == "id-mismatch":
            object.__setattr__(descriptor, "document_id", EntityId.new())
        elif defect == "media-object":
            object.__setattr__(descriptor, "media_type", "text/plain")
        elif defect == "media-value":
            object.__setattr__(descriptor.media_type, "value", "text/html")
        elif defect == "media-normalization":
            object.__setattr__(descriptor.media_type, "value", " TEXT/PLAIN ")
        elif defect.startswith("length-"):
            class LyingLength(int):
                def __ne__(self, other):
                    return False

                def __lt__(self, other):
                    return False

                def __int__(self):
                    return len(body)

            object.__setattr__(descriptor, "byte_length", {
                "length-bool": True, "length-negative": -1, "length-float": 7.0, "length-mismatch": len(body) + 1,
                "length-subclass": LyingLength(len(body) + 1),
            }[defect])
        elif defect == "digest-object":
            object.__setattr__(descriptor, "digest", sha256(body).hexdigest())
        elif defect == "digest-value":
            object.__setattr__(descriptor.digest, "value", "0" * 64)
        elif defect == "digest-normalization":
            object.__setattr__(descriptor.digest, "value", sha256(body).hexdigest().upper())
        return descriptor

    http.establishment.effect = malformed
    fixed(put(http), 500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN")
    assert len(http.establishment.calls) == 1 and http.establishment.calls[0].source.closed


def test_canonical_integer_subclass_uses_its_actual_length_value(http):
    class ActualLength(int):
        def __int__(self):
            raise AssertionError("Custom conversion must not control response integrity.")

        def __ne__(self, other):
            raise AssertionError("Custom comparison must not control response integrity.")

    def result(request, body):
        descriptor = descriptor_for(request, body)
        object.__setattr__(descriptor, "byte_length", ActualLength(len(body)))
        return descriptor

    http.establishment.effect = result
    response = put(http, b"binary")
    assert response.status_code == 200 and response.json()["byte_length"] == 6
    assert http.establishment.calls[0].source.closed


def test_known_registration_error_from_result_access_is_unknown(http):
    class BrokenResult(EnterpriseDocument):
        def __getattribute__(self, name):
            if name == "id":
                raise EnterpriseDocumentAlreadyExistsError(SECRET)
            return super().__getattribute__(name)

    http.registration.effect = lambda request: object.__new__(BrokenResult)
    fixed(post(http), 500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN")
    assert len(http.registration.calls) == 1


@pytest.mark.parametrize("error", [DocumentContentEstablishmentDocumentNotFoundError,
    DocumentContentEstablishmentConflictError, DocumentContentEstablishmentIntegrityError, DomainException])
def test_known_content_error_from_result_access_is_unknown(http, error):
    class BrokenResult(DocumentContentDescriptor):
        def __getattribute__(self, name):
            if name == "document_id":
                raise error(SECRET)
            return super().__getattribute__(name)

    http.establishment.effect = lambda request, body: object.__new__(BrokenResult)
    fixed(put(http), 500, "DOCUMENT_CONTENT_OUTCOME_UNKNOWN")
    assert len(http.establishment.calls) == 1 and http.establishment.calls[0].source.closed


@pytest.mark.parametrize("operation", ["registration", "content"])
def test_serialization_failure_stays_inside_unknown_result_boundary(http, monkeypatch, operation):
    monkeypatch.setattr(http.module, "Response", Mock(side_effect=DocumentContentEstablishmentConflictError(SECRET)))
    fixed(post(http) if operation == "registration" else put(http), 500,
          "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN" if operation == "registration" else "DOCUMENT_CONTENT_OUTCOME_UNKNOWN")
    if operation == "content":
        assert len(http.establishment.calls) == 1 and http.establishment.calls[0].source.closed
    else:
        assert len(http.registration.calls) == 1


def test_unserializable_returned_text_is_unknown_after_single_registration(http):
    values = metadata()
    values["title"] = "\ud800"
    fixed(post(http, values), 500, "DOCUMENT_REGISTRATION_OUTCOME_UNKNOWN")
    assert len(http.registration.calls) == 1


@pytest.mark.parametrize("operation", ["registration", "content"])
def test_baseexception_is_not_swallowed_and_content_stream_still_closes(http, operation):
    class StopOperation(BaseException):
        pass

    error = StopOperation()
    if operation == "registration":
        http.registration.effect = error
        request, expected = http.module._registration_input(json.dumps(metadata()).encode())
        with pytest.raises(StopOperation) as captured:
            http.module._register(http.registration, http.runtime, request, expected)
        assert len(http.registration.calls) == 1
    else:
        http.establishment.effect = error
        with pytest.raises(StopOperation) as captured:
            http.module._establish(http.establishment, http.runtime, EntityId.from_string(IDENTITY),
                                   DocumentContentMediaType(value="text/plain"), b"body")
        assert len(http.establishment.calls) == 1 and http.establishment.calls[0].source.closed
    assert captured.value is error


def _rfc084_host_inputs():
    from app.core.composition import CompositionRoot
    from app.services.document_content_establishment_application_service import (
        DocumentContentEstablishmentApplicationService,
    )
    from app.services.enterprise_document_registration_application_service import (
        EnterpriseDocumentRegistrationApplicationService,
    )

    return (
        CompositionRoot.build(),
        object.__new__(EnterpriseDocumentRegistrationApplicationService),
        object.__new__(DocumentContentEstablishmentApplicationService),
    )


@pytest.mark.parametrize("case", [
    "registration-only", "content-only", "wrong-registration", "wrong-content",
    "false-pair", "false-registration-only", "false-content-only", "swapped",
    "same-service-twice", "wrong-platform",
])
def test_rfc084_host_rejects_invalid_pairs_before_any_assembly(monkeypatch, case):
    from importlib import import_module
    from unittest.mock import Mock

    host = import_module("app.api.document_knowledge_ingestion_host")
    platform, registration, content = _rfc084_host_inputs()
    pairs = {
        "registration-only": (registration, None),
        "content-only": (None, content),
        "wrong-registration": (object(), content),
        "wrong-content": (registration, object()),
        "false-pair": (False, False),
        "false-registration-only": (False, None),
        "false-content-only": (None, False),
        "swapped": (content, registration),
        "same-service-twice": (registration, registration),
        "wrong-platform": (registration, content),
    }
    supplied_registration, supplied_content = pairs[case]
    spies = []
    for name in (
        "FastAPI", "create_operational_transition_router", "create_document_knowledge_ingestion_router",
        "create_document_preparation_router", "RequestAdmissionMiddleware",
    ):
        spy = Mock(side_effect=AssertionError("Invalid input reached host assembly"))
        monkeypatch.setattr(host, name, spy)
        spies.append(spy)
    with pytest.raises(TypeError):
        host.create_app(
            platform=object() if case == "wrong-platform" else platform,
            document_registration_service=supplied_registration,
            document_content_establishment_service=supplied_content,
        )
    for spy in spies:
        spy.assert_not_called()
    assert platform.runtime.is_request_admission_enabled is False


@pytest.mark.parametrize("explicit_none", [False, True])
def test_rfc084_host_omitted_pair_retains_original_routes(monkeypatch, explicit_none):
    from importlib import import_module
    from unittest.mock import Mock

    host = import_module("app.api.document_knowledge_ingestion_host")
    platform, _, _ = _rfc084_host_inputs()
    preparation = Mock(side_effect=AssertionError("An omitted pair must not mount preparation"))
    monkeypatch.setattr(host, "create_document_preparation_router", preparation)
    optional = {} if not explicit_none else {
        "document_registration_service": None, "document_content_establishment_service": None,
    }
    app = host.create_app(platform=platform, **optional)
    assert set(app.openapi()["paths"]) == {
        "/", "/health", "/operational-transition", "/documents/{document_id}/knowledge",
    }
    preparation.assert_not_called()
    assert app.user_middleware[0].kwargs["runtime"] is platform.runtime
    assert platform.runtime.is_request_admission_enabled is False


def test_rfc084_host_falsey_canonical_pair_is_forwarded_once_without_work(monkeypatch):
    from dataclasses import fields
    from importlib import import_module
    from unittest.mock import Mock

    from app.core.composition import CompositionRoot, PlatformComposition
    from app.services.document_content_establishment_application_service import (
        DocumentContentEstablishmentApplicationService,
    )
    from app.services.enterprise_document_registration_application_service import (
        EnterpriseDocumentRegistrationApplicationService,
    )

    class FalseyRegistration(EnterpriseDocumentRegistrationApplicationService):
        def __bool__(self):
            raise AssertionError("Registration truthiness must not be read")

    class FalseyContent(DocumentContentEstablishmentApplicationService):
        def __bool__(self):
            raise AssertionError("Content service truthiness must not be read")

    class FalseyPlatform(PlatformComposition):
        def __bool__(self):
            raise AssertionError("Platform truthiness must not be read")

    host = import_module("app.api.document_knowledge_ingestion_host")
    built = CompositionRoot.build()
    platform = FalseyPlatform(**{
        item.name: getattr(built, item.name) for item in fields(PlatformComposition)
    })
    registration = object.__new__(FalseyRegistration)
    content = object.__new__(FalseyContent)
    initial_state = platform.runtime.state
    forbidden = []
    for owner, name in (
        (registration, "register"), (content, "establish"),
        (platform.bootstrap, "startup"), (platform.bootstrap, "shutdown"),
        (platform.runtime, "enable_request_admission"), (platform.runtime, "disable_request_admission"),
        (platform.application_facade, "ingest_document_knowledge"),
        (platform.operational_transition_application_service, "request_operational"),
    ):
        spy = Mock(side_effect=AssertionError("Assembly must not perform application or lifecycle work"))
        monkeypatch.setattr(owner, name, spy)
        forbidden.append(spy)
    preparation = Mock(wraps=host.create_document_preparation_router)
    ingestion = Mock(wraps=host.create_document_knowledge_ingestion_router)
    operational = Mock(wraps=host.create_operational_transition_router)
    monkeypatch.setattr(host, "create_document_preparation_router", preparation)
    monkeypatch.setattr(host, "create_document_knowledge_ingestion_router", ingestion)
    monkeypatch.setattr(host, "create_operational_transition_router", operational)
    monkeypatch.setattr(CompositionRoot, "build", Mock(side_effect=AssertionError("Unexpected new graph")))
    app = host.create_app(
        platform=platform,
        document_registration_service=registration,
        document_content_establishment_service=content,
    )
    preparation.assert_called_once()
    assert preparation.call_args.args == ()
    forwarded = preparation.call_args.kwargs
    assert set(forwarded) == {"document_registration_service", "document_content_establishment_service", "runtime"}
    assert forwarded["document_registration_service"] is registration
    assert forwarded["document_content_establishment_service"] is content
    assert forwarded["runtime"] is platform.runtime
    ingestion.assert_called_once_with(facade=platform.application_facade, runtime=platform.runtime)
    operational.assert_called_once_with(platform.operational_transition_application_service)
    assert app.user_middleware[0].kwargs["runtime"] is platform.runtime
    assert set(app.openapi()["paths"]) == {
        "/", "/health", "/operational-transition", "/documents/{document_id}/knowledge",
        "/documents", "/documents/{document_id}/content",
    }
    assert set(app.openapi()["paths"]["/documents"]) == {"post"}
    assert set(app.openapi()["paths"]["/documents/{document_id}/content"]) == {"put"}
    assert platform.runtime.state is initial_state
    assert platform.runtime.is_request_admission_enabled is False
    for spy in forbidden:
        spy.assert_not_called()
    CompositionRoot.build.assert_not_called()
