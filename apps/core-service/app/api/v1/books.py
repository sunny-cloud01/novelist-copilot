from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.envelope import success_envelope
from app.core.phase_two_store import (
    WORKSPACE_ID,
    create_book,
    get_book,
    get_book_analysis,
    get_book_source_content,
    list_book_chapters,
    list_evidence_for_book,
)

router = APIRouter()


class CreateBookCommand(BaseModel):
    title: str
    author_name: str
    source_type: str
    workspace_id: str = WORKSPACE_ID
    platform: Optional[str] = None
    genre: Optional[str] = None
    usage_boundary: Optional[str] = None
    source_text: Optional[str] = None


@router.post("/books", status_code=201)
def post_book(command: CreateBookCommand, request: Request) -> dict:
    book = create_book(command.model_dump(), request.state.trace_id)
    return success_envelope(
        data=book,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/books/{book_id}")
def get_book_detail(book_id: str, request: Request) -> dict:
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return success_envelope(
        data=book,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/books/{book_id}/chapters")
def get_book_chapter_list(book_id: str, request: Request) -> dict:
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    chapters = list_book_chapters(book_id)
    return success_envelope(
        data={"items": chapters},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/books/{book_id}/content")
def get_book_content(book_id: str, request: Request) -> dict:
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    content = get_book_source_content(book_id)
    if not content:
        raise HTTPException(status_code=404, detail="source content not found")
    return success_envelope(
        data=content,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/books/{book_id}/evidence")
def get_book_evidence(book_id: str, request: Request) -> dict:
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return success_envelope(
        data={"items": list_evidence_for_book(book_id)},
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/books/{book_id}/analysis")
def get_book_analysis_report(book_id: str, request: Request) -> dict:
    report = get_book_analysis(book_id)
    if not report:
        raise HTTPException(status_code=404, detail="book not found")
    return success_envelope(
        data=report,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
