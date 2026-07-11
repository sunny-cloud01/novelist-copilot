# 10. Deployment View

Initial deployment is microservice-oriented and container-based.

Recommended baseline:

```text
Docker Compose Development Stack
├── Frontend Web App: React + TypeScript + pnpm + shadcn/ui
├── API Gateway / BFF: NestJS or FastAPI
├── Book and Ingestion Service
├── Knowledge and Story Graph Service
├── Retrieval and Planning Service
├── Prompt and Generation Service
├── Consistency and Review Service
├── Feedback Service
├── Worker Services
└── Scheduler Service

Storage Backends
├── PostgreSQL + pgvector
├── Redis
├── MinIO or S3-compatible Object Storage
├── Graph Projection Store when needed
└── Vector/Search Projection Store when needed

External Services
├── LLM Provider
├── OCR Provider
└── Publishing or Export Tools
```

Each service must be packaged as a Docker image or Docker Compose service. Local development must run through Docker Compose or equivalent container orchestration.

The architecture may start with a small number of backend services, but service boundaries, database ownership and events must follow microservice contracts from the beginning.
