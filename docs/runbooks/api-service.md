# Application Runbook: API Service Foundation

## Scope

Run and validate the local FastAPI foundation before database integration.

## Prerequisites

- Python 3.13.
- uv available on `PATH`.
- Dependencies synchronized from the repository root with `uv sync`.
- No database or external credential is required for the current foundation.

## Start

From the repository root:

```powershell
uv run uvicorn api_service.main:app --host 127.0.0.1 --port 8000
```

The command starts one local API process on host `127.0.0.1` and fixed port
`8000`. The process reads optional `APP_ENV` and `LOG_LEVEL` values from the
environment or root `.env`; their defaults are `development` and `INFO`.

## Readiness

After Uvicorn reports `Application startup complete`, verify:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/ready
```

The expected responses are `{"status":"ok"}` and `{"status":"ready"}`.
Readiness currently proves only that the FastAPI application initialized. It
does not probe PostgreSQL.

## Deterministic State

No persistent application state is created by the current foundation.

## Interface

- OpenAPI document: `http://127.0.0.1:8000/openapi.json`
- Business API prefix: `/api/v1`
- Liveness probe: `GET /health`
- Readiness probe: `GET /ready`

Public errors use an `error.code` and safe `error.message`. Unexpected exception
details are not returned to clients.

## Runtime Evidence

Uvicorn writes startup, shutdown, and HTTP access lines to the process console.
The current logs do not include a request correlation identifier or structured
JSON fields.

## Ownership And Cleanup

Stop the foreground Uvicorn process with `Ctrl+C`. Do not stop unrelated Python
or Uvicorn processes.

## Validation

From the repository root:

```powershell
uv lock --check
uv run pytest
uv run ruff format --check .
uv run ruff check .
```

For real-interface validation, start the API, retrieve `/health`, `/ready`, and
`/openapi.json`, then request an unknown path and confirm a `404` response using
the public error contract.

## Unknowns

- PostgreSQL readiness criteria will be defined with database foundation.
- Production worker count, bind address, process manager, and deployment
  lifecycle are not yet defined.
- Request correlation and structured logging are not yet implemented.
