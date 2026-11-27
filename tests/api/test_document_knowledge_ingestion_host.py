"""RFC-083 supplied-platform hosting, live admission and lifecycle ownership."""

from __future__ import annotations

import asyncio
from dataclasses import fields, replace
from importlib import import_module, util
from inspect import Parameter, signature
from types import SimpleNamespace
from typing import get_type_hints
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.api.request_admission import (
    DEFAULT_ADMISSION_EXEMPT_PATHS,
    RequestAdmissionMiddleware,
)
from app.config import settings
from app.core.composition import CompositionRoot, PlatformComposition
from app.core.runtime_state import RuntimeState
from app.domain.base import EntityId
from app.schemas.platform import PlatformStatus
from app.services.document_knowledge_ingestion_application_service import (
    DocumentKnowledgeIngestionResult,
)
from app.services.document_content_establishment_application_service import (
    DocumentContentEstablishmentApplicationService,
)
from app.services.enterprise_document_registration_application_service import (
    EnterpriseDocumentRegistrationApplicationService,
)


MODULE = "app.api.document_knowledge_ingestion_host"
ADMISSION_DETAIL = "PlantMind is not accepting operational requests."


def test_host_factory_is_available():
    """TDD red: the missing module is imported only when this test executes."""
    host = import_module(MODULE)
    assert callable(host.create_app)


@pytest.fixture
def host():
    return import_module(MODULE)


@pytest.fixture
def platform():
    return CompositionRoot.build()


def url(identity):
    return f"/documents/{identity}/knowledge"


def payload():
    return {"kind": "procedure", "title": "Host lifecycle evidence"}


def operational_payload():
    return {"observations": [{
        "source": "pi-system",
        "observation_type": "process",
        "value": "stable",
        "observed_at": "2026-08-09T09:00:00Z",
    }]}


def result_for(identity):
    record = EntityId.new()
    return DocumentKnowledgeIngestionResult(
        knowledge_record=SimpleNamespace(id=record),
        lineage=SimpleNamespace(document_id=identity, knowledge_record_id=record),
    )


def forbid(*args, **kwargs):
    raise AssertionError("Unexpected work at the host assembly boundary")


def test_factory_requires_only_the_keyword_only_canonical_platform(host, platform):
    parameters = signature(host.create_app).parameters
    assert tuple(parameters) == (
        "platform", "document_registration_service", "document_content_establishment_service",
    )
    assert all(item.kind is Parameter.KEYWORD_ONLY for item in parameters.values())
    assert parameters["platform"].default is Parameter.empty
    assert parameters["document_registration_service"].default is None
    assert parameters["document_content_establishment_service"].default is None
    assert get_type_hints(host.create_app) == {
        "platform": PlatformComposition,
        "document_registration_service": EnterpriseDocumentRegistrationApplicationService | None,
        "document_content_establishment_service": DocumentContentEstablishmentApplicationService | None,
        "return": FastAPI,
    }
    with pytest.raises(TypeError):
        host.create_app()
    with pytest.raises(TypeError):
        host.create_app(platform)


class DuckPlatform:
    def __bool__(self):
        raise AssertionError("The type guard must not evaluate truthiness")

    def __getattr__(self, name):
        raise AssertionError("The type guard must not inspect components")


@pytest.mark.parametrize(
    "value", [None, False, 0, "platform", object(), DuckPlatform()],
    ids=["none", "false", "zero", "text", "object", "duck"],
)
def test_wrong_type_is_rejected_before_any_assembly(host, monkeypatch, value):
    app_constructor = Mock(side_effect=forbid)
    operation_router = Mock(side_effect=forbid)
    ingestion_router = Mock(side_effect=forbid)
    middleware = Mock(side_effect=forbid)
    monkeypatch.setattr(host, "FastAPI", app_constructor)
    monkeypatch.setattr(host, "create_operational_transition_router", operation_router)
    monkeypatch.setattr(host, "create_document_knowledge_ingestion_router", ingestion_router)
    monkeypatch.setattr(host, "RequestAdmissionMiddleware", middleware)
    with pytest.raises(TypeError):
        host.create_app(platform=value)
    for collaborator in (app_constructor, operation_router, ingestion_router, middleware):
        collaborator.assert_not_called()


class FalseyPlatform(PlatformComposition):
    truth_checks = 0

    def __bool__(self):
        object.__setattr__(self, "truth_checks", self.truth_checks + 1)
        return False


def test_falsey_canonical_subclass_is_used_without_truth_testing(host, platform):
    supplied = FalseyPlatform(**{
        field.name: getattr(platform, field.name) for field in fields(PlatformComposition)
    })
    app = host.create_app(platform=supplied)
    assert isinstance(app, FastAPI)
    assert supplied.truth_checks == 0
    assert app.user_middleware[0].kwargs["runtime"] is supplied.runtime
    assert supplied.runtime.state is RuntimeState.CREATED
    assert supplied.runtime.is_request_admission_enabled is False


def test_assembly_reuses_exact_components_without_lifecycle_or_use_case_calls(
    host, platform, monkeypatch,
):
    operation_router = Mock(wraps=host.create_operational_transition_router)
    ingestion_router = Mock(wraps=host.create_document_knowledge_ingestion_router)
    monkeypatch.setattr(host, "create_operational_transition_router", operation_router)
    monkeypatch.setattr(host, "create_document_knowledge_ingestion_router", ingestion_router)
    spies = []
    for component, name in (
        (platform.bootstrap, "startup"), (platform.bootstrap, "shutdown"),
        (platform.health, "get_status"),
        (platform.application_facade, "ingest_document_knowledge"),
        (platform.operational_transition_application_service, "request_operational"),
    ):
        spy = Mock(side_effect=forbid)
        monkeypatch.setattr(component, name, spy)
        spies.append(spy)
    monkeypatch.setattr(CompositionRoot, "build", staticmethod(forbid))

    first = host.create_app(platform=platform)
    second = host.create_app(platform=platform)

    assert first is not second
    assert first.router is not second.router
    assert operation_router.call_count == ingestion_router.call_count == 2
    for call in operation_router.call_args_list:
        assert call.args == (platform.operational_transition_application_service,)
        assert call.kwargs == {}
    for call in ingestion_router.call_args_list:
        assert call.args == ()
        assert set(call.kwargs) == {"facade", "runtime"}
        assert call.kwargs["facade"] is platform.application_facade
        assert call.kwargs["runtime"] is platform.runtime
    for app in (first, second):
        assert len(app.user_middleware) == 1
        entry = app.user_middleware[0]
        assert entry.cls is RequestAdmissionMiddleware
        assert entry.kwargs == {"runtime": platform.runtime}
    assert DEFAULT_ADMISSION_EXEMPT_PATHS == ("/", "/health")
    assert platform.runtime.state is RuntimeState.CREATED
    assert platform.runtime.is_request_admission_enabled is False
    for spy in spies:
        spy.assert_not_called()


def test_exposed_business_routes_and_status_schema_match_existing_contract(host, platform):
    app = host.create_app(platform=platform)
    schema = app.openapi()
    assert set(schema["paths"]) == {
        "/", "/health", "/operational-transition", "/documents/{document_id}/knowledge",
    }
    for path in ("/", "/health"):
        assert set(schema["paths"][path]) == {"get"}
    for path in ("/operational-transition", "/documents/{document_id}/knowledge"):
        assert set(schema["paths"][path]) == {"post"}
    root = next(route for route in app.routes if getattr(route, "path", None) == "/")
    assert root.response_model is PlatformStatus
    assert app.title == settings.APP_NAME
    assert app.version == settings.VERSION
    assert app.description == "Enterprise Operational Intelligence Platform"


def test_status_reads_metadata_and_live_supplied_runtime_and_health(host, platform, monkeypatch):
    configured = SimpleNamespace(
        APP_NAME="Host settings name", VERSION="8.3.0", DEPLOYMENT_MODE="Explicit host",
    )
    runtime = SimpleNamespace(
        state=SimpleNamespace(value="created"), environment="First environment",
        is_request_admission_enabled=False,
    )
    health = SimpleNamespace(get_status=Mock(return_value={"live": "first"}))
    supplied = replace(platform, runtime=runtime, health=health)
    monkeypatch.setattr(host, "settings", configured)
    app = host.create_app(platform=supplied)
    assert app.title == configured.APP_NAME and app.version == configured.VERSION
    client = TestClient(app)
    try:
        before = client.get("/")
        assert before.status_code == 200
        assert before.json() == {
            "platform": {
                "name": configured.APP_NAME, "edition": "Enterprise",
                "deployment": configured.DEPLOYMENT_MODE, "version": configured.VERSION,
            },
            "runtime": {"status": "created", "environment": "First environment"},
        }
        assert client.get("/health").json() == {"live": "first"}
        runtime.state = SimpleNamespace(value="ready")
        runtime.environment = "Second environment"
        health.get_status.return_value = {"live": "second"}
        assert client.get("/").json()["runtime"] == {
            "status": "ready", "environment": "Second environment",
        }
        assert client.get("/health").json() == {"live": "second"}
    finally:
        client.close()
    assert health.get_status.call_count == 2
    assert runtime.is_request_admission_enabled is False


@pytest.mark.parametrize("path", [
    "/documents/not-a-uuid/knowledge", "/operational-transition",
    "/analysis/health", "/health/", "/health/nested",
])
def test_closed_admission_precedes_validation_and_has_only_exact_exemptions(
    host, platform, monkeypatch, path,
):
    ingest = Mock(side_effect=forbid)
    operation = Mock(side_effect=forbid)
    startup = Mock(side_effect=forbid)
    shutdown = Mock(side_effect=forbid)
    monkeypatch.setattr(platform.application_facade, "ingest_document_knowledge", ingest)
    monkeypatch.setattr(platform.operational_transition_application_service, "request_operational", operation)
    monkeypatch.setattr(platform.bootstrap, "startup", startup)
    monkeypatch.setattr(platform.bootstrap, "shutdown", shutdown)
    client = TestClient(host.create_app(platform=platform))
    try:
        response = client.post(path, content="{broken", headers={"content-type": "application/json"})
        assert response.status_code == 503
        assert response.json() == {"detail": ADMISSION_DETAIL}
        assert client.get("/").status_code == 200
        assert client.get("/health").status_code == 200
    finally:
        client.close()
    assert platform.runtime.state is RuntimeState.CREATED
    assert platform.runtime.is_request_admission_enabled is False
    for spy in (ingest, operation, startup, shutdown):
        spy.assert_not_called()


@pytest.mark.parametrize("failure", ["none", "startup", "body", "shutdown", "both"])
def test_lifespan_delegates_exactly_once_and_preserves_failure_semantics(host, platform, failure):
    events = []
    startup_error = LookupError("startup failed")
    body_error = ValueError("body failed")
    shutdown_error = OSError("shutdown failed")

    def startup():
        events.append("startup")
        if failure == "startup":
            raise startup_error

    def shutdown():
        events.append("shutdown")
        if failure in ("shutdown", "both"):
            raise shutdown_error

    bootstrap = SimpleNamespace(startup=Mock(side_effect=startup), shutdown=Mock(side_effect=shutdown))
    app = host.create_app(platform=replace(platform, bootstrap=bootstrap))
    assert events == []

    async def exercise():
        async with app.router.lifespan_context(app):
            events.append("body")
            if failure in ("body", "both"):
                raise body_error

    expected = {
        "startup": startup_error, "body": body_error,
        "shutdown": shutdown_error, "both": shutdown_error,
    }.get(failure)
    if expected is None:
        asyncio.run(exercise())
    else:
        with pytest.raises(type(expected)) as caught:
            asyncio.run(exercise())
        assert caught.value is expected
        if failure == "both":
            assert caught.value.__context__ is body_error
    assert events == (["startup"] if failure == "startup" else ["startup", "body", "shutdown"])
    bootstrap.startup.assert_called_once_with()
    assert bootstrap.shutdown.call_count == (0 if failure == "startup" else 1)
    assert platform.runtime.state is RuntimeState.CREATED
    assert platform.runtime.is_request_admission_enabled is False


def test_real_bootstrap_owns_admission_without_implicit_business_calls(host, platform, monkeypatch):
    startup = Mock(wraps=platform.bootstrap.startup)
    shutdown = Mock(wraps=platform.bootstrap.shutdown)
    ingest = Mock(side_effect=forbid)
    operation = Mock(side_effect=forbid)
    monkeypatch.setattr(platform.bootstrap, "startup", startup)
    monkeypatch.setattr(platform.bootstrap, "shutdown", shutdown)
    monkeypatch.setattr(platform.application_facade, "ingest_document_knowledge", ingest)
    monkeypatch.setattr(platform.operational_transition_application_service, "request_operational", operation)
    app = host.create_app(platform=platform)
    assert platform.runtime.is_request_admission_enabled is False
    with TestClient(app) as client:
        startup.assert_called_once_with()
        shutdown.assert_not_called()
        assert platform.runtime.state is RuntimeState.READY
        assert platform.runtime.is_request_admission_enabled is True
        assert client.get("/").json()["runtime"]["status"] == "ready"
        assert client.get("/health").json() == jsonable_encoder(platform.health.get_status())
    startup.assert_called_once_with()
    shutdown.assert_called_once_with()
    assert platform.runtime.is_request_admission_enabled is False
    ingest.assert_not_called()
    operation.assert_not_called()


def test_unconfigured_platform_is_accepted_and_live_admission_keeps_router_response(
    host, platform, monkeypatch,
):
    ingest = Mock(wraps=platform.application_facade.ingest_document_knowledge)
    monkeypatch.setattr(platform.application_facade, "ingest_document_knowledge", ingest)
    app = host.create_app(platform=platform)
    identity = EntityId.new()
    with TestClient(app) as client:
        initial = client.post(url(identity), json=payload())
        assert initial.status_code == 503
        assert initial.json() == {"detail": {"code": "INGESTION_NOT_CONFIGURED"}}
        platform.runtime.disable_request_admission()
        closed = client.post(url(identity), json=payload())
        invalid_closed = client.post("/documents/bad/knowledge", json={})
        assert closed.status_code == invalid_closed.status_code == 503
        assert closed.json() == invalid_closed.json() == {"detail": ADMISSION_DETAIL}
        assert ingest.call_count == 1
        platform.runtime.enable_request_admission()
        assert client.post("/documents/bad/knowledge", json={}).status_code == 422
        reopened = client.post(url(identity), json=payload())
        assert reopened.status_code == 503
        assert reopened.json() == {"detail": {"code": "INGESTION_NOT_CONFIGURED"}}
        assert ingest.call_count == 2
    assert platform.runtime.is_request_admission_enabled is False


def test_requests_reach_supplied_facade_and_operational_service_once(host, platform, monkeypatch):
    identity = EntityId.new()
    result = result_for(identity)
    ingest = Mock(return_value=result)
    operation = Mock(return_value=object())
    monkeypatch.setattr(platform.application_facade, "ingest_document_knowledge", ingest)
    monkeypatch.setattr(platform.operational_transition_application_service, "request_operational", operation)
    with TestClient(host.create_app(platform=platform)) as client:
        response = client.post(url(identity), json=payload())
        assert response.status_code == 201
        assert response.json() == {
            "document_id": str(identity), "knowledge_record_id": str(result.knowledge_record.id),
        }
        assert client.post("/operational-transition", json=operational_payload()).status_code == 204
    ingest.assert_called_once()
    command = ingest.call_args.args[0]
    assert command.document_id == identity
    assert command.kind == payload()["kind"] and command.title == payload()["title"]
    operation.assert_called_once()
    observations = operation.call_args.args[0]
    assert len(observations) == 1 and observations[0].source == "pi-system"
    assert platform.runtime.is_request_admission_enabled is False


def test_independent_platforms_have_independent_lifespans_and_admission(host):
    left, right = CompositionRoot.build(), CompositionRoot.build()
    left_app, right_app = host.create_app(platform=left), host.create_app(platform=right)
    assert left.runtime is not right.runtime and left.bootstrap is not right.bootstrap
    identity = EntityId.new()
    with TestClient(left_app) as left_client:
        assert left.runtime.is_request_admission_enabled is True
        assert right.runtime.is_request_admission_enabled is False
        with TestClient(right_app) as right_client:
            left.runtime.disable_request_admission()
            assert left_client.post(url(identity), json=payload()).json() == {"detail": ADMISSION_DETAIL}
            assert right.runtime.is_request_admission_enabled is True
            assert right_client.post(url(identity), json=payload()).json() == {
                "detail": {"code": "INGESTION_NOT_CONFIGURED"},
            }
        assert right.runtime.is_request_admission_enabled is False
        left.runtime.enable_request_admission()
        assert left_client.post(url(identity), json=payload()).json() == {
            "detail": {"code": "INGESTION_NOT_CONFIGURED"},
        }
    assert left.runtime.is_request_admission_enabled is False
    assert right.runtime.is_request_admission_enabled is False


def test_import_creates_no_host_or_platform_and_executes_no_use_case(host, monkeypatch):
    import fastapi
    from app.core.bootstrap_manager import BootstrapManager
    from app.services.application_facade import ApplicationFacade
    from app.services.operational_transition_application_service import (
        OperationalTransitionApplicationService,
    )

    monkeypatch.setattr(fastapi, "FastAPI", forbid)
    monkeypatch.setattr(CompositionRoot, "build", staticmethod(forbid))
    monkeypatch.setattr(BootstrapManager, "startup", forbid)
    monkeypatch.setattr(BootstrapManager, "shutdown", forbid)
    monkeypatch.setattr(ApplicationFacade, "ingest_document_knowledge", forbid)
    monkeypatch.setattr(OperationalTransitionApplicationService, "request_operational", forbid)
    spec = util.spec_from_file_location("rfc083_import_only_probe", host.__file__)
    assert spec is not None and spec.loader is not None
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert callable(module.create_app)
    assert "app" not in vars(module) and "platform" not in vars(module)
