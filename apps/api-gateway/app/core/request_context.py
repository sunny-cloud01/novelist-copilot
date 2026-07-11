from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import ulid

DEFAULT_ACTOR_ID = "demo-user"
DEFAULT_ACTOR_ROLE = "owner"
DEFAULT_WORKSPACE_ID = "demo-workspace"


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("x-request-id", str(ulid.new()))
        trace_id = request.headers.get("x-trace-id", str(ulid.new()))
        workspace_id = request.headers.get("x-workspace-id", DEFAULT_WORKSPACE_ID)
        actor_id = request.headers.get("x-actor-id", DEFAULT_ACTOR_ID)
        actor_role = request.headers.get("x-actor-role", DEFAULT_ACTOR_ROLE)

        request.state.request_id = request_id
        request.state.trace_id = trace_id
        request.state.workspace_id = workspace_id
        request.state.actor_id = actor_id
        request.state.actor_role = actor_role

        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        response.headers["x-trace-id"] = trace_id
        response.headers["x-workspace-id"] = workspace_id
        response.headers["x-actor-id"] = actor_id
        response.headers["x-actor-role"] = actor_role
        return response
