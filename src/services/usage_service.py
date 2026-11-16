"""Aggregates usage records into billable units service."""

import time
from datetime import datetime, timedelta, timezone

from database.base import SessionLocal
from database.models.usage_record import UsageRecord


class UsageService:
    """Service for recording and aggregating usage into billable units."""

    def record_usage(self, tenant_id: str, tokens: int = 0, cost: float = 0.0, tool_calls: int = 0) -> dict:
        """Persist a usage record for a tenant with real token/cost/tool-call counts."""
        db = SessionLocal()
        try:
            record = UsageRecord(
                id=str(time.time_ns()),
                tenant_id=tenant_id,
                tokens=tokens,
                cost=cost,
                tool_calls=tool_calls,
            )
            db.add(record)
            db.commit()
            return {"tenant_id": tenant_id, "tokens": tokens, "cost": cost, "tool_calls": tool_calls}
        finally:
            db.close()

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
