# NF-NKS-100 Book Knowledge Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the NF-NKS-100 Book Knowledge Extraction Specification as the canonical process standard for extracting structured knowledge from novels.

**Architecture:** The canonical specification lives at `docs/nks/NF-NKS-100.md`. Chapter source files live under `docs/nks/NF-NKS-100/`. The document references object definitions from `NF-NKS-000` and focuses on extraction inputs, pipeline stages, outputs, validation, and quality gates.

**Tech Stack:** Markdown, YAML Front Matter, shell-based validation.

## Global Constraints

- Formal Markdown files must contain only formal document content.
- NF-NKS-100 must reference NF-NKS-000 object definitions and must not redefine those objects.
- Extraction stages must be expressed as deterministic process requirements where possible.
- Output objects must preserve source evidence and traceability.
- This workspace is currently not a Git repository, so commit steps are skipped until Git is initialized.

---

### Task 1: Create NKS-100 Document Structure

**Files:**

- Create: `docs/nks/NF-NKS-100.md`
- Create: `docs/nks/NF-NKS-100/README.md`
- Create chapter files under `docs/nks/NF-NKS-100/`

**Interfaces:**

- Consumes: `docs/nks/NF-NKS-000.md`, `docs/prd/NF-PRD-001.md`, `docs/standards/NFES-000.md`.
- Produces: Extraction process rules for future DBS, AGENT, PROMPT, and pipeline implementation documents.

- [x] **Step 1: Create NKS-100 source directory**

Run: `test -d docs/nks/NF-NKS-100`

Expected: directory exists.

- [x] **Step 2: Create canonical NF-NKS-100 file**

Write a Draft v1.0.0 document with Front Matter, purpose, scope, inputs, extraction pipeline, stage specifications, output package, validation rules, quality gates, error handling, boundaries, references, approval, and change log.

- [x] **Step 3: Create chapter source files**

Create focused source files for purpose, inputs, pipeline, stage specs, output package, validation, quality gates, error handling, boundaries, and change log.

### Task 2: Validate NKS-100 Baseline

**Files:**

- Read: `docs/nks/NF-NKS-100.md`
- Read: `docs/nks/NF-NKS-100/*.md`

**Interfaces:**

- Consumes: Task 1 outputs.
- Produces: Validated NKS-100 baseline.

- [x] **Step 1: Validate front matter**

Run: `sed -n '1,28p' docs/nks/NF-NKS-100.md`

Expected: output starts with YAML Front Matter and includes `document_id: NF-NKS-100`.

- [x] **Step 2: Validate source chapters**

Run: `find docs/nks/NF-NKS-100 -type f | sort`

Expected: source files cover purpose, inputs, pipeline, stages, outputs, validation, quality gates, error handling, boundaries, and change log.

- [x] **Step 3: Check placeholders**

Run: `grep -R -n "TBD\|TODO\|待补充" docs/nks/NF-NKS-100.md docs/nks/NF-NKS-100 || true`

Expected: no unresolved placeholder lines.
