from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api_service import __version__
from api_service.api.router import router as api_router
from api_service.api.routes.health import router as health_router
from api_service.config import API_V1_PREFIX, APP_NAME, Settings, get_settings
from api_service.errors import register_error_handlers
from api_service.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.ready = True
    try:
        yield
    finally:
        app.state.ready = False


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings.log_level)

    app = FastAPI(
        title=APP_NAME,
        version=__version__,
        lifespan=lifespan,
    )
    app.state.ready = False
    app.state.settings = resolved_settings

    register_error_handlers(app)
    app.include_router(health_router)
    app.include_router(api_router, prefix=API_V1_PREFIX)
    return app


app = create_app()
