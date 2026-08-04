from fastapi.testclient import TestClient

from app.main import app


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
            "status": "Running",
            "environment": "Development",
        },
    }


def test_health_endpoint_returns_healthy_status() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }