import logging
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException

logger = logging.getLogger(__name__)


class ApplicationError(Exception):
    def __init__(self, *, code: str, message: str, status_code: int) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


def error_content(*, code: str, message: str) -> dict[str, dict[str, str]]:
    return {"error": {"code": code, "message": message}}


def register_error_handlers(app: FastAPI) -> None:
    @app.middleware("http")
    async def handle_unexpected_error(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        try:
            return await call_next(request)
        except Exception:
            logger.error(
                "Unhandled API error method=%s path=%r",
                request.method,
                request.url.path,
            )
            return JSONResponse(
                status_code=500,
                content=error_content(
                    code="internal_server_error",
                    message="Unexpected server error.",
                ),
            )

    @app.exception_handler(ApplicationError)
    async def handle_application_error(
        _request: Request,
        error: ApplicationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=error.status_code,
            content=error_content(code=error.code, message=error.message),
        )

    @app.exception_handler(HTTPException)
    async def handle_http_error(_request: Request, error: HTTPException) -> JSONResponse:
        message = error.detail if isinstance(error.detail, str) else "Request failed."
        return JSONResponse(
            status_code=error.status_code,
            content=error_content(code=f"http_{error.status_code}", message=message),
            headers=error.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _request: Request,
        _error: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_content(
                code="validation_error",
                message="Request validation failed.",
            ),
        )
