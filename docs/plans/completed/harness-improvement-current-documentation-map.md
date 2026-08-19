# Harness Improvement: Current Documentation Map

Date: 2026-08-17

## Status

Completed

## Representative Job

A fresh agent must map this consumer repository before planning or changing
product work. The accepted outcome is that it opens existing repository
authority directly and does not spend retrieval attempts on absent upstream
Harness implementation or history.

Baseline worker: Droid. Repository revision:
`8ebea8569e529ccd5ee6d2eec66ab871b82cbc52`. Branch:
`docs/current-harness-map`. External state is not relevant. Available tools are
repository reads, search, Git inspection, and the installed Harness maintenance
binary. The user explicitly authorized removing upstream-only references from
the current consumer documentation map.

## Baseline

During repository onboarding, `docs/README.md` directed the worker to
`ARCHITECTURE.md` and `HARNESS.md`, but both files were absent. It also described
`crates/harness/`, upstream scripts and tests, and `harness-cli-v*` history that
do not exist in this consumer repository. The worker needed failed reads,
repository-wide searches, and human clarification before concluding those
references were irrelevant.

Existing proof:

- `docs/README.md` contains the absent and upstream-only references.
- Repository search finds those names only in the installed file and its
  `.harness-core/base` ancestor.
- `scripts/bin/harness.exe status` reports Harness core `0.1.10` as current.
- `scripts/bin/harness.exe doctor` passes provenance, path, transaction, and
  three-way-merge checks.

Known limitation: one observed onboarding run establishes concrete friction but
does not prove every future agent would follow the stale references.

## Earliest Gap

**Context:** the first documentation map mixes consumer authority with upstream
repository implementation and history. The stale retrieval route appears before
agents reach the existing root README, decisions, plans, code, and tests.

## Correct Owner

The consumer repository owns the correction in `docs/README.md`. The installed
Harness update mechanism explicitly tracks consumer modifications and supports
three-way updates, so `.harness-core/base`, its manifest checksum, and the
installed core version must remain unchanged.

## Intervention

If upstream-only entries are replaced with existing consumer authority in
`docs/README.md` and `docs/product/README.md`, then a fresh agent will retrieve
the root README, workflow, decisions, plans, code, tests, runbooks, and installed
Harness surfaces directly on a repository-mapping job, because the current
documentation route no longer advertises absent files, generic upstream
contracts, or upstream source-tree history.

Evidence that would weaken this: a fresh agent still searches for the removed
upstream paths, misses an important existing authority surface, or the Harness
doctor/update preview cannot safely preserve the consumer modification.

Maintenance owner: this consumer repository. Removal condition: restore or
replace an entry only when that path becomes real authority in this repository,
or when a future Harness version supplies a more accurate consumer map.

## Native Validation

The first intervention passed link validation, `git diff --check`,
`harness status`, and `harness doctor`. The installed core remained `0.1.10`;
the status command identified `docs/README.md` as a supported consumer
modification while provenance and three-way-merge checks remained healthy.

After both revisions:

- all explicit Markdown links in `docs/README.md` and
  `docs/product/README.md` resolve;
- the current documentation route contains no `ARCHITECTURE.md`, `HARNESS.md`,
  `crates/harness`, `harness-cli-v*`, `repository-harness`, or
  `docs/architecture.md` reference;
- `git diff --check` passes;
- Harness status reports only expected consumer modifications; and
- Harness doctor continues to pass transaction, provenance, path, and
  three-way-merge checks.

## Fresh Rerun

Fresh rerun 1 used a new read-only explorer with the same repository-mapping
task and no chat history. It retrieved the corrected `docs/README.md`, reached
existing consumer authority without upstream source/history, and required no
human clarification. It also found the same stale upstream framing in
`docs/product/README.md`, so the intervention was relevant but incomplete.

Fresh rerun 2 retrieved the revised repository and product maps, used no
upstream Harness source or history, and required no human clarification. It
found one generic diagnostic example in `patterns/encoding-invariants.md` that
looked like a real but absent `docs/architecture.md` authority path. The example
was revised to require an explicit accepted-authority placeholder.

Fresh rerun 3 used another new read-only explorer with the same mapping task. It
retrieved `docs/WORKFLOW.md`, the corrected documentation map, the root README,
the product index, accepted decision 0001, contribution rules, manifests, and
tests. It encountered no current generic-upstream or nonexistent Harness path,
needed no upstream Harness source or history, and required no human
clarification for authority mapping.

The rerun noted that root `README.md` still says it predates code while package
scaffolding and import tests now exist. That is a separate consumer-product
status correction, not a Harness routing defect.

## Decision

Keep.

Three fresh reruns exercised the intervention. The first two exposed incomplete
adjacent routing context, which was revised. The final rerun followed only
existing consumer authority, avoided the former failed retrievals, and required
no human steering. The maintenance cost is three small consumer modifications
that the installed Harness explicitly tracks and can three-way merge.

## Handoff

- Current branch: `docs/current-harness-map`
- Working tree: clean after the validated documentation commit.
- Delivery state: committed and pushed to
  `origin/docs/current-harness-map`; not merged into `main`.
- Commit or pull request: implementation commit
  `478bd4933ecbb21b6beee6940d98d0495ce4eb93`; no pull request recorded.
- Remaining blockers or follow-up: the root README initialization-era status
  sentence remains separate product-documentation work.
- Next safe action: review and merge the documentation branch through the
  repository contribution flow.

## Result

The current documentation route now describes this repository rather than the
upstream Harness source repository. Retain the intervention while these paths
remain the consumer authority.

Follow-up outside this experiment: update the root README's initialization-era
status sentence when product documentation work is next authorized.
