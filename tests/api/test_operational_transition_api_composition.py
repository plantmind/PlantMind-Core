from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.operational_transition import create_router
from app.api.request_admission import (
    DEFAULT_ADMISSION_EXEMPT_PATHS,
    RequestAdmissionMiddleware,
)
from app.core.runtime import Runtime
from app.domain.observation import Observation
from app.main import app, platform


class SpyOperationalTransitionApplicationService:
    def __init__(self) -> None:
        self.calls: list[tuple[Observation, ...]] = []

    def request_operational(
        self,
        observations: tuple[Observation, ...],
    ) -> Any:
        self.calls.append(observations)
        return object()


def valid_payload() -> dict[str, object]:
    return {
        "observations": [
            {
                "source": "pi-system",
                "observation_type": "process",
                "value": "stable",
                "observed_at": "2026-08-09T09:00:00Z",
            }
        ]
    }


def test_operational_transition_path_is_not_admission_exempt() -> None:
    assert "/operational-transition" not in DEFAULT_ADMISSION_EXEMPT_PATHS


def test_closed_admission_prevents_application_service_invocation() -> None:
    runtime = Runtime()
    service = SpyOperationalTransitionApplicationService()
    test_app = FastAPI()
    test_app.add_middleware(
        RequestAdmissionMiddleware,
        runtime=runtime,
    )
    test_app.include_router(create_router(service))
    client = TestClient(test_app)

    response = client.post(
        "/operational-transition",
        json=valid_payload(),
    )

    assert response.status_code == 503
    assert service.calls == []


def test_main_exposes_operational_transition_route() -> None:
    schema = app.openapi()

    assert "/operational-transition" in schema["paths"]
    assert "post" in schema["paths"]["/operational-transition"]


def test_main_route_uses_canonical_application_service(monkeypatch) -> None:
    calls: list[tuple[Observation, ...]] = []

    def request_operational(
        observations: tuple[Observation, ...],
    ) -> object:
        calls.append(observations)
        return object()

    monkeypatch.setattr(
        platform.operational_transition_application_service,
        "request_operational",
        request_operational,
    )

    with TestClient(app) as client:
        response = client.post(
            "/operational-transition",
            json=valid_payload(),
        )

    assert response.status_code == 204
    assert len(calls) == 1
    assert calls[0][0].source == "pi-system"


def test_bootstrap_does_not_invoke_operational_transition_use_case(
    monkeypatch,
) -> None:
    calls: list[tuple[Observation, ...]] = []

    def request_operational(
        observations: tuple[Observation, ...],
    ) -> object:
        calls.append(observations)
        return object()

    monkeypatch.setattr(
        platform.operational_transition_application_service,
        "request_operational",
        request_operational,
    )

    with TestClient(app):
        pass

    assert calls == []


def test_health_does_not_invoke_operational_transition_use_case(
    monkeypatch,
) -> None:
    calls: list[tuple[Observation, ...]] = []

    def request_operational(
        observations: tuple[Observation, ...],
    ) -> object:
        calls.append(observations)
        return object()

    monkeypatch.setattr(
        platform.operational_transition_application_service,
        "request_operational",
        request_operational,
    )

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert calls == []
