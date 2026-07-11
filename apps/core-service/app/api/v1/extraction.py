from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.envelope import success_envelope
from app.core.phase_two_store import commit_knowledge_package, create_extraction_run, get_extraction_report, get_extraction_run

router = APIRouter()


class CreateExtractionRunCommand(BaseModel):
    book_id: str


@router.post("/extraction-runs", status_code=202)
def post_extraction_run(command: CreateExtractionRunCommand, request: Request) -> dict:
    try:
        run = create_extraction_run(
            command.book_id,
            request.state.trace_id,
            request.state.request_id,
            request.state.actor_id,
            request.state.actor_role,
            request.state.workspace_id,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return success_envelope(
        data=run,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/extraction-runs/{run_id}")
def get_extraction_run_detail(run_id: str, request: Request) -> dict:
    run = get_extraction_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="extraction run not found")
    return success_envelope(
        data=run,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/extraction-runs/{run_id}/report")
def get_extraction_run_report(run_id: str, request: Request) -> dict:
    report = get_extraction_report(run_id)
    if not report:
        raise HTTPException(status_code=404, detail="extraction run not found")
    return success_envelope(
        data=report,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.post("/extraction-runs/{run_id}/commit")
def post_commit_knowledge_package(run_id: str, request: Request) -> dict:
    result = commit_knowledge_package(run_id)
    if not result:
        raise HTTPException(status_code=404, detail="extraction run not found")
    return success_envelope(
        data=result,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
