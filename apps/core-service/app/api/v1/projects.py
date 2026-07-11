from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.envelope import success_envelope
from app.core.phase_two_store import WORKSPACE_ID, create_novel_project, get_novel_project

router = APIRouter()


class CreateNovelProjectCommand(BaseModel):
    title: str
    genre_scope: str
    workspace_id: str = WORKSPACE_ID
    quality_gate_profile_id: Optional[str] = None
    allowed_knowledge_source_refs: Optional[list[str]] = None
    story_bible_payload: Optional[dict] = None


@router.post("/novel-projects", status_code=202)
def post_novel_project(command: CreateNovelProjectCommand, request: Request) -> dict:
    try:
        project = create_novel_project(
            command.model_dump(exclude_none=True),
            request.state.trace_id,
            request.state.request_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return success_envelope(
        data=project,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/novel-projects/{project_id}")
def get_novel_project_detail(project_id: str, request: Request) -> dict:
    project = get_novel_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="novel project not found")
    return success_envelope(
        data=project,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
