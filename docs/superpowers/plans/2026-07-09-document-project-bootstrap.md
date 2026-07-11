# Document Project Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap the Novel Factory documentation project and land the first formal PRD document.

**Architecture:** Documentation is managed as source. Canonical reading files live at the category root, and long documents also have chapter source directories for incremental maintenance.

**Tech Stack:** Markdown, YAML Front Matter, shell-based validation.

## Global Constraints

- Formal Markdown files must contain only formal document content.
- Every canonical document must include Front Matter metadata.
- Document IDs must remain stable.
- Discussion records belong in chat or review notes, not in canonical documents.
- This workspace is currently not a Git repository, so commit steps are skipped until Git is initialized.

---

### Task 1: Create Documentation Project Skeleton

**Files:**

- Create: `README.md`
- Create directories: `docs/standards`, `docs/prd`, `docs/nks`, `docs/adr`, `docs/architecture`, `docs/database`, `docs/agents`, `docs/prompts`, `docs/operations`

**Interfaces:**

- Consumes: Existing `prod.md`, `docs/standard/NFES-000.md`, `NF-NKS-000`, `NF-NKS-100`.
- Produces: Stable directory layout for future documents.

- [x] **Step 1: Create directory skeleton**

Run: `find docs -maxdepth 2 -type d | sort`

Expected: category directories exist under `docs/`.

- [x] **Step 2: Create project README**

Write `README.md` with canonical document links and current milestone sequence.

- [x] **Step 3: Validate project entry point**

Run: `test -f README.md && grep -n "Milestone 1" README.md`

Expected: command prints the milestone heading line.

### Task 2: Clean and Chapterize NFES-000

**Files:**

- Create: `docs/standards/NFES-000.md`
- Create: `docs/standards/NFES-000/README.md`
- Create chapter files under `docs/standards/NFES-000/`

**Interfaces:**

- Consumes: Existing `docs/standard/NFES-000.md` and shared discussion agreement.
- Produces: Canonical documentation standard used by later PRD and NKS documents.

- [x] **Step 1: Create canonical NFES file**

Write a complete Draft v1.0.0 standard with Front Matter, rules, repository structure, and change log.

- [x] **Step 2: Create NFES chapter source files**

Split major sections into purpose, scope, principles, classification, lifecycle, authoring rules, repository structure, approval, and change log.

- [x] **Step 3: Validate NFES front matter**

Run: `sed -n '1,20p' docs/standards/NFES-000.md`

Expected: output starts and ends the YAML Front Matter block with `---`.

### Task 3: Generate NF-PRD-001 Product Overview

**Files:**

- Create: `docs/prd/NF-PRD-001.md`
- Create: `docs/prd/NF-PRD-001/README.md`
- Create chapter files under `docs/prd/NF-PRD-001/`

**Interfaces:**

- Consumes: Existing `prod.md`.
- Produces: Formal product overview used by NKS, architecture, database, agent, and prompt specifications.

- [x] **Step 1: Create canonical PRD file**

Write a Draft v2.0.0 product overview with Front Matter, product vision, system architecture, modules, Story Graph, AI generation pipeline, roadmap, positioning, references, and change log.

- [x] **Step 2: Create PRD chapter source files**

Split the PRD into focused source chapters for incremental editing.

- [x] **Step 3: Validate PRD source coverage**

Run: `find docs/prd/NF-PRD-001 -type f | sort`

Expected: source files cover vision, architecture, modules, Story Graph, generation pipeline, roadmap, positioning, and change log.

### Task 4: Workspace Validation

**Files:**

- Read: all created Markdown files.

**Interfaces:**

- Consumes: Tasks 1-3 outputs.
- Produces: A validated first milestone baseline.

- [x] **Step 1: List Markdown files**

Run: `find . -path './.git' -prune -o -name '*.md' -print | sort`

Expected: canonical and chapter documents are listed.

- [x] **Step 2: Check formal document metadata**

Run: `grep -R "^document_id:" docs/standards docs/prd`

Expected: canonical NFES and PRD files expose document IDs.

- [x] **Step 3: Check for obvious placeholder markers**

Run: `grep -R -n "TBD\|TODO\|待补充" docs/standards docs/prd || true`

Expected: no unresolved placeholder lines in the new formal documents.
