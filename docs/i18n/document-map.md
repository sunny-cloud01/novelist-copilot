# Bilingual Document Map

This map pairs canonical Novel Factory documents with their English companion metadata.

## Status Legend

- `canonical`: primary maintained specification.
- `companion-summary`: companion navigation or summary exists, not a full translation.
- `needs-translation`: companion content should be added later.
- `in-review`: translation exists and is under review.
- `aligned`: bilingual versions are semantically aligned.
- `outdated`: companion content needs update.

## Document Map

| Document ID   | Chinese / Canonical Path             | English Title                                             | Companion Status  |
| ------------- | ------------------------------------ | --------------------------------------------------------- | ----------------- |
| NFES-000      | `docs/standards/NFES-000.md`         | Novel Factory Documentation Standard                      | companion-summary |
| NF-PRD-001    | `docs/prd/NF-PRD-001.md`             | Product Overview                                          | companion-summary |
| NF-NKS-000    | `docs/nks/NF-NKS-000.md`             | Glossary and Domain Model                                 | companion-summary |
| NF-NKS-001    | `docs/nks/NF-NKS-001.md`             | Novel Knowledge Specification Map                         | companion-summary |
| NF-NKS-100    | `docs/nks/NF-NKS-100.md`             | Book Knowledge Extraction Specification                   | companion-summary |
| NF-NKS-200    | `docs/nks/NF-NKS-200.md`             | Story Graph Model Specification                           | companion-summary |
| NF-NKS-210    | `docs/nks/NF-NKS-210.md`             | Character and Relationship Knowledge Specification        | companion-summary |
| NF-NKS-220    | `docs/nks/NF-NKS-220.md`             | Worldview Location Faction and Power System Specification | companion-summary |
| NF-NKS-230    | `docs/nks/NF-NKS-230.md`             | Event Conflict Hook Reward and Climax Specification       | companion-summary |
| NF-NKS-240    | `docs/nks/NF-NKS-240.md`             | Pattern Library Specification                             | companion-summary |
| NF-NKS-250    | `docs/nks/NF-NKS-250.md`             | Rhythm Profile Specification                              | companion-summary |
| NF-NKS-260    | `docs/nks/NF-NKS-260.md`             | Asset Library Specification                               | companion-summary |
| NF-NKS-270    | `docs/nks/NF-NKS-270.md`             | Rule and Consistency Knowledge Specification              | companion-summary |
| NF-NKS-280    | `docs/nks/NF-NKS-280.md`             | Speech Expression and Style Taxonomy Specification        | companion-summary |
| NF-NKS-290    | `docs/nks/NF-NKS-290.md`             | Feedback Knowledge Specification                          | companion-summary |
| NF-ARCH-001   | `docs/architecture/NF-ARCH-001.md`   | System Architecture                                       | companion-summary |
| NF-ARCH-002   | `docs/architecture/NF-ARCH-002.md`   | Backend Technical Architecture                            | companion-summary |
| NF-DBS-001    | `docs/database/NF-DBS-001.md`        | Knowledge Database Specification                          | companion-summary |
| NF-DBS-002    | `docs/database/NF-DBS-002.md`        | Physical Database and Storage Selection                   | companion-summary |
| NF-PIPE-001   | `docs/pipeline/NF-PIPE-001.md`       | Book Ingestion and Extraction Pipeline                    | companion-summary |
| NF-PIPE-002   | `docs/pipeline/NF-PIPE-002.md`       | AI Generation and Revision Pipeline                       | companion-summary |
| NF-PIPE-003   | `docs/pipeline/NF-PIPE-003.md`       | Novel Writing Orchestration and Humanization Pipeline     | companion-summary |
| NF-AGENT-001  | `docs/agents/NF-AGENT-001.md`        | Agent Collaboration Model                                 | companion-summary |
| NF-PROMPT-001 | `docs/prompts/NF-PROMPT-001.md`      | Prompt Template Specification                             | companion-summary |
| NF-PROMPT-002 | `docs/prompts/NF-PROMPT-002.md`      | Writing Prompt Pack Specification                         | companion-summary |
| NF-RAG-001    | `docs/rag/NF-RAG-001.md`             | Knowledge Retrieval and Memory Context Specification      | companion-summary |
| NF-QA-001     | `docs/quality/NF-QA-001.md`          | Writing Quality Gate Specification                        | companion-summary |
| NF-IMPL-001   | `docs/implementation/NF-IMPL-001.md` | Product-Level Implementation Blueprint                    | companion-summary |
| NF-IMPL-002   | `docs/implementation/NF-IMPL-002.md` | MVP Delivery Plan                                         | companion-summary |
| NF-IMPL-003   | `docs/implementation/NF-IMPL-003.md` | Service Build Plan                                        | companion-summary |
| NF-API-001    | `docs/api/NF-API-001.md`             | Platform API Specification                                | companion-summary |
| NF-OPS-001    | `docs/operations/NF-OPS-001.md`      | Operations Specification                                  | companion-summary |
| NF-ADR-001    | `docs/adr/NF-ADR-001.md`             | Documentation Project Architecture Decision               | companion-summary |

## English Abstracts

### NFES-000

Defines the documentation engineering standard, document lifecycle, naming, structure and source-chapter build convention.

### NF-PRD-001

Defines the Novel Factory product vision, user-facing modules, knowledge engineering position and generation pipeline requirements.

### NF-NKS Series

Defines Novel Knowledge Engineering objects, extraction flow, Story Graph, character knowledge, worldview knowledge, event and reader-experience knowledge, pattern library, rhythm profile, asset library, consistency rules, speech expression taxonomy and feedback knowledge.

### NF-ARCH Series

Defines system architecture and backend technical architecture. The current baseline is microservice-oriented, container-based, and uses React, TypeScript, pnpm, shadcn/ui, NestJS or FastAPI, Python AI services, PostgreSQL with pgvector, Redis and MinIO.

### NF-DBS Series

Defines logical and physical database architecture, including PostgreSQL as system of record, pgvector, object storage, Redis, projection stores, ownership, migration and consistency rules.

### NF-PIPE Series

Defines book ingestion, extraction, AI generation, beat-by-beat writing orchestration, humanization, revision, review, feedback, memory retrieval and quality-gated writing pipelines.

### NF-AGENT, NF-PROMPT, NF-API and NF-OPS

Define agent collaboration, prompt templates, writing prompt packs, platform APIs and operations requirements.

### NF-RAG and NF-QA

Define retrieval memory context, Memory Package assembly, staleness rules, writing quality scores, humanization gates and low-AI-flavor checks.

### NF-IMPL Series

Defines product-level implementation blueprints, user journey, service runtime topology, traceability, labor control, MVP scope, delivery slices, service build plan and phased delivery.

### NF-ADR-001

Records the documentation project architecture decision and source-chapter based build approach.

## Terminology Alignment

| Chinese Term   | English Term                         | Canonical Source |
| -------------- | ------------------------------------ | ---------------- |
| 小说工厂       | Novel Factory                        | NF-NKS-000       |
| 小说知识工程   | Novel Knowledge Engineering          | NF-NKS-000       |
| 作品库         | Book Library                         | NF-ARCH-001      |
| 拆书           | Book Analysis / Knowledge Extraction | NF-NKS-100       |
| 知识库         | Knowledge Base                       | NF-NKS-000       |
| 故事图谱       | Story Graph                          | NF-NKS-200       |
| 套路库         | Pattern Library                      | NF-NKS-240       |
| 节奏模型       | Rhythm Profile                       | NF-NKS-250       |
| 素材库         | Asset Library                        | NF-NKS-260       |
| 统一话术分类   | Speech Expression and Style Taxonomy | NF-NKS-280       |
| 反馈知识       | Feedback Knowledge                   | NF-NKS-290       |
| 记忆上下文     | Memory Context                       | NF-RAG-001       |
| 质量门禁       | Quality Gate                         | NF-QA-001        |
| 实现蓝图       | Implementation Blueprint             | NF-IMPL-001      |
| 规则引擎       | Consistency Engine / Rule Knowledge  | NF-NKS-270       |
| 反馈闭环       | Feedback Loop                        | NF-ARCH-001      |
| 微服务导向架构 | Microservice-oriented Architecture   | NF-ARCH-002      |
| 人类化改写     | Humanization                         | NF-PIPE-003      |
| 情节点         | Beat                                 | NF-PIPE-003      |
