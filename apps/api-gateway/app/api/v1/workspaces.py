from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.envelope import success_envelope
from app.core.phase_two_adapter import create_workspace, get_workspace, get_workspace_home

router = APIRouter()


class CreateWorkspaceCommand(BaseModel):
    name: str
    slug: Optional[str] = None
    default_language: str = "zh-CN"


@router.post("/workspaces", status_code=201)
def post_workspace(command: CreateWorkspaceCommand, request: Request) -> dict:
    result = create_workspace(command.model_dump(exclude_none=True))
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.get("/workspaces/{workspace_id}")
def get_workspace_detail(workspace_id: str, request: Request) -> dict:
    result = get_workspace(workspace_id)
    if not result:
        raise HTTPException(status_code=404, detail="workspace not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.get("/workspaces/{workspace_id}/home")
def get_workspace_home_detail(workspace_id: str, request: Request) -> dict:
    result = get_workspace_home(workspace_id)
    if not result:
        raise HTTPException(status_code=404, detail="workspace not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )
