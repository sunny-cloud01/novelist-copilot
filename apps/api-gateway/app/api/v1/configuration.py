from fastapi import APIRouter, HTTPException, Request

from app.core.envelope import success_envelope
from app.core.phase_two_adapter import get_configuration_snapshot, set_model_profile_enabled

router = APIRouter()


@router.get("/configuration")
def get_configuration_detail(request: Request) -> dict:
    return success_envelope(
        data=get_configuration_snapshot(),
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.post("/model-profiles/{model_profile_id}/enable")
def post_enable_model_profile(model_profile_id: str, request: Request) -> dict:
    result = set_model_profile_enabled(model_profile_id, True)
    if not result:
        raise HTTPException(status_code=404, detail="model profile not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )


@router.post("/model-profiles/{model_profile_id}/disable")
def post_disable_model_profile(model_profile_id: str, request: Request) -> dict:
    result = set_model_profile_enabled(model_profile_id, False)
    if not result:
        raise HTTPException(status_code=404, detail="model profile not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )
