# Novel Factory English Documentation Entry

This directory provides the English companion entry for the Novel Factory documentation project.

## Positioning

- The detailed canonical specifications currently live under `docs/{category}/{document-id}.md`.
- Chinese documents carry the full domain meaning and implementation decisions.
- English companion documents provide technical summaries, terminology alignment, document navigation, and cross-team communication support.
- Translation status and document pairing are tracked in `../i18n/document-map.md`.

## Recommended Reading Order

1. `../standards/NFES-000.md` - Documentation engineering standard.
2. `../prd/NF-PRD-001.md` - Product overview and module boundaries.
3. `../nks/NF-NKS-000.md` - Glossary and domain model.
4. `../nks/NF-NKS-001.md` - Novel Knowledge Specification map.
5. `../architecture/NF-ARCH-001.md` - System architecture.
6. `../architecture/NF-ARCH-002.md` - Backend technical architecture.
7. `../database/NF-DBS-002.md` - Physical database and storage selection.
8. `../pipeline/NF-PIPE-001.md` - Book ingestion and extraction pipeline.
9. `../pipeline/NF-PIPE-002.md` - AI generation and revision pipeline.
10. `../pipeline/NF-PIPE-003.md` - Novel writing orchestration and humanization pipeline.
11. `../implementation/NF-IMPL-001.md` - Product-level implementation blueprint.

## Current Technical Baseline

- Frontend: React, TypeScript, pnpm, shadcn/ui preferred.
- Backend: microservice-oriented architecture.
- API Gateway / BFF: NestJS or FastAPI.
- AI and knowledge services: Python FastAPI and worker services.
- Infrastructure: Docker Compose for local development, PostgreSQL with pgvector, Redis, MinIO or S3-compatible object storage.

## Directory Responsibilities

| Directory            | Purpose                                       |
| -------------------- | --------------------------------------------- |
| `../standards/`      | Documentation standards                       |
| `../prd/`            | Product requirements and product architecture |
| `../nks/`            | Novel Knowledge Engineering specifications    |
| `../architecture/`   | System and technical architecture             |
| `../database/`       | Database and storage specifications           |
| `../pipeline/`       | Business pipeline specifications              |
| `../agents/`         | Agent collaboration specifications            |
| `../prompts/`        | Prompt engineering specifications             |
| `../api/`            | API specifications                            |
| `../implementation/` | Product-level implementation blueprints       |
| `../operations/`     | Operations specifications                     |
| `../adr/`            | Architecture decision records                 |
| `../i18n/`           | Bilingual maintenance rules and mapping       |

## Maintenance Rule

When a canonical Chinese-heavy document changes, update `../i18n/document-map.md` if its English title, abstract, terminology, or translation status changes.
