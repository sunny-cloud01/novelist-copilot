from fastapi import APIRouter, HTTPException, Request

from app.core.envelope import success_envelope
from app.core.phase_two_adapter import BOOK_ID, get_graph_node, get_graph_summary, list_graph_neighbors

router = APIRouter()


@router.get("/graph/summary")
def get_graph_summary_view(request: Request, book_id: str = BOOK_ID) -> dict:
    summary = get_graph_summary(book_id)
    return success_envelope(
        data=summary,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/graph/nodes/{node_id}")
def get_graph_node_view(node_id: str, request: Request) -> dict:
    node = get_graph_node(node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="graph node not found")
    return success_envelope(
        data=node,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )


@router.get("/graph/nodes/{node_id}/neighbors")
def get_graph_neighbors_view(node_id: str, request: Request) -> dict:
    neighbors = list_graph_neighbors(node_id)
    if neighbors is None:
        raise HTTPException(status_code=404, detail="graph node not found")
    return success_envelope(
        data=neighbors,
        request_id=request.state.request_id,
        trace_id=request.state.trace_id,
        workspace_id=request.state.workspace_id,
        actor_id=request.state.actor_id,
        actor_role=request.state.actor_role,
    )
