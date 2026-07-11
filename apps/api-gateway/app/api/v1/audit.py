from fastapi import APIRouter, Request

from app.core.envelope import success_envelope
from app.core.phase_two_adapter import list_audit_events

router = APIRouter()


@router.get("/audit-events")
def get_audit_events(request: Request) -> dict:
    return success_envelope(
        data={
            "items": list_audit_events(request.state.workspace_id),
            "workspace_id": request.state.workspace_id,
        },
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
