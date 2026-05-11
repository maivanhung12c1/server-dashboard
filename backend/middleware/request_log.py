import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestLogMiddleware(BaseHTTPMiddleware):
    """Log method, path, status, and duration for every HTTP request."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        rid = getattr(request.state, "request_id", "-")
        
        logger.info(
            "{method} {path} -> {status} ({ms:.1f} ms) [{rid}]",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            ms=duration_ms,
            rid=rid
        )
        return response