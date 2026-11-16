# Billing Model

How usage maps to cost, plan tiers explained.

## Plans

| Plan       | Price/month | Token limit | Requests/min | Tools                  |
|------------|-------------|-------------|---------------|-------------------------|
| Free       | $0          | 10,000      | 30            | database                |
| Pro        | $49         | 100,000     | 120           | database, file, api     |
| Enterprise | $499        | 1,000,000   | 600           | database, file, api     |

An admin can override a tenant's token limit (`POST /admin/quota-override`),
which takes precedence over the plan default.

## Usage to cost

Every agent run records a real `UsageRecord` (tokens, cost, tool_calls) —
tokens are estimated from the request/response size
(`services/token_estimator.py`), and cost is tokens priced at
`COST_PER_1K_TOKENS` (`billing/plans.py`, currently $0.002/1k tokens).

Quota is enforced cumulatively: `QuotaService` sums a tenant's token usage
over a rolling 30-day billing cycle and rejects (`402`) a request that
would push it over the plan limit (or override). A quota-warning
notification fires once at 80% of the limit, and again on rejection.

`POST /billing/invoice` aggregates a tenant's usage into billable line
items, persists an `Invoice` record, and sends an invoice-created
notification. Stripe subscriptions and webhook-driven invoice
events (`invoice.payment_succeeded`/`invoice.payment_failed`/
`customer.subscription.deleted`) are handled via `BillingService` and the
signature-verified `/billing/webhook` endpoint.
