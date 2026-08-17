# Claude Code instructions

Claude Code loads this file automatically at the beginning of every session.
The imports below are mandatory repository context. Keep each `@` directive on
its own line and do not wrap it in backticks.

@AGENTS.md

@docs/WORKFLOW.md

## Automatic workflow

For every request concerning this repository:

1. Start from the requested outcome.
2. Follow `AGENTS.md` and `docs/WORKFLOW.md` without waiting for the user to
   mention Harness.
3. Before changing files, read the smallest authoritative project context:
   - root `README.md` for current product scope and architecture;
   - relevant files under `docs/product/`, `docs/decisions/`, and
     `docs/architecture/`;
   - an existing file in `docs/plans/active/` when the task continues durable
     work;
   - affected code, tests, configuration, and runbooks.
4. Do not load unrelated documentation merely because it exists.
5. If a material product, architecture, security, or compatibility decision is
   missing, stop before mutation and ask for the smallest necessary decision.
6. For an authorized change, implement the smallest coherent solution and run
   behavior-appropriate validation before claiming completion.
7. Keep repository documentation current when a change alters documented
   behavior, architecture, commands, or operating requirements.

## Git workflow

- Read and follow `CONTRIBUTING.md` for branch and contribution rules.
- `main` is the stable primary branch.
- Do not implement a feature directly on `main`.
- Before starting an authorized feature, verify the working tree is safe, switch
  to `main`, and create a new `feature/<slug>` branch.
- Use `fix/<slug>`, `refactor/<slug>`, `docs/<slug>`, or `chore/<slug>` when the
  requested work is not a feature.
- Never switch branches in a way that may overwrite uncommitted or untracked
  user work.
- Do not commit, push, merge, rebase published history, or open a pull request
  unless the user has authorized that action.

## Work shape

- Answers, explanations, reviews, diagnoses, plans, and status requests are
  read-only unless the user explicitly asks for repository changes.
- Use an ephemeral plan for bounded work.
- Create one plan under `docs/plans/active/` only when work spans sessions,
  coordinates contributors, has meaningful dependencies, or needs recovery.
- Move a durable plan to `docs/plans/completed/` only after its implementation
  and validation are complete.
- Do not invent lanes, task databases, orchestration state, stories, or control
  planes. This Harness does not provide them.

## Project boundaries

- The repository is a multi-tenant Telegram digital-commerce platform.
- The application boundaries are:
  - `apps/web-admin`: Next.js administration interface;
  - `apps/api-service`: FastAPI business API, PostgreSQL access, and payment
    webhooks;
  - `apps/bot-service`: aiogram Telegram webhook gateway and bot interaction.
- Only `api-service` may access PostgreSQL directly.
- `bot-service` and `web-admin` must use the API boundary.
- Telegram webhooks belong to `bot-service`.
- SePay and Binance Pay webhooks belong to `api-service`.
- ACB bank transfers are reconciled through SePay. Do not add a direct ACB
  Internet Banking connector unless repository authority is explicitly changed.
- Python applications use Python 3.13 and the root uv workspace. Dependency
  changes must use `pyproject.toml` and regenerate the committed `uv.lock`.
- Do not introduce pip requirements files or Poetry unless decision 0001 is
  explicitly superseded.
- Tenant-owned bot tokens and payment credentials belong in encrypted database
  configuration, not source code or tenant-specific `.env` entries.
- Every tenant-scoped operation must derive trusted tenant context and prevent
  cross-tenant access.

## Secret handling

- Never print, quote, summarize, commit, or expose values from `.env`.
- Do not place real tokens, passwords, API keys, encryption keys, OTPs, or
  private keys in source code, examples, documentation, logs, tests, or command
  output.
- Use `.env.example` only for empty placeholder names.
- Treat existing and untracked files as user work. Do not overwrite, remove, or
  clean them without explicit authorization.

## Completion

Report:

- the requested outcome;
- files or behavior changed;
- validation that actually ran and its result;
- skipped checks, blockers, and unresolved risks.

Do not claim success based only on a checklist, plan, generated file, or
unverified command.
