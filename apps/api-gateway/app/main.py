from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.request_context import RequestContextMiddleware

app = FastAPI(title="Novel Factory API Gateway", version="0.1.0")
app.add_middleware(RequestContextMiddleware)
app.include_router(health_router, prefix="/v1")
