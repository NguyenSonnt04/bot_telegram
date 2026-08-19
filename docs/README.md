# Documentation Map

Start with the smallest authoritative surface.

## Repository Authority

- Root [`README.md`](../README.md): current product scope, architecture,
  security boundaries, technology choices, roadmap, and implementation status.
- `WORKFLOW.md`: request shape, planning, judgment, operation, validation, and
  completion.
- `product/`: focused living product contracts as they are accepted.
- `decisions/`: lasting product, architecture, data, security, compatibility,
  and validation choices.
- `plans/`: durable working memory only for work that needs cross-session
  recovery or coordination.
- `runbooks/`: verified application startup, readiness, interface, evidence, and
  cleanup procedures.
- [`patterns/encoding-invariants.md`](patterns/encoding-invariants.md):
  mechanical enforcement method for accepted architecture, reliability,
  security, and quality rules.
- `templates/`: optional structures for decisions, plans, runbooks, and Harness
  improvements.
- `../apps/`, `../packages/`, `../tests/`, configuration, and runtime signals:
  executable and observable behavior.

## Consumer-Owned Truth

The consumer's README, product documents, architecture, code, tests, CI,
runtime signals, and application behavior remain authoritative. Harness does
not overwrite those with upstream product assumptions.

## Installed Harness

- [`../AGENTS.md`](../AGENTS.md): agent entrypoint and authority boundary.
- [`../.agents/skills/`](../.agents/skills/): installed repository skills.
- [`../.harness-core/manifest.json`](../.harness-core/manifest.json): installed
  core version and managed-file provenance.
- `../scripts/bin/harness.exe`: Windows maintenance interface for status,
  doctor, install, and conflict-safe updates.

Harness supplies workflow and maintenance capability. It does not replace
consumer product authority or require upstream source-tree documentation in
this repository.
