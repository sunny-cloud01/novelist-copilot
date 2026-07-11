from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.envelope import success_envelope
from app.core.phase_two_adapter import (
    get_configuration_snapshot,
    set_model_profile_enabled,
    update_agent_model_assignment,
    update_prompt_version,
    update_quality_gate_profile,
)

router = APIRouter()


class UpdateQualityGateProfileCommand(BaseModel):
    ai_flavor_threshold: float
    originality_safety_threshold: float


class UpdateAgentModelAssignmentCommand(BaseModel):
    model_profile_id: str
    max_retry: int
    max_cost: float
    enabled: bool


class UpdatePromptVersionCommand(BaseModel):
    template_ref: str


@router.get("/configuration")
def get_configuration_detail(request: Request) -> dict:
    return success_envelope(
        data=get_configuration_snapshot(),
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/model-profiles/{model_profile_id}/enable")
def post_enable_model_profile(model_profile_id: str, request: Request) -> dict:
    try:
        result = set_model_profile_enabled(
            model_profile_id,
            True,
            request.state.request_id,
            request.state.trace_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    if not result:
        raise HTTPException(status_code=404, detail="model profile not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/model-profiles/{model_profile_id}/disable")
def post_disable_model_profile(model_profile_id: str, request: Request) -> dict:
    try:
        result = set_model_profile_enabled(
            model_profile_id,
            False,
            request.state.request_id,
            request.state.trace_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    if not result:
        raise HTTPException(status_code=404, detail="model profile not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/quality-gate-profiles/{quality_gate_profile_id}")
def post_quality_gate_profile_update(quality_gate_profile_id: str, command: UpdateQualityGateProfileCommand, request: Request) -> dict:
    try:
        result = update_quality_gate_profile(
            quality_gate_profile_id,
            command.ai_flavor_threshold,
            command.originality_safety_threshold,
            request.state.request_id,
            request.state.trace_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    if not result:
        raise HTTPException(status_code=404, detail="quality gate profile not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/agent-model-assignments/{assignment_id}")
def post_agent_model_assignment_update(assignment_id: str, command: UpdateAgentModelAssignmentCommand, request: Request) -> dict:
    try:
        result = update_agent_model_assignment(
            assignment_id,
            command.model_profile_id,
            command.max_retry,
            command.max_cost,
            command.enabled,
            request.state.request_id,
            request.state.trace_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    if result is False:
        raise HTTPException(status_code=404, detail="model profile not found")
    if result is None:
        raise HTTPException(status_code=404, detail="agent model assignment not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/prompt-versions/{agent_role}")
def post_prompt_version_update(agent_role: str, command: UpdatePromptVersionCommand, request: Request) -> dict:
    try:
        result = update_prompt_version(
            agent_role,
            command.template_ref,
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
