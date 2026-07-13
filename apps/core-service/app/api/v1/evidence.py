from fastapi import APIRouter, HTTPException, Request

from app.core.envelope import success_envelope
from app.core.phase_two_store import get_evidence

router = APIRouter()


@router.get("/evidence/{evidence_id:path}")
def get_evidence_detail(evidence_id: str, request: Request) -> dict:
    evidence = get_evidence(evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="evidence not found")
    return success_envelope(
        data=evidence,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
