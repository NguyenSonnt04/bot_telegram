import pytest
from pydantic import ValidationError

from api_service.config import API_V1_PREFIX, Settings


def test_settings_have_safe_development_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_env == "development"
    assert API_V1_PREFIX == "/api/v1"
    assert settings.log_level == "INFO"


def test_blank_example_values_keep_safe_defaults() -> None:
    settings = Settings(_env_file=".env.example")

    assert settings.app_env == "development"
    assert settings.log_level == "INFO"


def test_settings_reject_unknown_environment() -> None:
    with pytest.raises(ValidationError):
        Settings(app_env="staging", _env_file=None)
