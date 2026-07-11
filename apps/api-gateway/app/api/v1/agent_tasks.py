from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.envelope import success_envelope
from app.core.phase_two_adapter import create_agent_task, get_agent_task

router = APIRouter()


class CreateAgentTaskCommand(BaseModel):
    schema_version: int
    task_type: str
    workspace_id: str
    owner_module: str
    input_refs: list[str]
    idempotency_key: str
    trace_id: str
    requested_by: str


@router.post("/agent-tasks", status_code=202)
def post_agent_task(command: CreateAgentTaskCommand, request: Request) -> dict:
    try:
        result = create_agent_task(
            command.model_dump(),
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


@router.get("/agent-tasks/{task_id}")
def get_agent_task_detail(task_id: str, request: Request) -> dict:
    result = get_agent_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="agent task not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
