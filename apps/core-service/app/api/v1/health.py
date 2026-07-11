from fastapi import APIRouter, Request

from app.core.envelope import success_envelope

router = APIRouter()


@router.get("/health")
def get_health(request: Request) -> dict:
    return success_envelope(
        data={"service": "core-service", "status": "ok"},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )
