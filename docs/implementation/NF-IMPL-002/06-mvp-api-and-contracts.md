# 6. MVP API and Contracts

## 6.1 API Principles

MVP API 必须遵守 NF-API-001 的 envelope、trace、idempotency 和 error model。

所有 mutation 请求必须支持 request_id 和 trace_id。创建任务类请求必须支持 idempotency_key。

## 6.2 Required Endpoint Families

MVP endpoint families：

| Family     | Required Endpoints                                                               |
| ---------- | -------------------------------------------------------------------------------- |
| Workspace  | POST /v1/workspaces, GET /v1/workspaces/{workspace_id}                           |
| Source     | POST /v1/books, GET /v1/books, GET /v1/books/{book_id}/chapters                  |
| Task       | GET /v1/tasks/{task_id}, GET /v1/tasks/{task_id}/events                          |
| Extraction | POST /v1/extraction-runs, GET /v1/extraction-runs/{run_id}                       |
| Knowledge  | GET /v1/knowledge-objects, POST /v1/knowledge-objects/{object_id}/review-actions |
| Graph      | GET /v1/graph/nodes/{node_id}, GET /v1/graph/nodes/{node_id}/neighbors           |
| Project    | POST /v1/novel-projects, GET /v1/novel-projects/{project_id}                     |
| Planning   | POST /v1/chapter-plans, POST /v1/chapter-plans/{chapter_plan_id}/section-plans   |
| Writing    | POST /v1/writing-runs, GET /v1/writing-runs/{writing_run_id}                     |
| Quality    | GET /v1/quality-reports/{quality_report_id}                                      |
| Feedback   | POST /v1/feedback-records, GET /v1/feedback-records                              |
| Config     | GET /v1/model-profiles, GET /v1/quality-thresholds                               |

## 6.3 Standard Task Response

创建长任务的 API 必须返回：

```json
{
  "data": {
    "task_id": "TASK-000001",
    "status": "queued",
    "resource_ref": "writing_run:WR-000001"
  },
  "meta": {
    "request_id": "REQ-000001",
    "trace_id": "TRC-000001"
  },
  "errors": []
}
```

## 6.4 Review Action Contract

Review action 必须包含：

- action_type
- target_ref
- reason
- reviewer_id
- expected_next_state

允许 action_type：

- approve
- reject
- request_change
- merge_alias
- request_reextract
- accept_section
- accept_chapter
- request_rewrite
- edit_and_accept
- block_generation

## 6.5 Error Contract

MVP 必须实现以下错误码：

- validation_error
- authentication_error
- authorization_error
- not_found
- conflict
- lifecycle_violation
- dependency_error
- rate_limited
- internal_error
