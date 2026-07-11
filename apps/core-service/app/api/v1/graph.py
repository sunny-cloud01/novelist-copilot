from fastapi import APIRouter, Request

from app.core.envelope import success_envelope
from app.core.phase_two_store import BOOK_ID, get_graph_summary

router = APIRouter()


@router.get("/graph/summary")
def get_graph_summary_view(request: Request, book_id: str = BOOK_ID) -> dict:
    summary = get_graph_summary(book_id)
    return success_envelope(
        data=summary,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
    )
