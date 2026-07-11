# 7. Frontend Build Plan

## 7.1 Frontend Stack

Frontend must use:

- React
- TypeScript
- pnpm
- shadcn/ui preferred for common components

The MVP frontend is a working tool surface, not a marketing site.

## 7.2 Route Groups

MVP route groups:

```text
/workspaces/:workspaceId
/sources
/sources/:bookId
/extraction-runs/:runId
/knowledge/review
/graph
/projects
/projects/:projectId
/projects/:projectId/planner
/projects/:projectId/writing/:writingRunId
/feedback
/configuration
```

## 7.3 Shared UI Components

Shared components:

- AppShell
- WorkspaceSwitcher
- TaskStatusBadge
- TraceLinkList
- ReviewActionPanel
- EvidencePanel
- QualityScorePanel
- CostMetricPanel
- SectionList
- DraftDiffViewer

## 7.4 Page Data Rule

Pages must read state from API responses and task status. Frontend must not invent lifecycle state locally.

Long-running operations should show task progress, latest task event, retry_count and next required action.

## 7.5 Writing Studio Minimum Behavior

Writing Studio must allow:

- selecting a section or viewing internal Beat plan details.
- starting a writing_run.
- viewing Memory Package summary.
- viewing Writer output.
- viewing Critic issues.
- accepting Humanizer output.
- running chapter assembly.
- viewing Quality Gate result.
- submitting human review action.

## 7.6 Frontend Test Scope

MVP frontend tests should cover:

- task status rendering.
- review action form validation.
- Writing Studio state transitions.
- quality score panel thresholds.
- trace link rendering.
