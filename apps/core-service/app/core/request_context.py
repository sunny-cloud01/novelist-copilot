from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import ulid


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id", str(ulid.new()))
        trace_id = request.headers.get("x-trace-id", str(ulid.new()))

        request.state.request_id = request_id
        request.state.trace_id = trace_id

        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        response.headers["x-trace-id"] = trace_id
        return response
