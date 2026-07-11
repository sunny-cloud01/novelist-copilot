# Remaining Core Documents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the remaining core Novel Factory documentation categories defined by NFES-000.

**Architecture:** Each remaining document has a canonical Markdown file plus chapter source files. AGENT, PROMPT, API, OPS, and ADR documents reference PRD, NKS, ARCH, and DBS documents without redefining their owned concepts.

**Tech Stack:** Markdown, YAML Front Matter, shell-based validation.

## Global Constraints

- Formal Markdown files must contain only formal document content.
- Each canonical document must include Front Matter and a stable document_id.
- Long specifications must have chapter source directories.
- Documents must respect ownership boundaries from NFES-000 and NF-ARCH-001.
- This workspace is currently not a Git repository, so commit steps are skipped until Git is initialized.

---

### Task 1: NF-AGENT-001 Agent Collaboration Model

**Files:**

- Create: `docs/agents/NF-AGENT-001.md`
- Create: `docs/agents/NF-AGENT-001/README.md`
- Create chapter files under `docs/agents/NF-AGENT-001/`

- [x] Create canonical and chapter source files.
- [x] Validate front matter, source chapters, and placeholders.

### Task 2: NF-PROMPT-001 Prompt Template Specification

**Files:**

- Create: `docs/prompts/NF-PROMPT-001.md`
- Create: `docs/prompts/NF-PROMPT-001/README.md`
- Create chapter files under `docs/prompts/NF-PROMPT-001/`

- [x] Create canonical and chapter source files.
- [x] Validate front matter, source chapters, and placeholders.

### Task 3: NF-API-001 Platform API Specification

**Files:**

- Create: `docs/api/NF-API-001.md`
- Create: `docs/api/NF-API-001/README.md`
- Create chapter files under `docs/api/NF-API-001/`

- [x] Create canonical and chapter source files.
- [x] Validate front matter, source chapters, and placeholders.

### Task 4: NF-OPS-001 Operations Specification

**Files:**

- Create: `docs/operations/NF-OPS-001.md`
- Create: `docs/operations/NF-OPS-001/README.md`
- Create chapter files under `docs/operations/NF-OPS-001/`

- [x] Create canonical and chapter source files.
- [x] Validate front matter, source chapters, and placeholders.

### Task 5: NF-ADR-001 Document Project Architecture Decision

**Files:**

- Create: `docs/adr/NF-ADR-001.md`
- Create: `docs/adr/NF-ADR-001/README.md`
- Create chapter files under `docs/adr/NF-ADR-001/`

- [x] Create canonical and chapter source files.
- [x] Validate front matter, source chapters, and placeholders.

### Task 6: Repository Index Update

**Files:**

- Modify: `README.md`

- [x] Register all new canonical documents.
- [x] Add Milestone 3 completion list.
- [x] Run final document ID and placeholder checks.
