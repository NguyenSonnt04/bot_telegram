# Threat Model for Telegram Digital Shop

**Last Updated:** 2026-08-17
**Version:** 1.0.0
**Methodology:** STRIDE + Natural Language Analysis

---

## 1. System Overview

### Architecture Description

Telegram Digital Shop is a planned multi-tenant digital-commerce platform. A
tenant operates a Telegram bot and administration interface while the platform
provides catalog, inventory, ordering, payments, and digital delivery.

The repository defines three application boundaries:

1. **API service** - FastAPI business API, the only application allowed to
   access PostgreSQL, and the owner of SePay and Binance Pay webhooks.
2. **Bot service** - aiogram Telegram webhook gateway that resolves a trusted
   bot and tenant context before calling the API service.
3. **Web admin** - Next.js administration interface that calls the API service
   and must not access PostgreSQL directly.

Only the FastAPI foundation currently has executable code. It exposes
`GET /health`, `GET /ready`, OpenAPI metadata, and a common public error
contract. Authentication, tenant context, database access, payment processing,
file delivery, and the web and bot runtimes are not implemented yet.

### Key Components

| Component | Purpose | Security Criticality | Attack Surface |
| --- | --- | --- | --- |
| API service | Business rules, data access, payment webhooks | HIGH | Public HTTP API and future provider webhooks |
| Bot service | Telegram webhook gateway and bot interaction | HIGH | Telegram webhook updates and bot credentials |
| Web admin | Tenant and platform administration | HIGH | Browser sessions, forms, uploads, API calls |
| PostgreSQL | Tenant, order, payment, inventory, and audit data | HIGH | API-service database connection only |
| Object storage | Tenant-owned digital products | HIGH | Upload, download, and signed object access |
| Payment providers | SePay and Binance Pay integrations | HIGH | Signed webhooks and outbound API calls |

### Data Flow

Telegram and browser requests enter through the bot service or web admin, then
cross into the API service. The API service must derive tenant context from a
trusted bot identity or authenticated session before reading or writing
business data. Payment providers send externally controlled webhooks directly
to the API service, where signatures, provider identity, amount, order
reference, and idempotency must be verified before an order or delivery changes.

The current foundation has no persistent data flow. Its public endpoints return
static process state and safe errors.

---

## 2. Trust Boundaries & Security Zones

### Trust Boundary Definition

The system has four trust zones:

1. **Public zone**
   - Unauthenticated Telegram updates, payment webhooks, health probes, and
     browser traffic.
   - All fields and headers are attacker controlled until validated.
2. **Authenticated tenant zone**
   - Tenant owners, admins, and staff with valid sessions.
   - A valid identity does not grant access to another tenant.
3. **Platform administration zone**
   - Platform owner and support roles.
   - Support access must not reveal full tenant secrets or inventory.
4. **Internal data zone**
   - API service, PostgreSQL, encryption keys, object storage credentials, and
     provider credentials.
   - Bot service and web admin may cross this boundary only through the API.

### Authentication & Authorization

Authentication and authorization are not implemented. Repository authority
requires role-based administration, trusted tenant derivation, and prevention
of cross-tenant access. Future authentication code must establish both actor
identity and tenant membership before business access.

**Critical Security Controls:**

- Only `api-service` may connect directly to PostgreSQL.
- Never trust browser-supplied `tenant_id`.
- Telegram webhook identity must be resolved from a public bot identifier and
  verified webhook secret.
- Payment webhooks require provider-specific authenticity and idempotency
  checks.
- Tenant credentials and inventory secrets must be encrypted and never logged.

---

## 3. Attack Surface Inventory

### External Interfaces

#### Current Public HTTP Endpoints

- `GET /health` - Process liveness.
  - **Input:** No request body.
  - **Validation:** No input is consumed.
  - **Risk:** Probe abuse and minor service fingerprinting.
- `GET /ready` - FastAPI initialization readiness.
  - **Input:** No request body.
  - **Validation:** Reads application lifecycle state.
  - **Risk:** Service availability disclosure.
- `GET /openapi.json` - Framework-generated API metadata.
  - **Input:** No request body.
  - **Validation:** Framework managed.
  - **Risk:** Attack-surface discovery if exposed in production.

#### Planned Public HTTP Interfaces

- `/api/v1/*` browser and bot business operations.
- `/webhooks/telegram/{bot_public_id}/{webhook_secret}` Telegram updates.
- SePay and Binance Pay webhook routes owned by `api-service`.
- Product and inventory upload routes owned by the admin surface.

### Data Input Vectors

The planned system accepts input from Telegram updates, browser forms and file
uploads, payment-provider webhook bodies and headers, environment
configuration, object metadata, and database records. Every vector must be
treated as untrusted at its boundary.

---

## 4. Critical Assets & Data Classification

### PII

- Telegram user identifiers and profile information.
- Administrator identities and tenant memberships.
- Support and warranty messages that may contain sensitive user content.

**Protection Measures:** Tenant-scoped authorization, minimal logging,
encrypted transport, retention controls, and restricted support access.

### Credentials & Secrets

- Telegram bot tokens and webhook secrets.
- SePay and Binance Pay credentials and webhook verification material.
- JWT, application, database, inventory, and payment encryption keys.
- Digital inventory credentials and private product contents.

**Protection Measures:** System keys remain outside the database; tenant
credentials are encrypted before persistence; secrets are masked in admin
responses and excluded from logs, source code, and `.env.example`.

### Business-Critical Data

- Orders, payments, wallet ledgers, refunds, and deliveries.
- Tenant catalogs, inventory, subscriptions, and quotas.
- Payment webhook event history and audit logs.

---

## 5. Threat Analysis

### S - Spoofing Identity

#### Threat: Forged tenant, bot, administrator, or provider identity

**Scenario:** An attacker supplies another tenant identifier, guesses a bot
webhook path, steals a session, or submits a fake payment-provider notification.

**Vulnerable Components:** Future API authentication, bot registry, Telegram
webhook gateway, payment webhooks, and admin sessions.

**Attack Vector:**

1. Attacker obtains or guesses a public resource identifier.
2. Request supplies an untrusted tenant or order reference.
3. Server fails to bind the request to a verified session, bot, or provider.
4. Attacker acts as another tenant or confirms an unpaid order.

**Existing Mitigations:** Repository authority forbids trusting browser
`tenant_id`, assigns webhook ownership, and requires webhook verification.

**Gaps:** Authentication, membership enforcement, bot lookup, webhook signature
verification, and session security are not implemented.

**Severity:** CRITICAL | **Likelihood:** HIGH

### T - Tampering with Data

#### Threat: Order, payment, wallet, or inventory manipulation

**Scenario:** Unvalidated request or webhook data modifies amount, status,
inventory assignment, or wallet balance.

**Existing Mitigations:** Money must use integer minor units; webhook handling
must be idempotent; delivery must be transactional.

**Gaps:** Persistence, transaction boundaries, provider verification, and
business validation are not implemented.

**Severity:** CRITICAL | **Likelihood:** HIGH

### R - Repudiation

#### Threat: Sensitive administrative or financial actions lack durable evidence

**Scenario:** An administrator changes payment configuration or manually
redelivers inventory, then denies the action because no actor, tenant, request,
or before/after evidence was recorded.

**Existing Mitigations:** Product authority requires `audit_logs` for important
administrative actions.

**Gaps:** Audit persistence and request correlation are not implemented. Current
Uvicorn access logs are process-local and do not identify an authenticated
actor or tenant.

**Severity:** HIGH | **Likelihood:** MEDIUM

### I - Information Disclosure

#### Threat: Cross-tenant data or secrets leak through APIs, logs, or files

**Scenario:** A query omits tenant scope, an error returns implementation
details, or logs record credentials or private inventory.

**Existing Mitigations:** The current API returns generic unexpected errors and
logs only method and path. Repository authority requires encrypted credentials,
masked admin responses, and tenant-scoped operations.

**Gaps:** Database query enforcement, secret encryption, object storage
isolation, response schemas, and log redaction are not implemented.

**Severity:** CRITICAL | **Likelihood:** HIGH

### D - Denial of Service

#### Threat: Public endpoints or tenant workloads exhaust shared resources

**Scenario:** Attackers flood webhooks, submit large uploads, create expensive
queries, or cause repeated provider retries.

**Existing Mitigations:** Redis may later support tenant-aware rate limiting;
the current health endpoints perform constant work.

**Gaps:** Rate limits, upload bounds, pagination enforcement, timeouts, queue
limits, and provider retry controls are not implemented.

**Severity:** HIGH | **Likelihood:** HIGH

### E - Elevation of Privilege

#### Threat: Tenant staff gain tenant-owner or platform privileges

**Scenario:** A route checks authentication but omits membership role and tenant
scope, allowing an authenticated user to alter bots, payment configuration, or
platform subscriptions.

**Existing Mitigations:** Product roles and tenant boundaries are documented.

**Gaps:** RBAC middleware, policy enforcement, negative authorization tests, and
platform-support restrictions are not implemented.

**Severity:** CRITICAL | **Likelihood:** MEDIUM

---

## 6. Vulnerability Pattern Library

### SQL Injection

```python
# Vulnerable
query = f"SELECT * FROM orders WHERE tenant_id = '{tenant_id}'"

# Safe
statement = select(Order).where(
    Order.tenant_id == trusted_tenant_id,
    Order.id == order_id,
)
```

### XSS

```tsx
// Vulnerable
<div dangerouslySetInnerHTML={{ __html: tenantSuppliedText }} />

// Safe
<div>{tenantSuppliedText}</div>
```

### Command Injection

```python
# Vulnerable
subprocess.run(f"tool {user_value}", shell=True)

# Safe
subprocess.run(["tool", validated_value], check=True)
```

### Path Traversal

```python
# Vulnerable
path = upload_root / user_filename

# Safe
object_key = f"{trusted_tenant_id}/{generated_object_id}"
```

### Authentication Bypass

```python
# Vulnerable
tenant_id = request.json()["tenant_id"]

# Safe
tenant_id = authenticated_membership.tenant_id
```

### IDOR

```python
# Vulnerable
order = await repository.get(order_id)

# Safe
order = await repository.get_for_tenant(
    tenant_id=trusted_tenant_id,
    order_id=order_id,
)
```

---

## 7. Security Testing Strategy

### Automated Testing

| Tool | Purpose | Frequency |
| --- | --- | --- |
| Ruff | Python static quality checks | Every change |
| Pytest | Unit, boundary, and negative security tests | Every change |
| Dependency scanner | Known vulnerable dependencies | Not configured |
| Secrets detection | Leaked credentials | Not configured |
| Browser/API security tests | Authorization and user-flow checks | After surfaces exist |

### Manual Security Reviews

Human review is required for authentication and authorization, tenant-scoped
data access, cryptographic code, payment verification, digital delivery,
administrator privileges, file upload, and any HIGH or CRITICAL finding.

---

## 8. Assumptions & Accepted Risks

### Security Assumptions

1. TLS termination will be required before public deployment.
2. PostgreSQL credentials will grant only application-required privileges.
3. Payment-provider verification requirements will be taken from current
   provider documentation during implementation.

### Accepted Risks

1. Current `/ready` verifies only FastAPI lifecycle initialization because
   database integration does not exist.
2. Current logs lack request correlation because no authenticated or
   tenant-scoped operation exists yet.
3. OpenAPI and probe exposure policy is undecided for production.

---

## 9. Threat Model Changelog

### Version 1.0.0 (2026-08-17)

- Created initial STRIDE model from repository product authority.
- Distinguished current FastAPI foundation from planned system behavior.
- Added Python, FastAPI, Next.js, webhook, tenant-isolation, and data-access
  vulnerability patterns.
