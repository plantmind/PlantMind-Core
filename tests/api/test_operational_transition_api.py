from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.operational_transition import create_router
from app.domain.observation import Observation, ObservationType


class SpyOperationalTransitionApplicationService:
    def __init__(self) -> None:
        self.calls: list[tuple[Observation, ...]] = []
        self.result: Any = object()

    def request_operational(
        self,
        observations: tuple[Observation, ...],
    ) -> Any:
        self.calls.append(observations)
        return self.result


def create_test_app(
    service: SpyOperationalTransitionApplicationService,
) -> FastAPI:
    app = FastAPI()
    app.include_router(create_router(service))
    return app


def test_operational_transition_endpoint_accepts_post_request() -> None:
    service = SpyOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service))

    response = client.post(
        "/operational-transition",
        json={
            "observations": [
                {
                    "source": "pi-system",
                    "observation_type": "process",
                    "value": "stable",
                    "observed_at": "2026-08-09T09:00:00Z",
                }
            ]
        },
    )

    assert response.status_code == 204


def test_transport_observation_maps_to_domain_observation() -> None:
    service = SpyOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service))

    response = client.post(
        "/operational-transition",
        json={
            "observations": [
                {
                    "source": "pi-system",
                    "observation_type": "process",
                    "value": "stable",
                    "observed_at": "2026-08-09T09:00:00Z",
                }
            ]
        },
    )

    assert response.status_code == 204
    assert len(service.calls) == 1

    observation = service.calls[0][0]
    assert isinstance(observation, Observation)
    assert observation.source == "pi-system"
    assert observation.observation_type is ObservationType.PROCESS
    assert observation.value == "stable"
    assert observation.observed_at == datetime(
        2026,
        8,
        9,
        9,
        0,
        tzinfo=UTC,
    )


def test_successful_request_returns_no_content() -> None:
    service = SpyOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service))

    response = client.post(
        "/operational-transition",
        json={
            "observations": [
                {
                    "source": "pi-system",
                    "observation_type": "process",
                    "value": "stable",
                    "observed_at": "2026-08-09T09:00:00Z",
                }
            ]
        },
    )

    assert response.status_code == 204
    assert response.content == b""


def test_domain_validation_failure_returns_422_without_service_call() -> None:
    service = SpyOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service))
    response = client.post("/operational-transition", json={"observations": [{"source": "   ", "observation_type": "process", "value": "stable", "observed_at": "2026-08-09T09:00:00Z"}]})
    assert response.status_code == 422
    assert service.calls == []


def test_naive_timestamp_returns_422_without_service_call() -> None:
    service = SpyOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service))
    response = client.post("/operational-transition", json={"observations": [{"source": "pi-system", "observation_type": "process", "value": "stable", "observed_at": "2026-08-09T09:00:00"}]})
    assert response.status_code == 422
    assert service.calls == []


def test_invalid_observation_type_returns_422_without_service_call() -> None:
    service = SpyOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service))
    response = client.post("/operational-transition", json={"observations": [{"source": "pi-system", "observation_type": "unsupported", "value": "stable", "observed_at": "2026-08-09T09:00:00Z"}]})
    assert response.status_code == 422
    assert service.calls == []


def test_client_cannot_supply_workload_evidence() -> None:
    service = SpyOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service))
    response = client.post("/operational-transition", json={"observations": [{"source": "pi-system", "observation_type": "process", "value": "stable", "observed_at": "2026-08-09T09:00:00Z"}], "operational_workload_evidence": {"workload_id": "client-controlled"}})
    assert response.status_code == 422
    assert service.calls == []


def test_client_cannot_supply_transition_evidence() -> None:
    service = SpyOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service))
    response = client.post("/operational-transition", json={"observations": [{"source": "pi-system", "observation_type": "process", "value": "stable", "observed_at": "2026-08-09T09:00:00Z"}], "operational_transition_evidence": {"eligible": True}})
    assert response.status_code == 422
    assert service.calls == []


def test_observation_order_is_preserved() -> None:
    service = SpyOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service))
    response = client.post("/operational-transition", json={"observations": [{"source": "first-source", "observation_type": "process", "value": "first", "observed_at": "2026-08-09T09:00:00Z"}, {"source": "second-source", "observation_type": "alarm", "value": "second", "observed_at": "2026-08-09T09:01:00Z"}]})
    assert response.status_code == 204
    assert len(service.calls) == 1
    observations = service.calls[0]
    assert tuple(item.source for item in observations) == ("first-source", "second-source")
    assert tuple(item.value for item in observations) == ("first", "second")


class FailingOperationalTransitionApplicationService(
    SpyOperationalTransitionApplicationService
):
    def request_operational(
        self,
        observations: tuple[Observation, ...],
    ) -> Any:
        self.calls.append(observations)
        raise RuntimeError("transition rejected")


def test_application_service_failure_is_not_retried() -> None:
    service = FailingOperationalTransitionApplicationService()
    client = TestClient(create_test_app(service), raise_server_exceptions=False)
    response = client.post("/operational-transition", json={"observations": [{"source": "pi-system", "observation_type": "process", "value": "stable", "observed_at": "2026-08-09T09:00:00Z"}]})
    assert response.status_code == 500
    assert len(service.calls) == 1
