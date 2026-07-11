# NF-NKS-000 Glossary Domain Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the NF-NKS-000 Glossary & Domain Model v2.0 document as the canonical terminology and domain object source for Novel Factory.

**Architecture:** The canonical NKS file lives at `docs/nks/NF-NKS-000.md`. Chapter source files live under `docs/nks/NF-NKS-000/` so later updates can modify focused sections without editing a long RFC-style file.

**Tech Stack:** Markdown, YAML Front Matter, shell-based validation.

## Global Constraints

- Formal Markdown files must contain only formal document content.
- NF-NKS-000 is the single source of truth for Novel Factory domain terms.
- Other documents may reference NF-NKS-000 definitions but must not redefine them.
- The previous root-level `NF-NKS-000` draft is not present in the current workspace, so this version is derived from NFES-000, NF-PRD-001, and recovered session context.
- This workspace is currently not a Git repository, so commit steps are skipped until Git is initialized.

---

### Task 1: Create NKS Document Structure

**Files:**

- Create: `docs/nks/NF-NKS-000.md`
- Create: `docs/nks/NF-NKS-000/README.md`
- Create chapter files under `docs/nks/NF-NKS-000/`

**Interfaces:**

- Consumes: `docs/standards/NFES-000.md`, `docs/prd/NF-PRD-001.md`.
- Produces: Canonical terminology and domain object definitions for NKS-100, ARCH, DBS, AGENT, and PROMPT documents.

- [x] **Step 1: Create NKS source directory**

Run: `test -d docs/nks/NF-NKS-000`

Expected: directory exists.

- [x] **Step 2: Create canonical NF-NKS-000 file**

Write a Draft v2.0.0 document with Front Matter, purpose, principles, naming rules, glossary, domain object definitions, relationship model, ID rules, boundaries, references, approval, and change log.

- [x] **Step 3: Create chapter source files**

Create focused source files for purpose, principles, naming, glossary, domain objects, relationships, lifecycle, boundaries, and change log.

### Task 2: Validate NKS Baseline

**Files:**

- Read: `docs/nks/NF-NKS-000.md`
- Read: `docs/nks/NF-NKS-000/*.md`

**Interfaces:**

- Consumes: Task 1 outputs.
- Produces: Validated NKS v2.0.0 baseline.

- [x] **Step 1: Validate front matter**

Run: `sed -n '1,24p' docs/nks/NF-NKS-000.md`

Expected: output starts with YAML Front Matter and includes `document_id: NF-NKS-000`.

- [x] **Step 2: Validate source chapters**

Run: `find docs/nks/NF-NKS-000 -type f | sort`

Expected: source files cover purpose, principles, naming, glossary, domain objects, relationships, lifecycle, boundaries, and change log.

- [x] **Step 3: Check placeholders**

Run: `grep -R -n "TBD\|TODO\|待补充" docs/nks || true`

Expected: no unresolved placeholder lines.
