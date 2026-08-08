from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.request_admission import (
    DEFAULT_ADMISSION_EXEMPT_PATHS,
    RequestAdmissionMiddleware,
)
from app.core.runtime import Runtime
from app.core.runtime_state import RuntimeState


def create_test_app(runtime: Runtime) -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        RequestAdmissionMiddleware,
        runtime=runtime,
        exempt_paths=DEFAULT_ADMISSION_EXEMPT_PATHS,
    )

    @app.get("/")
    def status() -> dict[str, str]:
        return {"status": "available"}

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"health": "available"}

    @app.get("/operational")
    def operational() -> dict[str, str]:
        return {"result": "accepted"}

    @app.get("/analysis/health")
    def nested_health() -> dict[str, str]:
        return {"health": "nested"}

    return app


def test_operational_request_is_allowed_when_admission_enabled() -> None:
    runtime = Runtime()
    runtime.enable_request_admission()
    client = TestClient(create_test_app(runtime))

    response = client.get("/operational")

    assert response.status_code == 200
    assert response.json() == {"result": "accepted"}


def test_operational_request_is_rejected_when_admission_disabled() -> None:
    runtime = Runtime()
    client = TestClient(create_test_app(runtime))

    response = client.get("/operational")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "PlantMind is not accepting operational requests."
    }


def test_admission_enforcement_does_not_modify_runtime() -> None:
    runtime = Runtime()
    initial_state = runtime.state
    client = TestClient(create_test_app(runtime))

    client.get("/operational")

    assert runtime.state is initial_state
    assert runtime.state is RuntimeState.CREATED
    assert runtime.is_request_admission_enabled is False


def test_status_endpoint_remains_available_when_admission_disabled() -> None:
    runtime = Runtime()
    client = TestClient(create_test_app(runtime))

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "available"}


def test_health_endpoint_remains_available_when_admission_disabled() -> None:
    runtime = Runtime()
    client = TestClient(create_test_app(runtime))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"health": "available"}


def test_observation_exemptions_do_not_use_health_path_wildcard() -> None:
    runtime = Runtime()
    client = TestClient(create_test_app(runtime))

    response = client.get("/analysis/health")

    assert response.status_code == 503


def test_enforcement_reads_live_state_from_same_runtime_instance() -> None:
    runtime = Runtime()
    client = TestClient(create_test_app(runtime))

    rejected = client.get("/operational")

    runtime.enable_request_admission()

    accepted = client.get("/operational")

    assert rejected.status_code == 503
    assert accepted.status_code == 200
