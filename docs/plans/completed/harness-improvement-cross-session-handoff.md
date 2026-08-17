# Harness Improvement: Cross-Session Completion Handoff

Date: 2026-08-17

## Status

Completed

## Representative Job

A fresh AI session must determine what an authorized coding task completed,
what proof passed, where the work was delivered, what remains unresolved, and
the next safe action without reconstructing those facts from chat history.

Baseline worker: Droid. Repository revision:
`478bd4933ecbb21b6beee6940d98d0495ce4eb93`. Branch:
`docs/current-harness-map`. Relevant repository state:

- `main` and `origin/main` point to `8ebea85`;
- `feature/api-foundation` and its remote point to `38522d2`; and
- the API branch records FastAPI as initialized while `main` still records it
  as incomplete.

Available tools are repository reads, Git inspection, validation commands, and
fresh read-only agents. The user explicitly authorized a Harness improvement
that preserves completed coding context across sessions. This experiment does
not authorize merging branches, changing product policy, or creating a task
database.

## Baseline

The previous coding trajectory completed and pushed the API foundation on a
feature branch, but a later session required a generated chat summary to recover
the work. When the user sent `resume`, only checklist finalization remained and
the user had to ask why the agent appeared not to continue.

Current repository evidence shows why delivery state matters:

- `README.md` on the current base still says the repository predates code and
  marks FastAPI initialization incomplete.
- `README.md` on `feature/api-foundation` contains local startup guidance and
  marks FastAPI initialization complete.
- The current completion standard requires outcome, proof, current repository
  truth, and plan state, but does not explicitly require branch, commit,
  push/PR/merge state, unresolved work, or the next safe action.
- The execution-plan result section requests outcome, limitations, and
  follow-up, but has no explicit handoff fields.

Human steering was required to explain that the user wants future sessions to
recover from repository state rather than conversation memory.

Known limitation: repository guidance cannot make unmerged feature work become
authority on `main`. A fresh clone that only reads `main` can know unmerged work
only by inspecting remote branches or pull requests.

## Earliest Gap

**Context and delivery:** the workflow describes when to update repository truth
but does not define a completion handoff that distinguishes implemented,
committed, pushed, opened for review, and merged state. It also does not require
the next safe action when work remains.

## Correct Owner

The consumer repository owns this behavior in `docs/WORKFLOW.md`, which every
repository agent is instructed to read. `docs/templates/exec-plan.md` owns the
durable-plan shape. Product status remains with its existing product, decision,
runbook, code, test, Git, and pull-request owners.

Do not modify `.harness-core`, create a global session log, or copy product
status into a second task database.

## Intervention

If a concise cross-session handoff protocol is added to `docs/WORKFLOW.md` and
explicit handoff fields are added to both durable-plan templates, then a fresh
agent will recover completed and remaining work from canonical repository and
Git state, because every authorized change must either remain self-describing
through its diff and delivery state or update the one durable plan required for
safe continuation.

The protocol will require:

- canonical product, decision, runbook, and plan owners to be updated only when
  their truth changes;
- durable unfinished work to record progress, proof, blockers, delivery state,
  and the next safe action before a session ends;
- completed durable plans to record branch, commit, push/PR/merge state, and
  follow-up before moving to `completed/`;
- bounded work to rely on code, tests, Git, and the final report rather than
  creating a per-session status file; and
- new sessions to distinguish current-branch work from authority merged into
  `main`.

Evidence that would weaken this: a fresh agent still needs chat history or human
relay to identify delivery state and next action, treats an unmerged branch as
`main` authority, or creates redundant status artifacts for bounded work.

Maintenance owner: this consumer repository. Removal condition: remove or
replace the protocol if repository-native automation or a single better owner
provides equivalent handoff without duplicate state.

## Native Validation

Initial validation:

- `git diff --check` passes.
- Harness status reports core `0.1.10` as current and identifies the workflow
  and plan-template edits as supported consumer modifications.
- Harness doctor passes transaction, update-resolution, three-way-merge,
  provenance, and managed-path checks.
- Harness update dry-run could not reach the upstream release-tag endpoint
  because it returned HTTP 429. No update was applied and local status/doctor
  remained healthy.

After revising both durable-plan templates:

- `git diff --check` passes;
- Harness status still reports core `0.1.10` as current;
- Harness doctor still passes transaction, update-resolution, three-way-merge,
  provenance, and managed-path checks; and
- the workflow, execution-plan template, Harness-improvement template, and this
  experiment use the same delivery-state and next-action vocabulary.

## Fresh Rerun

Fresh rerun 1 used a new read-only explorer with no chat history and asked it to
recover completed coding, delivery state, `main` authority, unresolved work,
and the next safe action.

The worker retrieved the new workflow protocol, distinguished the workspace
commit merged on `main` from the API commit pushed only to its feature branch,
identified the current documentation changes as working-tree work, avoided a
global session-status database, and recommended inspecting status and updating
the existing active plan before delivery.

The intervention was available, retrieved, relevant, and sufficient for the
recovery job. The rerun also exposed one consistency gap: the active Harness
experiment is itself durable work, but its template had no explicit handoff
fields. The intervention was revised to add them.

Fresh rerun 2 used another new read-only explorer with no chat history. It
retrieved the workflow protocol, both durable-plan templates, and this active
plan. It correctly separated:

- workspace work merged on `main`;
- API and documentation-map commits pushed only to feature/documentation
  branches;
- unverified pull-request state; and
- the current handoff intervention as working-tree-only work.

It found the three guidance surfaces internally consistent, considered this
plan sufficient for another session, recommended the recorded next safe action,
and needed no chat history or human relay for recovery.

## Decision

Keep.

The first rerun exercised the protocol and exposed a missing handoff section in
the Harness-improvement template. After revision, the second rerun exercised all
three surfaces and recovered the accepted outcome without conversation memory.
The maintenance cost is a short workflow section and matching fields in the two
existing durable-plan templates, with no new state system.

## Handoff

- Current branch: `docs/current-harness-map`
- Working tree: expected clean after the validated documentation commit.
- Delivery state: committed and pushed to
  `origin/docs/current-harness-map`; not merged into `main`.
- Commit or pull request: use the current branch tip; no pull request is
  recorded by this experiment.
- Remaining blockers or follow-up: Harness update dry-run was externally
  blocked by HTTP 429. The API and documentation branches remain outside
  `main`, so a session starting from `main` must inspect remote branch or pull
  request state to discover them.
- Next safe action: review and merge the documentation branch through the
  repository contribution flow, then separately review the API foundation for
  merge into `main`.

## Result

Future sessions now have a repository-native completion protocol. Bounded work
remains self-describing through canonical documentation, code, tests, Git, and
delivery state. Durable work must persist progress, validation, blockers,
delivery state, and the next safe action in one plan before pausing or moving to
another session.

The intervention intentionally does not update `.harness-core`, create a global
status file, infer remote pull-request state, or make unmerged work authoritative
on `main`.
