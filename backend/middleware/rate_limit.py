import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from common.response.response_schema import ResponseModel
from core.conf import settings


class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app) -> None:
        super().__init__(app)

        self._buckets: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:

        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        ip = request.client.host if request.client else "unknown"

        is_write = request.method in {
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        }

        limit = (
            settings.RATE_LIMIT_WRITE_PER_MINUTE
            if is_write
            else settings.RATE_LIMIT_PER_MINUTE
        )

        now = time.monotonic()

        cutoff = now - 60.0

        bucket_key = f"{ip}:{'w' if is_write else 'r'}"
        bucket = self._buckets[bucket_key]

        while bucket and bucket[0] <= cutoff:
            bucket.popleft()

        if len(bucket) >= limit:
            return JSONResponse(
                status_code=429,
                content=ResponseModel(
                    code=429,
                    msg="Too many requests. Please slow down.",
                ).model_dump(),
                headers={
                    "Retry-After": "60",
                },
            )

        bucket.append(now)

        return await call_next(request)