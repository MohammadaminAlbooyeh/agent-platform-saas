# Billing Model

How usage maps to cost, plan tiers explained.

## Plans

| Plan     | Price/month | Token limit |
|----------|-------------|-------------|
| Free     | $0          | 10,000      |
| Pro      | $49         | 100,000     |
| Enterprise| $499       | 1,000,000   |

## Usage to Cost

Usage records (tokens, tool calls) are aggregated per billing cycle and
converted into billable units. Invoices are generated via Stripe.
