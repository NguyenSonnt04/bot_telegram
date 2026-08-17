import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api_service.errors import ApplicationError


def test_application_error_uses_public_error_contract(app: FastAPI) -> None:
    @app.get("/api/v1/test-error")
    async def test_error() -> None:
        raise ApplicationError(
            code="test_error",
            message="Test failure.",
            status_code=409,
        )

    with TestClient(app) as client:
        response = client.get("/api/v1/test-error")

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "test_error",
            "message": "Test failure.",
        }
    }


def test_unexpected_error_does_not_expose_exception_details(
    app: FastAPI,
    caplog,
) -> None:
    @app.get("/api/v1/unexpected-error")
    async def unexpected_error() -> None:
        raise RuntimeError("sensitive implementation detail")

    with caplog.at_level(logging.ERROR):
        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get("/api/v1/unexpected-error")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "internal_server_error",
            "message": "Unexpected server error.",
        }
    }
    assert "sensitive implementation detail" not in response.text
    assert "sensitive implementation detail" not in caplog.text
    assert "method=GET path='/api/v1/unexpected-error'" in caplog.text


def test_missing_route_uses_public_error_contract(app: FastAPI) -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/missing")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "http_404",
            "message": "Not Found",
        }
    }
