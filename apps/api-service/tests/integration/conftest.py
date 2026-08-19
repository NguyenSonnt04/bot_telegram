import pytest
from fastapi import FastAPI

from api_service.config import Settings
from api_service.main import create_app


class FakeDatabase:
    def __init__(self, *, ready: bool = True) -> None:
        self.ready = ready

    async def is_ready(self) -> bool:
        return self.ready

    async def dispose(self) -> None:
        pass


@pytest.fixture
def database() -> FakeDatabase:
    return FakeDatabase()


@pytest.fixture
def app(database: FakeDatabase) -> FastAPI:
    return create_app(
        Settings(app_env="test", log_level="CRITICAL", _env_file=None),
        database=database,
    )
