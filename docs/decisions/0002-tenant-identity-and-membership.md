# 0002 Tenant identity and membership

Date: 2026-08-19

## Status

Accepted

## Context

The platform serves many shops from one API and PostgreSQL database. The first
business schema must establish durable tenant identity, global administrator
identity, membership roles, and a repository boundary that prevents a caller
from selecting another tenant by supplying a raw identifier.

Email uniqueness, platform-role representation, tenant lifecycle states, and
deletion behavior materially affect every later administration and business
module.

## Decision

- Use UUID primary keys for tenants, administrators, and memberships.
- Use tenant states `provisioning`, `active`, `suspended`, and `archived`.
- Store administrators globally in `admin_users`.
- Canonicalize administrator email to lowercase and enforce global uniqueness.
- Store at most one nullable `platform_role` on `admin_users`, with values
  `platform_owner` and `platform_support`.
- Store tenant roles only in `tenant_memberships`, with values `tenant_owner`,
  `tenant_admin`, and `tenant_staff`.
- Allow multiple tenant owners.
- Preserve tenant and membership history through status changes rather than
  deleting records with dependent data.
- Require tenant-owned repositories to derive their predicate from a
  `TenantContext`, never a raw caller-supplied `tenant_id`.

## Alternatives Considered

1. Case-sensitive email uniqueness. Rejected because the same operational
   identity could be registered with casing differences.
2. A separate platform-membership table. Rejected while each administrator may
   hold at most one platform role.
3. Platform roles represented as tenant memberships. Rejected because platform
   authority and tenant authority are different trust boundaries.
4. Database-per-tenant. Rejected because the accepted platform architecture is
   one shared multi-tenant database with tenant-scoped business data.

## Consequences

Positive:

- Administrator identity is stable across multiple tenant memberships.
- Platform and tenant authority remain distinct.
- Tenant-owned repository APIs make the tenant predicate mandatory.
- Later business tables can consistently reference tenant UUIDs.

Tradeoffs:

- Authentication must canonicalize email using the same lowercase rule.
- Database Row-Level Security is not enabled yet.
- Trusted `TenantContext` derivation cannot be completed until session and bot
  authentication exist.

## Follow-Up

- Implement authenticated session and bot sources for `TenantContext`.
- Add tenant status-transition services and authorization.
- Apply the tenant-owned repository boundary to each business module.
- Evaluate PostgreSQL Row-Level Security before production data is introduced.
