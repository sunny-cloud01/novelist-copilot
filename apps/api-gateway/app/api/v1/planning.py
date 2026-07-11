from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.core.envelope import success_envelope
from app.core.phase_two_adapter import WORKSPACE_ID, create_chapter_plan, create_section_plans, get_chapter_plan, list_section_plans

router = APIRouter()


class CreateChapterPlanCommand(BaseModel):
    project_id: str
    chapter_index: int
    target_word_count: int
    workspace_id: str = WORKSPACE_ID
    payload: dict = Field(default_factory=dict)


class CreateSectionPlansCommand(BaseModel):
    section_count: int = Field(default=4, ge=1, le=4)


@router.post("/chapter-plans", status_code=202)
def post_chapter_plan(command: CreateChapterPlanCommand, request: Request) -> dict:
    result = create_chapter_plan(command.model_dump(), request.state.trace_id)
    if not result:
        raise HTTPException(status_code=404, detail="novel project not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.get("/chapter-plans/{chapter_plan_id}")
def get_chapter_plan_detail(chapter_plan_id: str, request: Request) -> dict:
    result = get_chapter_plan(chapter_plan_id)
    if not result:
        raise HTTPException(status_code=404, detail="chapter plan not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.get("/chapter-plans/{chapter_plan_id}/section-plans")
def get_section_plan_list(chapter_plan_id: str, request: Request) -> dict:
    result = list_section_plans(chapter_plan_id)
    if not result:
        raise HTTPException(status_code=404, detail="chapter plan not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.post("/chapter-plans/{chapter_plan_id}/section-plans", status_code=202)
def post_section_plans(chapter_plan_id: str, command: CreateSectionPlansCommand, request: Request) -> dict:
    result = create_section_plans(chapter_plan_id, command.section_count, request.state.trace_id)
    if not result:
        raise HTTPException(status_code=404, detail="chapter plan not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )
