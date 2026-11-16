"""Database MCP tool: safe, allowlisted, tenant-scoped reads."""

from mcp_tools.registry import Tool


def resolve_query_name(raw: str) -> str:
    """Map free-form input to one of the allowlisted query names."""
    normalized = (raw or "").strip().lower()
    if "invoice" in normalized:
        return "invoices"
    return "usage_summary"


def run_scoped_query(tenant_id: str, query_name: str) -> dict:
    """Run a safe, allowlisted read-only query scoped to the tenant."""
    from database.base import SessionLocal
    from database.models.invoice import Invoice
    from services.usage_service import UsageService

    name = resolve_query_name(query_name)

    if name == "invoices":
        db = SessionLocal()
        try:
            rows = (
                db.query(Invoice)
                .filter(Invoice.tenant_id == tenant_id)
                .order_by(Invoice.created_at.desc())
                .limit(50)
                .all()
            )
            return {
                "query": "invoices",
                "rows": [{"id": r.id, "amount": r.amount, "status": r.status} for r in rows],
                "row_count": len(rows),
            }
        finally:
            db.close()

    usage = UsageService().aggregate(tenant_id)
    return {"query": "usage_summary", "rows": [usage], "row_count": 1}


class DatabaseTool(Tool):
    name = "database"
    allowed_plans = ["free", "pro", "enterprise"]

    async def run(self, query: str, tenant_id: str) -> dict:
        """Run a read-only, allowlisted query scoped to the tenant."""
        data = run_scoped_query(tenant_id, query)
        return {"tool": "database", "tenant_id": tenant_id, **data}
