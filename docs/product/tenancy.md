# Tenancy Contract

## Scope

This contract defines platform administrator identities, tenant lifecycle
identity, tenant membership, and the trusted tenant boundary used by business
data access.

## Tenant Identity

- Every tenant uses a UUID primary key.
- Tenant status is one of `provisioning`, `active`, `suspended`, or `archived`.
- Suspending a tenant blocks tenant operation without deleting its history.
- Archiving is the terminal retention state for a tenant with business data.
- Tenant records with dependent data must not be hard-deleted.
- Status-transition workflows remain out of scope until tenant administration
  behavior is implemented.

## Administrator Identity

- `admin_users` is global across the platform.
- Email is canonicalized to lowercase before persistence and is unique across
  the platform.
- Passwords are stored only as password hashes. Authentication and password
  policy implementation remain separate work.
- A global administrator may have one nullable `platform_role`:
  `platform_owner` or `platform_support`.
- Platform roles do not grant tenant membership and must not be represented as
  tenant membership records.

## Tenant Membership

- `tenant_memberships` links one global administrator to one tenant.
- A user may have at most one membership record per tenant.
- Tenant membership role is one of `tenant_owner`, `tenant_admin`, or
  `tenant_staff`.
- Multiple tenant owners are allowed.
- Disabling a membership preserves its history.

## Trusted Tenant Boundary

Repository authority: the root [`README.md`](../../README.md) requires every
business query to carry tenant context and requires cross-tenant isolation
tests.

- Tenant-scoped repositories require a `TenantContext`; they do not accept a
  caller-supplied `tenant_id` query argument.
- Every tenant-owned query must add its tenant predicate from that context.
- A query for tenant A must not return a tenant B record even when the remaining
  identifier matches.
- HTTP sessions and bot identity will become trusted context sources when those
  authentication boundaries are implemented.
- Until then, repository tests prove the tenant predicate and reject repository
  construction without a `TenantContext`.

There are no authorized exceptions for tenant-owned business repositories.
