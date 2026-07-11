# 2. Required Contracts

## 2.1 API Envelope

All endpoints must use the NF-API-001 envelope.

Response schema names：

- `ApiSuccessEnvelope`
- `ApiErrorEnvelope`
- `ApiError`
- `RequestMeta`

Required meta fields：

- request_id
- trace_id

## 2.2 Task Contracts

Required schemas：

- `Task`
- `TaskEvent`
- `CreateTaskCommand`
- `WorkerCommand`
- `WorkerResult`
- `TaskStatus`

`TaskStatus` enum values：

```text
queued
running
retrying
succeeded
failed
cancelled
requires_review
blocked
```

## 2.3 Domain Resource Contracts

MVP must define schemas for：

- Workspace
- SourceBook
- SourceChapter
- ExtractionRun
- KnowledgeObject
- EvidenceRecord
- GraphNode
- GraphEdge
- NovelProject
- StoryBible
- ChapterPlan
- SectionPlan
- WritingRun
- SectionRun
- ChapterDraft
- ReviewReport
- QualityReport
- FeedbackRecord
- ModelProfile
- AgentModelAssignment

## 2.4 Review Action Contract

Review action enum：

```text
approve
reject
request_change
merge_alias
request_reextract
accept_section
accept_chapter
request_rewrite
edit_and_accept
block_generation
```

`accept_beat` is not an external API action. Beat may remain an internal planning concept inside `SectionPlan.payload`.
