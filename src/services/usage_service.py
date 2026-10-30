"""Aggregates usage records into billable units service."""

from datetime import datetime, timedelta, timezone

from database.base import SessionLocal
from database.models.usage_record import UsageRecord


class UsageService:
    """Service for aggregating usage into billable units."""

    def aggregate(self, tenant_id: str, hours: int = 24) -> dict:
        """Aggregate usage records for a tenant over the last `hours`."""
        db = SessionLocal()
        try:
            since = datetime.now(timezone.utc) - timedelta(hours=hours)
            rows = (
                db.query(UsageRecord)
                .filter(UsageRecord.tenant_id == tenant_id)
                .filter(UsageRecord.created_at >= since)
                .all()
            )
            total_tokens = sum(r.tokens or 0 for r in rows)
            total_cost = sum(r.cost or 0.0 for r in rows)
            total_calls = sum(r.tool_calls or 0 for r in rows)
            return {
                "tenant_id": tenant_id,
                "hours": hours,
                "tokens": total_tokens,
                "cost": round(total_cost, 6),
                "tool_calls": total_calls,
                "record_count": len(rows),
            }
        finally:
            db.close()
