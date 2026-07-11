from typing import Any

DEFAULT_ACTOR_ID = "demo-user"
DEFAULT_ACTOR_ROLE = "owner"
DEFAULT_WORKSPACE_ID = "demo-workspace"


def success_envelope(
    data: dict[str, Any],
    request_id: str,
    trace_id: str,
    workspace_id: str = DEFAULT_WORKSPACE_ID,
    actor_id: str = DEFAULT_ACTOR_ID,
    actor_role: str = DEFAULT_ACTOR_ROLE,
) -> dict[str, Any]:
    return {
        "data": data,
        "meta": {
            "request_id": request_id,
            "trace_id": trace_id,
            "workspace_id": workspace_id,
            "actor_id": actor_id,
            "actor_role": actor_role,
        },
        "errors": [],
    }
