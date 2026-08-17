import pytest
from fastapi import FastAPI

from api_service.config import Settings
from api_service.main import create_app


@pytest.fixture
def app() -> FastAPI:
    return create_app(Settings(app_env="test", log_level="CRITICAL", _env_file=None))
