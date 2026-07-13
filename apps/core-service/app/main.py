from fastapi import FastAPI

from app.api.v1.agent_tasks import router as agent_tasks_router
from app.api.v1.audit import router as audit_router
from app.api.v1.books import router as books_router
from app.api.v1.configuration import router as configuration_router
from app.api.v1.extraction import router as extraction_router
from app.api.v1.evidence import router as evidence_router
from app.api.v1.graph import router as graph_router
from app.api.v1.health import router as health_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.planning import router as planning_router
from app.api.v1.projects import router as projects_router
from app.api.v1.workspaces import router as workspaces_router
from app.api.v1.writing import router as writing_router
from app.core.request_context import RequestContextMiddleware

app = FastAPI(title="Novel Factory Core Service", version="0.1.0")
app.add_middleware(RequestContextMiddleware)
app.include_router(health_router, prefix="/v1")
app.include_router(audit_router, prefix="/v1")
app.include_router(books_router, prefix="/v1")
app.include_router(extraction_router, prefix="/v1")
app.include_router(evidence_router, prefix="/v1")
app.include_router(knowledge_router, prefix="/v1")
app.include_router(graph_router, prefix="/v1")
app.include_router(projects_router, prefix="/v1")
app.include_router(workspaces_router, prefix="/v1")
app.include_router(planning_router, prefix="/v1")
app.include_router(configuration_router, prefix="/v1")
app.include_router(writing_router, prefix="/v1")
app.include_router(agent_tasks_router, prefix="/v1")
