# NF-DBS-001 Knowledge Database Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the NF-DBS-001 Knowledge Database Specification as the canonical storage and schema baseline for Novel Factory knowledge data.

**Architecture:** The canonical database specification lives at `docs/database/NF-DBS-001.md`. Chapter source files live under `docs/database/NF-DBS-001/`. The document maps NKS objects and NKS-100 extraction packages into logical storage domains, schema groups, constraints, indexes, migrations, retention, and backup rules.

**Tech Stack:** Markdown, YAML Front Matter, shell-based validation.

## Global Constraints

- Formal Markdown files must contain only formal document content.
- NF-DBS-001 must reference NF-NKS-000 object definitions and NF-NKS-100 package rules.
- NF-DBS-001 defines schema and storage responsibilities, not API routes, Agent behavior, or Prompt templates.
- Database details must stay implementation-neutral unless the architecture requires a storage class.
- This workspace is currently not a Git repository, so commit steps are skipped until Git is initialized.

---

### Task 1: Create Database Document Structure

**Files:**

- Create: `docs/database/NF-DBS-001.md`
- Create: `docs/database/NF-DBS-001/README.md`
- Create chapter files under `docs/database/NF-DBS-001/`

**Interfaces:**

- Consumes: `docs/architecture/NF-ARCH-001.md`, `docs/nks/NF-NKS-000.md`, `docs/nks/NF-NKS-100.md`, `docs/standards/NFES-000.md`.
- Produces: Database baseline for API, Agent, Prompt, and implementation documents.

- [x] **Step 1: Create database source directory**

Run: `test -d docs/database/NF-DBS-001`

Expected: directory exists.

- [x] **Step 2: Create canonical NF-DBS-001 file**

Write a Draft v1.0.0 document with Front Matter, purpose, scope, storage principles, storage domains, logical schema groups, core tables/collections, graph model, evidence model, review model, indexing, constraints, migration, backup, boundaries, references, approval, and change log.

- [x] **Step 3: Create chapter source files**

Create focused source files for purpose, principles, storage domains, schema groups, object storage, graph storage, evidence/review, indexing/constraints, migration/backup, and change log.

### Task 2: Validate Database Baseline

**Files:**

- Read: `docs/database/NF-DBS-001.md`
- Read: `docs/database/NF-DBS-001/*.md`

**Interfaces:**

- Consumes: Task 1 outputs.
- Produces: Validated NF-DBS-001 baseline.

- [x] **Step 1: Validate front matter**

Run: `sed -n '1,30p' docs/database/NF-DBS-001.md`

Expected: output starts with YAML Front Matter and includes `document_id: NF-DBS-001`.

- [x] **Step 2: Validate source chapters**

Run: `find docs/database/NF-DBS-001 -type f | sort`

Expected: source files cover purpose, principles, domains, schema groups, object storage, graph storage, evidence/review, indexes, migrations, backup, and change log.

- [x] **Step 3: Check placeholders**

Run: `grep -R -n "TBD\|TODO\|待补充" docs/database/NF-DBS-001.md docs/database/NF-DBS-001 || true`

Expected: no unresolved placeholder lines.
