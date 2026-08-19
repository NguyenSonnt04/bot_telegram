import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncEngine

from api_service.infrastructure.database import DatabaseManager


def build_database(engine: AsyncEngine) -> DatabaseManager:
    database = object.__new__(DatabaseManager)
    database.engine = engine
    return database


def test_database_readiness_executes_probe() -> None:
    connection = AsyncMock()
    connection_context = MagicMock()
    connection_context.__aenter__ = AsyncMock(return_value=connection)
    connection_context.__aexit__ = AsyncMock(return_value=None)
    engine = MagicMock(spec=AsyncEngine)
    engine.connect.return_value = connection_context
    database = build_database(engine)

    ready = asyncio.run(database.is_ready())

    assert ready is True
    connection.execute.assert_awaited_once()
    statement = connection.execute.await_args.args[0]
    assert str(statement) == "SELECT 1"


def test_database_readiness_handles_connection_failure_without_logging_details(
    caplog,
) -> None:
    sensitive_marker = "database-password-marker-42f1"
    connection_context = MagicMock()
    connection_context.__aenter__ = AsyncMock(
        side_effect=RuntimeError(sensitive_marker),
    )
    connection_context.__aexit__ = AsyncMock(return_value=None)
    engine = MagicMock(spec=AsyncEngine)
    engine.connect.return_value = connection_context
    database = build_database(engine)

    with caplog.at_level(logging.WARNING):
        ready = asyncio.run(database.is_ready())

    assert ready is False
    assert "Database readiness check failed" in caplog.text
    assert sensitive_marker not in caplog.text


def test_database_dispose_releases_engine() -> None:
    engine = MagicMock(spec=AsyncEngine)
    engine.dispose = AsyncMock()
    database = build_database(engine)

    asyncio.run(database.dispose())

    engine.dispose.assert_awaited_once()
