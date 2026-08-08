from fastapi.testclient import TestClient

from app.api.request_admission import RequestAdmissionMiddleware
from app.main import app, platform


def test_root_endpoint_returns_platform_status() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "platform": {
            "name": "PlantMind",
            "edition": "Enterprise",
            "deployment": "On-Premise",
            "version": "1.0.0",
        },
        "runtime": {
            "status": "ready",
            "environment": "Development",
        },
    }


def test_health_endpoint_returns_platform_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "platform_name": "PlantMind",
        "version": "1.0.0",
        "environment": "Development",
        "runtime_ready": True,
        "registered_services": 0,
        "services": [],
    }


def test_main_uses_composed_runtime_for_request_admission() -> None:
    middleware = next(
        item
        for item in app.user_middleware
        if item.cls is RequestAdmissionMiddleware
    )

    assert middleware.kwargs["runtime"] is platform.runtime
