from fastapi import FastAPI
from fastapi.testclient import TestClient

from api_service.config import Settings
from api_service.main import create_app


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


def test_readiness_requires_database_configuration() -> None:
    app = create_app(
        Settings(app_env="test", log_level="CRITICAL", _env_file=None),
    )

    with TestClient(app) as client:
        response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "error": {
            "code": "http_503",
            "message": "Database is not ready.",
        }
    }


def test_readiness_returns_service_unavailable_when_database_probe_fails(
    app: FastAPI,
    database,
) -> None:
    database.ready = False

    with TestClient(app) as client:
        response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {
        "error": {
            "code": "http_503",
            "message": "Database is not ready.",
        }
    }
