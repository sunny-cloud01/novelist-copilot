from fastapi import APIRouter, Request

from app.core.envelope import success_envelope
from app.core.runtime_settings import load_runtime_settings

router = APIRouter()


@router.get("/health")
def get_health(request: Request) -> dict:
    settings = load_runtime_settings()
    return success_envelope(
        data={
            "service": "core-service",
            "status": "ok",
            "runtime": {
                "postgres_url": settings.postgres_url,
                "redis_url": settings.redis_url,
                "minio_endpoint": settings.minio_endpoint,
                "minio_bucket": settings.minio_bucket,
            },
        },
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
