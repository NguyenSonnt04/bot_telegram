# Application Runbook: API Service

## Scope

Run, migrate, and validate the local FastAPI service with its PostgreSQL
connection.

## Prerequisites

- Python 3.13.
- uv available on `PATH`.
- Dependencies synchronized from the repository root with `uv sync`.
- PostgreSQL 17 is available.
- `DATABASE_URL` is configured in the root `.env` with the
  `postgresql+asyncpg://` driver. Do not place the real value in documentation
  or command history.

## Migrations

From the repository root, inspect and apply the committed migration chain:

```powershell
uv run alembic -c apps/api-service/alembic.ini current
uv run alembic -c apps/api-service/alembic.ini upgrade head
```

Create future revisions only after importing the affected SQLAlchemy metadata
into `apps/api-service/migrations/env.py`:

```powershell
uv run alembic -c apps/api-service/alembic.ini revision --autogenerate -m "<change>"
```

Review generated migrations before applying them. Do not edit a database schema
manually after persistent data exists.

## Start

From the repository root:

```powershell
uv run uvicorn api_service.main:app --host 127.0.0.1 --port 8000
```

The command starts one local API process on host `127.0.0.1` and fixed port
`8000`. The process reads `DATABASE_URL` and optional `APP_ENV` and `LOG_LEVEL`
values from the environment or root `.env`; application and logging defaults
are `development` and `INFO`.

## Readiness

After Uvicorn reports `Application startup complete`, verify:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/ready
```

The expected responses are `{"status":"ok"}` and `{"status":"ready"}`.
Readiness proves that the FastAPI application initialized and PostgreSQL
responded to `SELECT 1`. A missing configuration or failed database probe
returns `503` with the public error contract.

## Deterministic State

Starting the API creates no application data. Running `alembic upgrade head`
creates or advances Alembic's version state and applies committed schema
migrations.

## Interface

- OpenAPI document: `http://127.0.0.1:8000/openapi.json`
- Business API prefix: `/api/v1`
- Liveness probe: `GET /health`
- Readiness probe: `GET /ready`

Public errors use an `error.code` and safe `error.message`. Unexpected exception
details are not returned to clients.

## Tenancy Foundation

The API service persists tenants, global administrator identities, and tenant
memberships. Alembic revision `0002_tenant_foundation` creates the corresponding
PostgreSQL schema.

Tenant-scoped membership access requires a `TenantContext`, and the
`TenantMembershipRepository` derives its tenant predicate from that context. A
PostgreSQL integration test verifies that a membership belonging to one tenant
is not returned through another tenant's context.

Authentication, trusted request-context derivation, and route-level
authorization are not implemented yet. The current repository boundary and
integration test do not by themselves establish an authenticated HTTP tenant
boundary.

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
uv run alembic -c apps/api-service/alembic.ini heads
```

For real-interface validation, start the API, retrieve `/health`, `/ready`, and
`/openapi.json`, then request an unknown path and confirm a `404` response using
the public error contract. A successful `/ready` response is also the
consumer-facing PostgreSQL connectivity check.

## Unknowns

- Production worker count, bind address, process manager, and deployment
  lifecycle are not yet defined.
- Request correlation and structured logging are not yet implemented.
- Business schemas beyond the tenant, administrator, and membership foundation
  remain pending their focused product design.
