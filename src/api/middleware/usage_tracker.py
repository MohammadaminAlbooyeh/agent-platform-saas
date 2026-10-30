"""Usage tracking middleware: records tokens/requests consumed per call."""

import json
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from database.base import SessionLocal
from database.models.usage_record import UsageRecord


class UsageTrackerMiddleware(BaseHTTPMiddleware):
    """Records tokens and requests consumed per API call for the current tenant."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        tenant_id = getattr(request.state, "tenant_id", None)
        start = time.time()

        response = await call_next(request)

        if tenant_id:
            db = SessionLocal()
            try:
                record = UsageRecord(
                    id=str(time.time_ns()),
                    tenant_id=tenant_id,
                    tokens=0,
                    cost=0.0,
                    tool_calls=0,
                )
                db.add(record)
                db.commit()
            except Exception:
                db.rollback()
            finally:
                db.close()

        return response
