"""RFC-081 HTTP mapping, admission and error contracts."""
from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.api import document_knowledge_ingestion as api
from app.api.request_admission import RequestAdmissionMiddleware
from app.core.runtime import Runtime
from app.domain.base import DomainException, EntityId
from app.services.application_facade import ApplicationFacade
from app.services.document_knowledge_ingestion_application_service import DocumentKnowledgeIngestionResult
from app.services.parsed_document_knowledge_ingestion_application_service import ParsedDocumentKnowledgeIngestionRequest

SECRET = "private SQL /secret/path stored-text"


def result_for(identity, knowledge=None):
    knowledge = knowledge or EntityId.new()
    return DocumentKnowledgeIngestionResult(
        knowledge_record=SimpleNamespace(id=knowledge),
        lineage=SimpleNamespace(document_id=identity, knowledge_record_id=knowledge))


@contextmanager
def client_for(facade, runtime, middleware=True):
    app = FastAPI()
    if middleware:
        app.add_middleware(RequestAdmissionMiddleware, runtime=runtime)
    app.include_router(api.create_router(facade=facade, runtime=runtime))
    with TestClient(app) as client:
        yield client


@pytest.fixture
def rig():
    runtime, facade, identity = Runtime(), Mock(spec=ApplicationFacade), EntityId.new()
    runtime.enable_request_admission()
    facade.ingest_document_knowledge.return_value = result_for(identity)
    with client_for(facade, runtime) as client:
        yield client, facade, runtime, identity


def url(identity):
    return f"/documents/{identity}/knowledge"


def payload(**changes):
    return {"kind": "procedure", "title": "Synthetic", **changes}


@pytest.mark.parametrize("subject", [None, {"subject_type": " equipment ", "subject_id": str(uuid4())}])
def test_maps_exact_request_and_returns_only_canonical_ids(rig, subject):
    client, facade, runtime, identity = rig
    before = runtime.state, runtime.is_request_admission_enabled
    response = client.post(url(identity), json=payload(kind=" Procedure ", title=" عنوان ", subject=subject))
    assert response.status_code == 201 and "location" not in response.headers
    result = facade.ingest_document_knowledge.return_value
    assert response.json() == {"document_id": str(identity), "knowledge_record_id": str(result.knowledge_record.id)}
    facade.ingest_document_knowledge.assert_called_once()
    command = facade.ingest_document_knowledge.call_args.args[0]
    assert isinstance(command, ParsedDocumentKnowledgeIngestionRequest)
    assert command.document_id == identity and command.kind == " Procedure " and command.title == " عنوان "
    if subject is None:
        assert command.subject is None
    else:
        assert command.subject.subject_type == subject["subject_type"]
        assert str(command.subject.subject_id) == subject["subject_id"]
    assert before == (runtime.state, runtime.is_request_admission_enabled)


@pytest.mark.parametrize("field", ["kind", "title"])
@pytest.mark.parametrize("value", ["", " \t\n", "\u2003", 1, True, [], None])
def test_rejects_invalid_required_text_before_facade(rig, field, value):
    client, facade, _, identity = rig
    assert client.post(url(identity), json=payload(**{field: value})).status_code == 422
    facade.ingest_document_knowledge.assert_not_called()


@pytest.mark.parametrize("body", [
    {}, {"kind": "procedure"}, {"title": "x"}, [],
    payload(content="override"), payload(source_type="override"),
    payload(subject={}), payload(subject={"subject_type": "equipment", "subject_id": "invalid"}),
    payload(subject={"subject_type": " ", "subject_id": str(uuid4())}),
    payload(subject={"subject_type": 4, "subject_id": str(uuid4())}),
    payload(subject={"subject_type": "equipment", "subject_id": str(uuid4()), "extra": "x"}),
])
def test_invalid_body_or_extra_fields_make_no_call(rig, body):
    client, facade, _, identity = rig
    assert client.post(url(identity), json=body).status_code == 422
    facade.ingest_document_knowledge.assert_not_called()


def test_invalid_path_id_and_malformed_json_make_no_call(rig):
    client, facade, _, identity = rig
    assert client.post("/documents/not-a-uuid/knowledge", json=payload()).status_code == 422
    assert client.post(url(identity), content="{broken", headers={"Content-Type": "application/json"}).status_code == 422
    facade.ingest_document_knowledge.assert_not_called()


@pytest.mark.parametrize("middleware", [True, False])
def test_live_admission_blocks_calls_without_changing_runtime(middleware):
    runtime, facade, identity = Runtime(), Mock(spec=ApplicationFacade), EntityId.new()
    facade.ingest_document_knowledge.return_value = result_for(identity)
    initial = runtime.state
    with client_for(facade, runtime, middleware) as client:
        for enabled, expected in ((False, 503), (True, 201), (False, 503)):
            if enabled:
                runtime.enable_request_admission()
            else:
                runtime.disable_request_admission()
            response = client.post(url(identity), json=payload())
            assert response.status_code == expected
            if not enabled:
                assert response.json() == {"detail": "PlantMind is not accepting operational requests."}
            assert runtime.state is initial
            assert runtime.is_request_admission_enabled is enabled
    facade.ingest_document_knowledge.assert_called_once()


def test_closed_middleware_precedes_invalid_input(rig):
    client, facade, runtime, _ = rig
    runtime.disable_request_admission()
    assert client.post("/documents/bad/knowledge", json={}).status_code == 503
    facade.ingest_document_knowledge.assert_not_called()


@pytest.mark.parametrize("kind,status,code", [
    (api.ApplicationFacadeDocumentIngestionNotConfiguredError, 503, "INGESTION_NOT_CONFIGURED"),
    (api.DocumentContentAccessDocumentNotFoundError, 404, "DOCUMENT_NOT_FOUND"),
    (api.DocumentKnowledgeIngestionDocumentNotFoundError, 404, "DOCUMENT_NOT_FOUND"),
    (api.DocumentContentAccessContentNotFoundError, 409, "DOCUMENT_CONTENT_NOT_AVAILABLE"),
    (api.DocumentContentAccessIntegrityError, 409, "DOCUMENT_CONTENT_INTEGRITY_FAILURE"),
    (api.DocumentContentParserUnsupportedMediaTypeError, 422, "DOCUMENT_MEDIA_TYPE_UNSUPPORTED"),
    (api.DocumentContentParserInvalidContentError, 422, "DOCUMENT_CONTENT_INVALID"),
])
def test_named_errors_are_fixed_and_never_retried(rig, kind, status, code):
    client, facade, runtime, identity = rig
    before = runtime.state, runtime.is_request_admission_enabled
    facade.ingest_document_knowledge.side_effect = kind(SECRET)
    response = client.post(url(identity), json=payload())
    assert response.status_code == status and response.json() == {"detail": {"code": code}}
    assert SECRET not in response.text and "retry-after" not in response.headers
    facade.ingest_document_knowledge.assert_called_once()
    assert before == (runtime.state, runtime.is_request_admission_enabled)


@pytest.mark.parametrize("error", [
    ValueError(SECRET), TypeError(SECRET), DomainException(SECRET),
    RuntimeError(SECRET), OSError(SECRET), HTTPException(status_code=418, detail=SECRET),
    api.KnowledgeLineageTransactionPostCommitCleanupError(SECRET),
])
def test_unexpected_and_post_commit_failures_have_explicit_outcomes(rig, error):
    client, facade, _, identity = rig
    facade.ingest_document_knowledge.side_effect = error
    response = client.post(url(identity), json=payload())
    committed = isinstance(error, api.KnowledgeLineageTransactionPostCommitCleanupError)
    assert response.status_code == 500
    assert response.json() == {"detail": {
        "code": "INGESTION_COMMITTED_CLEANUP_FAILED" if committed else "INGESTION_FAILED",
        "persistence_outcome": "committed" if committed else "unknown",
        "retry_recommended": False}}
    assert SECRET not in response.text and "retry-after" not in response.headers
    facade.ingest_document_knowledge.assert_called_once()


@pytest.mark.parametrize("case", ["wrong_type", "missing", "raw_doc", "raw_record",
    "bad_doc_value", "bad_record_value", "bad_link_value", "wrong_doc", "wrong_link"])
def test_invalid_result_cannot_claim_success_or_rollback(rig, case):
    client, facade, _, identity = rig
    result = result_for(identity)
    if case == "wrong_type": result = object()
    elif case == "missing": result.knowledge_record.id = None
    elif case == "raw_doc": result.lineage.document_id = identity.value
    elif case == "raw_record": result.knowledge_record.id = uuid4()
    elif case == "bad_doc_value": result.lineage.document_id = EntityId(value="not-a-uuid")
    elif case == "bad_record_value": result.knowledge_record.id = EntityId(value="not-a-uuid")
    elif case == "bad_link_value": result.lineage.knowledge_record_id = EntityId(value="not-a-uuid")
    elif case == "wrong_doc": result.lineage.document_id = EntityId.new()
    elif case == "wrong_link": result.lineage.knowledge_record_id = EntityId.new()
    facade.ingest_document_knowledge.return_value = result
    response = client.post(url(identity), json=payload())
    assert response.status_code == 500
    assert response.json()["detail"] == {"code": "INGESTION_FAILED",
        "persistence_outcome": "unknown", "retry_recommended": False}
    facade.ingest_document_knowledge.assert_called_once()


def test_actual_facade_is_the_entry_and_analysis_is_not_called(monkeypatch):
    service, gateway, identity, runtime = Mock(), Mock(), EntityId.new(), Runtime()
    runtime.enable_request_admission()
    service.ingest.return_value = result_for(identity)
    facade = ApplicationFacade(gateway=gateway, parsed_document_knowledge_ingestion_service=service)
    analyze = Mock(side_effect=AssertionError("Unexpected analyze"))
    monkeypatch.setattr(facade, "analyze", analyze)
    with client_for(facade, runtime) as client:
        assert client.post(url(identity), json=payload()).status_code == 201
    service.ingest.assert_called_once()
    gateway.execute.assert_not_called()
    analyze.assert_not_called()


def test_real_unconfigured_facade_and_repeated_configured_calls(rig):
    client, facade, runtime, identity = rig
    with client_for(ApplicationFacade(), runtime) as disabled:
        response = disabled.post(url(identity), json=payload())
        assert response.status_code == 503
        assert response.json() == {"detail": {"code": "INGESTION_NOT_CONFIGURED"}}
    one, two = result_for(identity), result_for(identity)
    facade.ingest_document_knowledge.side_effect = [one, two]
    assert client.post(url(identity), json=payload()).json()["knowledge_record_id"] == str(one.knowledge_record.id)
    assert client.post(url(identity), json=payload()).json()["knowledge_record_id"] == str(two.knowledge_record.id)
    assert facade.ingest_document_knowledge.call_count == 2


def test_router_has_only_the_explicit_post_and_does_not_call_dependencies():
    facade, runtime = Mock(spec=ApplicationFacade), Mock(spec=Runtime)
    router = api.create_router(facade=facade, runtime=runtime)
    assert len(router.routes) == 1
    route = router.routes[0]
    assert route.path == "/documents/{document_id}/knowledge" and route.methods == {"POST"}
    assert not facade.mock_calls and not runtime.mock_calls
