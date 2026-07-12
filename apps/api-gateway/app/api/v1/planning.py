from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional

from app.core.envelope import success_envelope
from app.core.phase_two_adapter import (
    WORKSPACE_ID,
    create_asset,
    create_chapter_plan,
    create_pattern,
    create_rhythm_profile,
    create_section_plans,
    get_asset,
    get_chapter_plan,
    get_pattern,
    get_rhythm_profile,
    list_assets,
    list_patterns,
    list_rhythm_profiles,
    list_section_plans,
)

router = APIRouter()


class CreateChapterPlanCommand(BaseModel):
    project_id: str
    chapter_index: int
    target_word_count: int
    workspace_id: str = WORKSPACE_ID
    payload: dict = Field(default_factory=dict)


class CreateSectionPlansCommand(BaseModel):
    section_count: int = Field(default=4, ge=1, le=4)


class CreatePatternCommand(BaseModel):
    canonical_name: str
    pattern_type: str
    status: str = "draft"
    intent: str
    preconditions: list[str]
    steps: list[dict]
    slots: list[str]
    expected_reader_effect: str
    compatible_rhythm_profile_id: Optional[str] = None
    evidence_refs: list[str]
    workspace_id: str = WORKSPACE_ID


class CreateRhythmProfileCommand(BaseModel):
    target_id: str
    status: str = "draft"
    label: str
    climax_index: float
    conflict_index: float
    dialogue_ratio: float
    description_ratio: float
    battle_ratio: float
    information_density: float
    suspense_index: float
    reward_count: int
    emotion_curve: list[dict]
    workspace_id: str = WORKSPACE_ID


class CreateAssetCommand(BaseModel):
    asset_type: str
    canonical_name: str
    status: str = "draft"
    content_summary: str
    style_tags: list[str]
    genre_scope: str
    usage_context: str
    constraints: list[str]
    expression_type_refs: list[str]
    source_refs: list[str]
    evidence_refs: list[str]
    quality_score: float
    workspace_id: str = WORKSPACE_ID


@router.post("/chapter-plans", status_code=202)
def post_chapter_plan(command: CreateChapterPlanCommand, request: Request) -> dict:
    try:
        result = create_chapter_plan(
            command.model_dump(),
            request.state.trace_id,
            request.state.request_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    if not result:
        raise HTTPException(status_code=404, detail="novel project not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
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
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
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
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/chapter-plans/{chapter_plan_id}/section-plans", status_code=202)
def post_section_plans(chapter_plan_id: str, command: CreateSectionPlansCommand, request: Request) -> dict:
    try:
        result = create_section_plans(
            chapter_plan_id,
            command.section_count,
            request.state.trace_id,
            request.state.request_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    if not result:
        raise HTTPException(status_code=404, detail="chapter plan not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/patterns")
def get_patterns(request: Request, status: Optional[str] = None, patternType: Optional[str] = None) -> dict:
    return success_envelope(
        data={"items": list_patterns(status, patternType)},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/patterns", status_code=201)
def post_pattern(command: CreatePatternCommand, request: Request) -> dict:
    try:
        result = create_pattern(
            command.model_dump(exclude_none=True),
            request.state.request_id,
            request.state.trace_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/patterns/{pattern_id}")
def get_pattern_detail(pattern_id: str, request: Request) -> dict:
    result = get_pattern(pattern_id)
    if not result:
        raise HTTPException(status_code=404, detail="pattern not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/rhythm-profiles")
def get_rhythm_profiles(request: Request, status: Optional[str] = None, targetId: Optional[str] = None) -> dict:
    return success_envelope(
        data={"items": list_rhythm_profiles(status, targetId)},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/rhythm-profiles", status_code=201)
def post_rhythm_profile(command: CreateRhythmProfileCommand, request: Request) -> dict:
    try:
        result = create_rhythm_profile(
            command.model_dump(exclude_none=True),
            request.state.request_id,
            request.state.trace_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/rhythm-profiles/{rhythm_profile_id}")
def get_rhythm_profile_detail(rhythm_profile_id: str, request: Request) -> dict:
    result = get_rhythm_profile(rhythm_profile_id)
    if not result:
        raise HTTPException(status_code=404, detail="rhythm profile not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/assets")
def get_assets(request: Request, status: Optional[str] = None, assetType: Optional[str] = None) -> dict:
    return success_envelope(
        data={"items": list_assets(status, assetType)},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/assets", status_code=201)
def post_asset(command: CreateAssetCommand, request: Request) -> dict:
    try:
        result = create_asset(
            command.model_dump(exclude_none=True),
            request.state.request_id,
            request.state.trace_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/assets/{asset_id}")
def get_asset_detail(asset_id: str, request: Request) -> dict:
    result = get_asset(asset_id)
    if not result:
        raise HTTPException(status_code=404, detail="asset not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
