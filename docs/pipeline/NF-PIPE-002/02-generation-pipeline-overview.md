# 2. Generation Pipeline Overview

## 2.1 High Level Flow

```text
Generation Request
↓
Context Retrieval
↓
Chapter Planning
↓
Prompt Assembly
↓
Draft Generation
↓
Consistency Review
↓
Revision Run
↓
AI Quality Review
↓
Human Review Gate
↓
Approved Draft or Revision Request
↓
Feedback Capture
```

## 2.2 Pipeline Owners

| Stage              | Owner Module            |
| ------------------ | ----------------------- |
| Generation Request | Generation Service      |
| Context Retrieval  | Retrieval Service       |
| Chapter Planning   | Planning Service        |
| Prompt Assembly    | Prompt Assembly Service |
| Draft Generation   | Generation Service      |
| Consistency Review | Consistency Service     |
| Revision Run       | Generation Service      |
| AI Quality Review  | Review Service          |
| Human Review Gate  | Review Service          |
| Feedback Capture   | Feedback Service        |

## 2.3 Input Contract

Generation Request 至少包含：

- request_id
- target_book_or_project_id
- generation_scope
- genre
- chapter_goal
- current_story_state_refs
- required_character_refs
- required_world_refs
- required_pattern_refs
- rhythm_target
- forbidden_changes
- requester

## 2.4 Output Contract

Pipeline 输出至少包含：

- chapter_plan
- prompt_package_ref
- draft_candidate_ref
- consistency_report
- revision_report
- quality_report
- human_review_report
- feedback_records
- final_draft_ref or rejection_reason
