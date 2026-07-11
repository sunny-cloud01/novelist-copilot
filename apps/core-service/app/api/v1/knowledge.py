from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.envelope import success_envelope
from app.core.phase_two_store import RUN_ID, apply_review_action, list_knowledge_objects_for_run

router = APIRouter()


class ReviewActionCommand(BaseModel):
    action: str
    target_object_id: Optional[str] = None
    note: Optional[str] = None


@router.get("/knowledge-objects")
def get_knowledge_objects(request: Request, run_id: str = RUN_ID) -> dict:
    items = list_knowledge_objects_for_run(run_id)
    return success_envelope(
        data={"items": items, "run_id": run_id},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.post("/knowledge-objects/{object_id}/review-actions")
def post_review_action(object_id: str, command: ReviewActionCommand, request: Request) -> dict:
    try:
        obj = apply_review_action(object_id, command.action, command.target_object_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not obj:
        raise HTTPException(status_code=404, detail="knowledge object not found")
    return success_envelope(
        data=obj,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )
