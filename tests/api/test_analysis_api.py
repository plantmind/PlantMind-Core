from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.analysis import router


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


def test_analysis_health_endpoint() -> None:
    client = TestClient(create_test_app())

    response = client.get("/analysis/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "PlantMind Analysis API",
    }