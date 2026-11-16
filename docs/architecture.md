# Architecture

System diagram and data flow for the Agent Platform SaaS.

## Overview

Clients authenticate with per-tenant API keys (`X-API-Key`). The
`TenantContextMiddleware` looks up the tenant by an indexed hash of that key
and injects it into `request.state`. `RateLimitMiddleware` then enforces a
Redis-backed token bucket sized by the tenant's plan (free/pro/enterprise
each have a different `requests_per_minute`; unauthenticated requests share
a conservative anonymous allowance). Requests are routed through
`Orchestrator` to the appropriate LangGraph agent (query, processor,
research), each of which calls a real MCP tool (database, file, or API)
rather than returning placeholder data.

Admin dashboard access is separate from tenant API keys: admin users are
stored in their own table with bcrypt-hashed passwords, bootstrapped on
first startup from `ADMIN_USERNAME`/`ADMIN_PASSWORD`. Startup also refuses
to boot in `APP_ENV=production` if `JWT_SECRET` or `ADMIN_PASSWORD` are
still at their insecure defaults.

## Data Flow

1. Client call -> API key auth -> tenant resolution (indexed hash lookup)
2. Per-plan rate limit check
3. Quota check against cumulative usage this billing cycle (plan limit,
   or an admin-set override) — rejects with 402 and sends a quota-warning
   notification if exceeded, or at 80% of quota
4. Agent execution via orchestrator, using a real MCP tool (DB read,
   sandboxed file read, or SSRF-guarded HTTP fetch)
5. Real usage record written (tokens/cost/tool_calls derived from the
   agent's actual work, not a placeholder zero)
6. Billing aggregation + invoice generation, Stripe webhooks verified by
   signature and dispatched by event type

## MCP tools

- **database** — runs one of an allowlisted set of tenant-scoped read
  queries (usage summary, invoices); not arbitrary SQL.
- **file** — reads files from a per-tenant sandbox directory
  (`FILE_TOOL_ROOT/<tenant_id>/`); rejects any path that resolves outside
  that sandbox.
- **api** — fetches a URL with SSRF protection: blocks literal private/
  loopback/link-local IPs *and* hostnames that resolve to one, so a
  DNS name can't be used to bypass the IP-literal check.

## Known limitations

- Token/cost accounting uses a `len(json) / 4` heuristic
  (`services/token_estimator.py`), not a real tokenizer — fine for
  relative metering, not for exact LLM billing reconciliation.
- Rate limiting fails open if Redis is unreachable.
