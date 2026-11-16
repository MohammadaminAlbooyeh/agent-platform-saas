# API Reference

All tenant-scoped endpoints require an `X-API-Key` header. Admin endpoints
require `Authorization: Bearer <admin JWT>` from `/admin/login`.

## Agent

- `POST /agent/execute` — `{"agent_type": "query"|"processor"|"research", "payload": {...}}`.
  Returns `{"task_id", "status": "completed"}` on success, or `402` if the
  tenant's token quota (plan limit or admin override) is exceeded.
  - `query` payload: `{"query": "usage_summary"|"invoices"}` (free-form
    text is accepted and normalized; unrecognized values fall back to
    `usage_summary`).
  - `processor` payload: `{"operation": "identity"|"uppercase_keys"|"sum"|"count"|"dedupe", "data": ...}`.
  - `research` payload: `{"topic": "..."}` and/or `{"url": "https://..."}` —
    if `url` is given, it's fetched through the SSRF-guarded API tool.
- `POST /agent/stream` — same payload, returns one SSE `data:` event with
  the result.
- `GET /agent/status/{task_id}` — status stub (always "completed").

## Tools

- `GET /tools` — lists MCP tools available for the caller's plan.
- `POST /tools/test` — `{"tool": "database"|"file"|"api", ...tool kwargs}`;
  403 if the tool isn't on the caller's plan.

## Tenants

- `POST /tenants` — `{"name": str, "plan": "free"|"pro"|"enterprise"}` ->
  `201` with the new tenant and its plaintext API key (shown once).
- `GET /tenants/{id}` — tenant metadata (no API key).

## Billing

- `POST /billing/subscribe` — `{"plan_id": "pro"|"enterprise"}`.
- `POST /billing/invoice` — aggregates the caller's usage into an invoice,
  persists it, and sends an invoice-created notification.
- `POST /billing/webhook` — Stripe webhook receiver. Verifies the
  `Stripe-Signature` header against `STRIPE_WEBHOOK_SECRET` when set;
  without a configured secret it accepts the payload unverified (logged
  as a warning) — only safe for local development.

## Usage

- `GET /usage/{tenant_id}` — per-tenant usage stats (tokens, cost,
  tool_calls, record_count) over the last 24h by default. Callers may
  only view their own usage.

## Admin

- `POST /admin/login` — `{"username", "password"}` -> admin JWT. The
  first admin user is bootstrapped on startup from
  `ADMIN_USERNAME`/`ADMIN_PASSWORD`.
- `GET /admin/tenants` — list all tenants.
- `POST /admin/quota-override` — `{"tenant_id", "token_limit"}`; persists
  a per-tenant token quota override that takes precedence over the plan
  default.
