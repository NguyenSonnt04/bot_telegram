from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_health_reports_process_liveness(app: FastAPI) -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_reports_initialized_application(app: FastAPI) -> None:
    with TestClient(app) as client:
        response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readiness_returns_service_unavailable_when_state_is_not_ready(
    app: FastAPI,
) -> None:
    with TestClient(app) as client:
        app.state.ready = False
        response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "error": {
            "code": "http_503",
            "message": "API service is not ready.",
        }
    }
