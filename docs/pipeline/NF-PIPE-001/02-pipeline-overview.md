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
