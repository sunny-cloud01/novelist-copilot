from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.envelope import success_envelope
from app.core.phase_two_store import commit_knowledge_package, create_extraction_run, get_extraction_report, get_extraction_run

router = APIRouter()


class CreateExtractionRunCommand(BaseModel):
    book_id: str


@router.post("/extraction-runs", status_code=202)
def post_extraction_run(command: CreateExtractionRunCommand, request: Request) -> dict:
    run = create_extraction_run(command.book_id, request.state.trace_id)
    return success_envelope(
        data=run,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
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
    )
