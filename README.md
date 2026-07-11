# Novel Factory Documentation Project

Novel Factory Documentation Project is the formal documentation workspace for the Novel Factory system.

This repository follows NFES-000 and treats documentation as maintainable source code:

- Formal documents are written in Markdown.
- Each document has stable metadata and a document ID.
- Long specifications are split into chapter files for maintenance.
- Aggregated documents provide the canonical reading version.
- Discussion notes are not mixed into formal Markdown documents.

## Language Editions

- [docs/zh-CN/README.md](docs/zh-CN/README.md) - 中文文档入口和推荐阅读顺序。
- [docs/en-US/README.md](docs/en-US/README.md) - English companion entry and technical baseline summary.
- [docs/i18n/README.md](docs/i18n/README.md) - Bilingual documentation policy.
- [docs/i18n/document-map.md](docs/i18n/document-map.md) - Bilingual document map, English abstracts and terminology alignment.

The existing `docs/{category}/{document-id}.md` files remain the canonical reading versions. The language entry directories provide navigation, abstracts and translation governance without breaking the source-chapter build workflow.

## Canonical Documents

- `docs/standards/NFES-000.md` - Novel Factory Documentation Standard
- `docs/prd/NF-PRD-001.md` - Product Overview
- `docs/nks/NF-NKS-000.md` - Glossary and Domain Model
- `docs/nks/NF-NKS-001.md` - Novel Knowledge Specification Map
- `docs/nks/NF-NKS-100.md` - Book Knowledge Extraction Specification
- `docs/nks/NF-NKS-200.md` - Story Graph Model Specification
- `docs/nks/NF-NKS-210.md` - Character and Relationship Knowledge Specification
- `docs/nks/NF-NKS-220.md` - Worldview Location Faction and Power System Specification
- `docs/nks/NF-NKS-230.md` - Event Conflict Hook Reward and Climax Specification
- `docs/nks/NF-NKS-240.md` - Pattern Library Specification
- `docs/nks/NF-NKS-250.md` - Rhythm Profile Specification
- `docs/nks/NF-NKS-260.md` - Asset Library Specification
- `docs/nks/NF-NKS-270.md` - Rule and Consistency Knowledge Specification
- `docs/nks/NF-NKS-280.md` - Speech Expression and Style Taxonomy Specification
- `docs/nks/NF-NKS-290.md` - Feedback Knowledge Specification
- `docs/architecture/NF-ARCH-001.md` - System Architecture
- `docs/architecture/NF-ARCH-002.md` - Backend Technical Architecture
- `docs/database/NF-DBS-001.md` - Knowledge Database Specification
- `docs/database/NF-DBS-002.md` - Physical Database and Storage Selection
- `docs/pipeline/NF-PIPE-001.md` - Book Ingestion and Extraction Pipeline
- `docs/pipeline/NF-PIPE-002.md` - AI Generation and Revision Pipeline
- `docs/pipeline/NF-PIPE-003.md` - Novel Writing Orchestration and Humanization Pipeline
- `docs/agents/NF-AGENT-001.md` - Agent Collaboration Model
- `docs/prompts/NF-PROMPT-001.md` - Prompt Template Specification
- `docs/prompts/NF-PROMPT-002.md` - Writing Prompt Pack Specification
- `docs/rag/NF-RAG-001.md` - Knowledge Retrieval and Memory Context Specification
- `docs/quality/NF-QA-001.md` - Writing Quality Gate Specification
- `docs/implementation/NF-IMPL-001.md` - Product-Level Implementation Blueprint
- `docs/implementation/NF-IMPL-002.md` - MVP Delivery Plan
- `docs/implementation/NF-IMPL-003.md` - Service Build Plan
- `docs/api/NF-API-001.md` - Platform API Specification
- `docs/operations/NF-OPS-001.md` - Operations Specification
- `docs/adr/NF-ADR-001.md` - Documentation Project Architecture Decision

## Source Structure

```text
docs/
├── zh-CN/
├── en-US/
├── i18n/
├── standards/
│   └── NFES-000/
├── prd/
│   └── NF-PRD-001/
├── nks/
├── adr/
├── architecture/
├── database/
├── pipeline/
├── api/
├── agents/
├── prompts/
├── rag/
├── quality/
├── implementation/
└── operations/
```

## Scripts

Documentation scripts live in `scripts/` and use only the Python standard library.

- `python scripts/build_docs.py --list` lists canonical documents that have matching source chapter directories.
- `python scripts/build_docs.py --check` compares canonical documents with generated output from source chapters and reports drift.
- `python scripts/build_docs.py --write` regenerates canonical documents from source chapters.

Use `--document DOC-ID` to limit any command to a single document, for example:

```sh
python scripts/build_docs.py --check --document NF-NKS-100
```

`--write` updates canonical Markdown files in place. Run `--check` first and review differences before writing generated output.

## Current Milestone

Milestone 1: Documentation Refactoring

- Step 1: NFES-000 Documentation Standard
- Step 2: NF-PRD-001 Product Overview v2.0
- Step 3: NF-NKS-000 Glossary & Domain Model v2.0
- Step 4: NF-NKS-100 Book Knowledge Extraction Specification

Milestone 2: Architecture and Implementation Baseline

- Step 1: NF-ARCH-001 System Architecture
- Step 2: NF-DBS-001 Knowledge Database Specification
- Step 3: NF-AGENT-001 Agent Collaboration Model
- Step 4: NF-PROMPT-001 Prompt Template Specification

Milestone 3: Platform Interface and Operations Baseline

- Step 1: NF-API-001 Platform API Specification
- Step 2: NF-OPS-001 Operations Specification
- Step 3: NF-ADR-001 Document Project Architecture Decision

Milestone 4: NKS Module Completion

- Step 1: NF-NKS-001 Novel Knowledge Specification Map
- Step 2: NF-NKS-200 Story Graph Model Specification
- Step 3: NF-NKS-210 Character and Relationship Knowledge Specification
- Step 4: NF-NKS-220 Worldview Location Faction and Power System Specification
- Step 5: NF-NKS-230 Event Conflict Hook Reward and Climax Specification
- Step 6: NF-NKS-240 Pattern Library Specification
- Step 7: NF-NKS-250 Rhythm Profile Specification
- Step 8: NF-NKS-260 Asset Library Specification
- Step 9: NF-NKS-270 Rule and Consistency Knowledge Specification
- Step 10: NF-NKS-280 Speech Expression and Style Taxonomy Specification
- Step 11: NF-NKS-290 Feedback Knowledge Specification

Milestone 5: Technical Implementation Baseline

- Step 1: NF-DBS-002 Physical Database and Storage Selection
- Step 2: NF-ARCH-002 Backend Technical Architecture
- Step 3: NF-PIPE-001 Book Ingestion and Extraction Pipeline
- Step 4: NF-PIPE-002 AI Generation and Revision Pipeline
- Step 5: NF-PIPE-003 Novel Writing Orchestration and Humanization Pipeline

Milestone 6: Writing Closure and Quality Baseline

- Step 1: NF-NKS-290 Feedback Knowledge Specification
- Step 2: NF-RAG-001 Knowledge Retrieval and Memory Context Specification
- Step 3: NF-PROMPT-002 Writing Prompt Pack Specification
- Step 4: NF-QA-001 Writing Quality Gate Specification

Milestone 7: Product-Level Implementation Blueprint

- Step 1: NF-IMPL-001 Product-Level Implementation Blueprint
- Step 2: NF-IMPL-002 MVP Delivery Plan
- Step 3: NF-IMPL-003 Service Build Plan

## Implementation Bootstrap

```sh
pnpm install
python -m pip install -e apps/api-gateway -e apps/core-service -e apps/ai-worker -e apps/scheduler pytest
Docker compose -f infra/docker-compose.yml up -d
pnpm contracts:lint
pnpm contracts:test
pytest -q
pnpm --filter @novel-factory/web dev
```

For shell environments that require the newer CLI spelling, the equivalent command is `docker compose -f infra/docker-compose.yml up -d`.
