# Product Docs

This directory contains focused consumer-product behavior derived from accepted
intent in this repository.

The root [`README.md`](../../README.md) currently owns the consolidated product
scope, architecture, security boundaries, roadmap, and implementation status.
As domains become implementation-ready, derive smaller living documents here
instead of keeping one growing specification as the operating manual. Name
files after actual product domains, such as `tenancy.md`, `catalog.md`,
`ordering.md`, `payments.md`, or `permissions.md`.

## Current Product Contract

No focused product-domain document has been accepted yet. Until one exists, use
the root README, accepted decisions, implementation, and executable tests as
the current consumer authority. Do not infer missing product policy from
Harness templates or upstream source repositories.

## Update Rule

When behavior changes:

1. Update the affected product document when the expected behavior changed.
2. Update the active execution plan when complex work uses one.
3. Add a lasting decision only when future work must inherit a consequential
   product, architecture, data, security, compatibility, or validation choice.
4. Add or update executable proof that exercises the behavior.

Bounded changes do not require a parallel lifecycle record.
