from fastapi import APIRouter, Request

from app.core.envelope import success_envelope

router = APIRouter()


@router.get("/health")
def get_health(request: Request) -> dict:
    return success_envelope(
        data={"service": "api-gateway", "status": "ok"},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
