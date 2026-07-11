---
document_id: NF-PIPE-001
title: Book Ingestion and Extraction Pipeline
version: 1.0.0
status: Draft
category: Pipeline Specification
owner: Novel Factory Backend Architecture Team
created: 2026-07-10
updated: 2026-07-10
dependencies:
  - NFES-000
  - NF-PRD-001
  - NF-NKS-000
  - NF-NKS-001
  - NF-NKS-100
  - NF-NKS-200
  - NF-NKS-210
  - NF-NKS-220
  - NF-NKS-230
  - NF-NKS-240
  - NF-NKS-250
  - NF-NKS-260
  - NF-NKS-270
  - NF-ARCH-001
  - NF-ARCH-002
  - NF-DBS-001
  - NF-DBS-002
  - NF-AGENT-001
references:
  - docs/standards/NFES-000.md
  - docs/prd/NF-PRD-001.md
  - docs/nks/NF-NKS-000.md
  - docs/nks/NF-NKS-001.md
  - docs/nks/NF-NKS-100.md
  - docs/nks/NF-NKS-200.md
  - docs/nks/NF-NKS-210.md
  - docs/nks/NF-NKS-220.md
  - docs/nks/NF-NKS-230.md
  - docs/nks/NF-NKS-240.md
  - docs/nks/NF-NKS-250.md
  - docs/nks/NF-NKS-260.md
  - docs/nks/NF-NKS-270.md
  - docs/architecture/NF-ARCH-001.md
  - docs/architecture/NF-ARCH-002.md
  - docs/database/NF-DBS-001.md
  - docs/database/NF-DBS-002.md
  - docs/agents/NF-AGENT-001.md
---

# NF-PIPE-001

# Book Ingestion and Extraction Pipeline

# 1. Purpose and Scope

本文档定义 Novel Factory 的 Book Ingestion and Extraction Pipeline。

该 Pipeline 将原始小说输入转化为可审核、可追踪、可检索、可用于后续生成的 BookKnowledgePackage。它是从拆书到 AI 写作的第一条工程流水线。

本文档覆盖：

- 书籍导入和文件接收。
- 文本清洗、去重、章节识别和标准化。
- Chapter 和 Scene 切分。
- NF-NKS-100 定义的对象、关系、Pattern、Rhythm、Rule 和 Evidence 抽取。
- 任务状态、幂等、重试和失败恢复。
- 人工审核、导出和反馈回流。
- 可观测性和错误分类。

本文档不定义章节生成流水线、Prompt 模板正文、数据库物理表结构或具体 LLM Prompt。

# 2. Pipeline Overview

## 2.1 High Level Flow

```text
Source Submission
↓
Book Registration
↓
File Intake
↓
Text Normalization
↓
Chapter Segmentation
↓
Scene Segmentation
↓
Knowledge Extraction
↓
Evidence Binding
↓
Object Normalization
↓
Quality Review
↓
Human Review Gate
↓
BookKnowledgePackage Export
↓
Knowledge Base Commit
```

## 2.2 Pipeline Owners

| Stage                 | Owner Module            |
| --------------------- | ----------------------- |
| Source Submission     | Book Service            |
| File Intake           | Ingestion Service       |
| Text Normalization    | Ingestion Service       |
| Chapter Segmentation  | Ingestion Service       |
| Scene Segmentation    | Extraction Orchestrator |
| Knowledge Extraction  | Extraction Orchestrator |
| Evidence Binding      | Extraction Orchestrator |
| Object Normalization  | Knowledge Service       |
| Quality Review        | Review Service          |
| Package Export        | Extraction Orchestrator |
| Knowledge Base Commit | Knowledge Service       |

## 2.3 Output Contract

Pipeline 的最终输出是 BookKnowledgePackage。

BookKnowledgePackage 必须包含：

- metadata
- source_book
- chapters
- scenes
- objects
- relationships
- rhythm_profiles
- patterns
- rules
- evidence
- review_report
- export_manifest

该结构引用 NF-NKS-100，不得在 Pipeline 文档中重新定义对象权威语义。

# 3. Ingestion Stages

## 3.1 Source Submission

Source Submission 接收待拆解作品。

输入至少包含：

- title
- author
- platform
- genre
- tags
- source
- file_ref or text_ref
- submitted_by

输出：source_book candidate 和 ingestion_run。

## 3.2 Book Registration

Book Registration 创建 source_books 记录。

要求：

- 使用稳定 book_id。
- 记录 import_status。
- 记录 source metadata。
- 生成 idempotency_key，防止重复导入同一作品。

## 3.3 File Intake

File Intake 将原始文件写入 Object Storage，并在 PostgreSQL 保存 object_ref。

每个文件必须记录：

- object_ref
- checksum
- byte_size
- mime_type
- source_book_id
- uploaded_at

## 3.4 Text Normalization

Text Normalization 负责将原始文件转为 normalized_text。

处理内容：

- 编码归一化。
- 去除广告、水印、页眉和页脚。
- 保留章节标题。
- 保留段落顺序。
- 标记疑似 OCR 或排版错误。
- 生成 text_range。

不得改写正文语义。

## 3.5 Chapter Segmentation

Chapter Segmentation 识别章节边界并创建 source_chapters。

要求：

- chapter_index 必须连续。
- title 缺失时允许生成标题，但必须标记 generated_title。
- text_range 必须指向 normalized_text。
- 缺章、重复章、章节顺序异常必须进入 segmentation_report。

# 4. Extraction Stages

## 4.1 Scene Segmentation

Scene Segmentation 将 Chapter 切分为 Scene candidate。

切分依据：

- 时间变化。
- 地点变化。
- 参与角色变化。
- 叙事目标变化。
- 冲突状态变化。

输出：scene_candidates、scene_boundaries 和 segmentation_confidence。

## 4.2 Entity Extraction

Entity Extraction 抽取 Character、Faction、Location、Worldview、Power System、Artifact、Resource 和其他 NF-NKS 对象候选。

每个候选对象必须绑定 evidence_refs。

## 4.3 Event and Relationship Extraction

Event Extraction 抽取 Event、Conflict、Hook、Reward 和 Climax。

Relationship Extraction 基于已存在对象创建 Story Graph Relationship candidate。

禁止创建指向不存在对象的关系。

## 4.4 Pattern, Rhythm and Rule Extraction

Pipeline 必须抽取：

- Pattern candidate。
- Rhythm Profile。
- Rule candidate。
- Consistency constraint。
- Contradiction candidate。

这些输出分别引用 NF-NKS-240、NF-NKS-250 和 NF-NKS-270。

## 4.5 Evidence Binding

所有对象、关系、Pattern、Rhythm Profile、Rule 和抽取判断必须绑定 Evidence。

Evidence 至少包含：

- source_type
- source_id
- text_range
- source_text_excerpt_ref
- extraction_method
- confidence

## 4.6 Object Normalization

Object Normalization 负责：

- alias 合并。
- object_id 分配。
- duplicate candidate 归并。
- unresolved object 标记。
- lifecycle_status 初始化。

不确定对象不得直接进入 Approved 状态。

# 5. Task State and Idempotency

## 5.1 Pipeline Run

每次流水线执行必须创建 pipeline_run。

最小字段：

- run_id
- book_id
- pipeline_version
- requested_by
- status
- current_stage
- input_refs
- output_refs
- idempotency_key
- started_at
- finished_at

## 5.2 Stage Status

标准 stage status：

```text
pending -> running -> succeeded
pending -> skipped
running -> failed
running -> requires_review
running -> retrying -> running
```

`requires_review` 表示自动流程无法安全继续。

## 5.3 Idempotency Rule

Pipeline 必须支持幂等重试。

同一个 book_id、source checksum、pipeline_version 和 idempotency_key 的重复请求，不得创建互相冲突的 source_book、chapter、scene、object 或 package。

## 5.4 Checkpoint Rule

每个重要阶段完成后必须写入 checkpoint。

建议 checkpoint：

- file_intake_completed
- normalization_completed
- chapter_segmentation_completed
- scene_segmentation_completed
- entity_extraction_completed
- relationship_extraction_completed
- review_completed
- package_export_completed

失败恢复必须从最近安全 checkpoint 继续，而不是默认重跑全流程。

## 5.5 Retry Policy

可重试错误：

- transient_llm_provider_error
- temporary_storage_error
- queue_timeout
- projection_update_failure

不可直接重试错误：

- invalid_source_format
- missing_required_metadata
- severe_chapter_order_conflict
- evidence_binding_failure
- schema_validation_failure

不可直接重试错误必须进入人工审核或人工修复流程。

# 6. Review, Export and Feedback

## 6.1 Quality Review

Quality Review 在 BookKnowledgePackage 导出前执行。

检查内容：

- chapter coverage
- scene coverage
- object evidence coverage
- relationship validity
- unresolved object ratio
- contradiction candidates
- rhythm profile completeness
- extraction error severity

## 6.2 Human Review Gate

以下情况必须进入人工审核：

- 章节顺序存在严重冲突。
- 大量角色或地点无法归并。
- Story Graph 出现关键关系冲突。
- Rule 或 Consistency constraint 存在高严重级别矛盾。
- Quality Review 阻塞项未解决。

## 6.3 Package Export

Package Export 生成 BookKnowledgePackage 并写入 Object Storage。

PostgreSQL 必须保存：

- package_id
- book_id
- extraction_run_id
- package_ref
- checksum
- object_count
- relationship_count
- evidence_count
- validation_status
- review_status

## 6.4 Knowledge Base Commit

只有通过审核的对象和关系可以进入 Approved Knowledge Base。

Candidate 或 Reviewed 对象可以保留用于实验，但生成系统必须显式标记其来源和状态。

## 6.5 Feedback Capture

Pipeline 必须记录：

- 人工修正。
- 审核驳回原因。
- 抽取错误类别。
- 对后续 Prompt、Pattern、Rule 或 extraction rule 的改进建议。

这些信号进入 Feedback Service，用于后续优化抽取与生成质量。

# 7. Failure Recovery and Observability

## 7.1 Error Categories

Pipeline 错误至少分为：

- source_format_error
- metadata_error
- normalization_error
- segmentation_error
- extraction_error
- evidence_binding_error
- object_normalization_error
- review_blocked
- package_export_error
- storage_error
- llm_provider_error
- unknown_error

## 7.2 Recovery Actions

每个错误必须指定 recovery_action。

允许值：

- retry
- resume_from_checkpoint
- require_human_fix
- require_human_review
- skip_with_reason
- abort_pipeline

## 7.3 Observability Signals

Pipeline 必须记录：

- run_duration
- stage_duration
- queue_wait_time
- llm_call_count
- token_usage
- object_count
- relationship_count
- evidence_count
- unresolved_object_ratio
- review_blocker_count
- retry_count
- package_export_size

## 7.4 Audit Rule

所有人工修正、状态覆盖、重新导出和强制通过操作必须写入 audit_events。

Audit record 必须包含 actor、action、reason、target_type、target_id、before_ref、after_ref 和 created_at。

## 7.5 Data Retention

原始输入、标准化文本、抽取包、审核报告和导出清单必须按 NF-OPS-001 的保留策略保存。

临时中间件缓存可以过期，但必须能从 PostgreSQL checkpoint 和 Object Storage artifact 恢复。

# 8. Boundaries, References and Change Log

## 8.1 Boundaries

NF-PIPE-001 定义 Book Ingestion and Extraction Pipeline。

NF-PIPE-001 不定义章节生成流水线、Prompt 模板正文、数据库物理表结构、前端操作界面或具体 LLM Prompt。

## 8.2 References

- NFES-000
- NF-PRD-001
- NF-NKS-000
- NF-NKS-001
- NF-NKS-100
- NF-NKS-200
- NF-NKS-210
- NF-NKS-220
- NF-NKS-230
- NF-NKS-240
- NF-NKS-250
- NF-NKS-260
- NF-NKS-270
- NF-ARCH-001
- NF-ARCH-002
- NF-DBS-001
- NF-DBS-002
- NF-AGENT-001

## 8.3 Approval

Document Status: Draft

Next Review: Backend pipeline implementation review

Next Document: NF-PIPE-002 AI Generation and Revision Pipeline

## 8.4 Change Log

| Version | Date       | Author                                  | Change                                                |
| ------- | ---------- | --------------------------------------- | ----------------------------------------------------- |
| 1.0.0   | 2026-07-10 | Novel Factory Backend Architecture Team | Initial book ingestion and extraction pipeline draft. |
