import pytest
from pydantic import ValidationError

from api_service.config import API_V1_PREFIX, Settings


@pytest.fixture(autouse=True)
def isolate_settings_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)


def test_settings_have_safe_development_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_env == "development"
    assert API_V1_PREFIX == "/api/v1"
    assert settings.log_level == "INFO"
    assert settings.database_url is None


def test_blank_example_values_keep_safe_defaults() -> None:
    settings = Settings(_env_file=".env.example")

    assert settings.app_env == "development"
    assert settings.log_level == "INFO"


def test_settings_reject_unknown_environment() -> None:
    with pytest.raises(ValidationError):
        Settings(app_env="staging", _env_file=None)


def test_settings_load_database_url_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_url = "postgresql+asyncpg://application:placeholder@localhost/shop"
    monkeypatch.setenv("DATABASE_URL", database_url)

    settings = Settings(_env_file=None)

    assert settings.database_url is not None
    assert settings.database_url.get_secret_value() == database_url
    assert database_url not in repr(settings)
