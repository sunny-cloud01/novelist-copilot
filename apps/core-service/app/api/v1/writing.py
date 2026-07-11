from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional

from app.core.envelope import success_envelope
from app.core.phase_two_store import (
    WORKSPACE_ID,
    accept_chapter,
    create_writing_run,
    get_quality_report,
    get_writing_run,
    list_feedback_records,
)

router = APIRouter()


class CreateWritingRunCommand(BaseModel):
    project_id: str
    chapter_plan_id: str
    workspace_id: str = WORKSPACE_ID
    writer_model_profile_id: Optional[str] = None
    critic_model_profile_id: Optional[str] = None
    humanizer_model_profile_id: Optional[str] = None


@router.post("/writing-runs", status_code=202)
def post_writing_run(command: CreateWritingRunCommand, request: Request) -> dict:
    result = create_writing_run(command.model_dump(exclude_none=True), request.state.trace_id)
    if not result:
        raise HTTPException(status_code=404, detail="writing dependencies not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.get("/writing-runs/{writing_run_id}")
def get_writing_run_detail(writing_run_id: str, request: Request) -> dict:
    result = get_writing_run(writing_run_id)
    if not result:
        raise HTTPException(status_code=404, detail="writing run not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.post("/writing-runs/{writing_run_id}/accept-chapter")
def post_accept_chapter(writing_run_id: str, request: Request) -> dict:
    result = accept_chapter(writing_run_id, request.state.trace_id)
    if result is None:
        raise HTTPException(status_code=404, detail="writing run not found")
    if result is False:
        raise HTTPException(status_code=409, detail="writing run acceptance dependencies incomplete")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.get("/feedback-records")
def get_feedback_records(request: Request, targetType: Optional[str] = None, targetId: Optional[str] = None) -> dict:
    result = {
        "items": list_feedback_records(targetType, targetId),
        "target_type": targetType,
        "target_id": targetId,
    }
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.get("/quality-reports/{quality_report_id}")
def get_quality_report_detail(quality_report_id: str, request: Request) -> dict:
    result = get_quality_report(quality_report_id)
    if not result:
        raise HTTPException(status_code=404, detail="quality report not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )
