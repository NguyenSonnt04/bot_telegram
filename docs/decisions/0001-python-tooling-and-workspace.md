# 0001 Python tooling and workspace

Date: 2026-08-17

## Status

Accepted

## Context

The repository contains two Python applications, `apps/api-service` and
`apps/bot-service`. Development and deployment need one reproducible dependency
workflow that works on Windows, CI, and a Linux VPS without maintaining separate
virtual-environment and lock-file conventions.

## Decision

- Use Python 3.13 for both Python applications.
- Use uv as the Python package and environment manager.
- Configure the repository as a uv workspace.
- Define the workspace at the repository root in `pyproject.toml`.
- Give `api-service` and `bot-service` their own `pyproject.toml` files and
  application-specific dependencies.
- Commit one root `uv.lock` file.
- Use one root `.venv` for the workspace.
- Use `uv sync` for local development.
- Use `uv sync --frozen --no-dev` when deploying to a VPS.
- Do not hand-edit `uv.lock`.

## Alternatives Considered

1. pip with `venv` and requirements files. This is familiar but requires more
   manual coordination for environments, direct dependencies, transitive
   dependencies, and locking across two applications.
2. Poetry. This provides dependency resolution and locking but adds a separate
   project workflow and is less direct for this repository's multi-application
   workspace.

## Consequences

Positive:

- Local development, CI, and VPS deployment resolve the same dependency graph.
- Python installation, virtual environments, dependency locking, and command
  execution use one tool.
- Each application keeps its own runtime dependencies while sharing one lock.
- Dependency installation is fast enough for frequent CI and deployment runs.

Tradeoffs:

- Contributors and deployment hosts must install uv.
- Workspace commands must identify the intended package when a command is
  application-specific.
- Updating Python beyond 3.13 requires an explicit compatibility change and a
  regenerated lock file.

## Follow-Up

- Add application-specific dependencies as each service is implemented.
- Document exact migration and service startup commands after those commands
  exist and have been validated.
