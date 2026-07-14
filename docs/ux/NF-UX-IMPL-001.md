---
document_id: NF-UX-IMPL-001
title: Missing Pages Implementation Plan
version: 1.0.0
status: Active
category: UX Implementation
owner: Novel Factory Development Team
created: 2026-07-14
updated: 2026-07-14
---

# NF-UX-IMPL-001: 缺失页面补充实现方案

## 问题分析

根据 NF-UX-001 (Creator Interaction Flow Specification) 的定义，当前平台实现缺失以下关键页面，导致两条主线（知识工程线和创作线）的详情页面和交互流程不完整。

### 两条主线及缺失情况

**Line 1：知识工程线（Source/Knowledge Branch）**

| Page                         | UX Spec | Current Status           | Issue                        |
| ---------------------------- | ------- | ------------------------ | ---------------------------- |
| Upload Source Book           | 3.3     | ✓ SourceLibraryPage      | 正常                         |
| Auto Analyze Book            | 3.4     | ✓ BookAnalysisCenterPage | 正常                         |
| Extraction Run Detail        | 3.4     | ✓ ExtractionRunPage      | 正常                         |
| Knowledge Review             | 3.5     | ✓ KnowledgeReviewPage    | 正常                         |
| **Knowledge Package Detail** | 3.5     | ✗ MISSING                | 无查看已落库知识包的详情页面 |
| Story Graph View             | 3.5     | ✓ GraphPage              | 正常但缺少从知识包的入口     |

**Line 2：创作线（Writing/Project Branch）**

| Page                        | UX Spec | Current Status                | Issue                         |
| --------------------------- | ------- | ----------------------------- | ----------------------------- |
| Create Novel Project        | 4.1     | ✓ StoryBibleWizardPage        | 正常                          |
| Story Bible Review          | 4.1     | ✗ EMBEDDED IN ProjectHomePage | 不是独立页面                  |
| **Chapter Direction Setup** | 4.2     | ✗ MISSING                     | 无章节目标输入和确认页面      |
| **Writing Run Detail**      | 4.3     | ✗ MISSING                     | WritingStudioPage存在但不清晰 |
| **Quality Review**          | 4.4     | ✗ MISSING                     | 无阻塞问题和质量审查页面      |
| **Chapter Approval**        | 4.5     | ✗ MISSING                     | 无最终章节批准页面            |

### 入口问题（Navigation Issues）

1. **Knowledge Package 无入口**：从 ExtractionRunPage 无法跳转到查看已落库知识包
2. **Story Bible 评审不清晰**：审核流程嵌入在 ProjectHomePage，缺少独立评审页面
3. **Chapter Setup 缺失**：PlannerPage 后没有章节方向确认的页面
4. **Writing Run 状态不清**：未能清晰显示一键生成的进度和内部 Scene/Beat 状态
5. **Quality Review 无入口**：写作完成后没有质量审查页面
6. **Approval 无实现**：没有最终批准章节的页面和流程

## 补充方案

### 1. Knowledge Package Detail Page

**Route:** `/knowledge-packages/:packageId`

**Purpose:** 查看已提交知识包的详细内容，包括：

- 包基本信息（来源、版本、创建时间）
- 抽取统计（章节数、场景数、对象数、证据数）
- 知识对象浏览（角色、地点、事件、势力等）
- 故事图谱联动查看
- 证据来源追踪

**Import Location:** [apps/web/src/features/knowledge/knowledge-package-detail-page.tsx](apps/web/src/features/knowledge/knowledge-package-detail-page.tsx)

**Route Registration:** router.tsx

```typescript
{ path: "knowledge-packages/:packageId", element: <KnowledgePackageDetailPage /> }
```

**Entry Points:**

- From ExtractionRunPage: "查看知识包" button
- From KnowledgeReviewPage: 审核完成后跳转
- From Knowledge Home: 列表点击

---

### 2. Story Bible Review Page (Standalone)

**Route:** `/projects/:projectId/story-bible/review`

**Purpose:** Story Bible 候选版本的独立审核页面，而不是嵌入在 ProjectHomePage

**Current Location:** Embedded in ProjectHomePage
**New Location:** [apps/web/src/features/projects/story-bible-review-page.tsx](apps/web/src/features/projects/story-bible-review-page.tsx)

**Route Registration:** router.tsx

```typescript
{ path: "projects/:projectId/story-bible/review", element: <StoryBibleReviewPage /> }
```

**Entry Points:**

- From ProjectHomePage: "进入故事圣经评审" button
- From StoryBibleWizardPage: 生成 Story Bible 后直接跳转

---

### 3. Chapter Direction Setup Page

**Route:** `/projects/:projectId/chapters/:chapterIndex/setup`

**Purpose:** 为每一章设置生成参数：

- chapter_goal：本章目标描述
- target_word_count：目标字数
- main_conflict：主要冲突
- reward_or_hook：爽点或钩子
- emotional_direction：情感走向
- must_include：必须包含的内容
- must_not_change：禁止改变的内容

**Import Location:** [apps/web/src/features/projects/chapter-direction-setup-page.tsx](apps/web/src/features/projects/chapter-direction-setup-page.tsx)

**Route Registration:** router.tsx

```typescript
{ path: "projects/:projectId/chapters/:chapterIndex/setup", element: <ChapterDirectionSetupPage /> }
```

**Entry Points:**

- From PlannerPage: 每个章节的 "设置章节参数" button
- From WritingStudioPage 返回后重新编辑

---

### 4. Writing Run Detail Page

**Route:** `/projects/:projectId/writing-runs/:writingRunId`

**Purpose:** 查看一键生成的进度和状态：

- writing_run_status（running, completed, blocked）
- 内部 pipeline 进度（Memory Package, Prompt Package, Writer Draft, Critic, Humanizer, Quality Gate）
- Memory Package 和 Prompt Package 的具体内容
- 实时日志和事件流
- 草稿内容预览

**Import Location:** [apps/web/src/features/projects/writing-run-detail-page.tsx](apps/web/src/features/projects/writing-run-detail-page.tsx)

**Route Registration:** router.tsx

```typescript
{ path: "projects/:projectId/writing-runs/:writingRunId", element: <WritingRunDetailPage /> }
```

**Update WritingStudioPage:** 重新定义为写作工作台的入口，包括：

- 待生成的章节列表
- 进行中的 writing run 列表
- 已完成的草稿列表

---

### 5. Quality Review Page (Blocking Issues & Review)

**Route:** `/projects/:projectId/writing-runs/:writingRunId/quality-review`

**Purpose:** 处理阻塞问题和质量审查：

- 按类型展示 Quality Gate 报告（blocking, warning, suggestion, passed）
- 每个 blocking issue 显示：
  - 错误描述
  - 冲突证据
  - 修复建议
  - 重新生成或局部修改的选项
- 批量处理或逐项处理选项

**Import Location:** [apps/web/src/features/review/quality-review-page.tsx](apps/web/src/features/review/quality-review-page.tsx)

**Route Registration:** router.tsx

```typescript
{ path: "projects/:projectId/writing-runs/:writingRunId/quality-review", element: <QualityReviewPage /> }
```

**Entry Points:**

- From WritingRunDetailPage: Quality Gate 部分点击查看详情
- 自动跳转：当 writing run 完成且有 blocking issues 时

---

### 6. Chapter Approval Page

**Route:** `/projects/:projectId/writing-runs/:writingRunId/approval`

**Purpose:** 最终章节批准：

- 展示最终章节内容
- 显示所有警告和建议（可被忽略）
- 记录批准者、时间、审核结果
- 输入反馈备注（用于反馈循环优化）
- Approve 按钮进入正式 manuscript

**Import Location:** [apps/web/src/features/review/chapter-approval-page.tsx](apps/web/src/features/review/chapter-approval-page.tsx)

**Route Registration:** router.tsx

```typescript
{ path: "projects/:projectId/writing-runs/:writingRunId/approval", element: <ChapterApprovalPage /> }
```

**Entry Points:**

- From QualityReviewPage: 所有 blocking issues 处理完后
- 自动跳转：当可以批准时

---

## 路由更新

### apps/web/src/router.tsx - 新增路由

```typescript
// Knowledge Line
{ path: "knowledge-packages/:packageId", element: <KnowledgePackageDetailPage /> },

// Writing Line - Story Bible
{ path: "projects/:projectId/story-bible/review", element: <StoryBibleReviewPage /> },

// Writing Line - Chapter Setup & Writing
{ path: "projects/:projectId/chapters/:chapterIndex/setup", element: <ChapterDirectionSetupPage /> },
{ path: "projects/:projectId/writing-runs/:writingRunId", element: <WritingRunDetailPage /> },

// Writing Line - Quality & Approval
{ path: "projects/:projectId/writing-runs/:writingRunId/quality-review", element: <QualityReviewPage /> },
{ path: "projects/:projectId/writing-runs/:writingRunId/approval", element: <ChapterApprovalPage /> },
```

## 页面导航流程图

### Knowledge Line Flow

```text
SourceLibraryPage
       ↓
Upload Source → BookAnalysisCenterPage
                       ↓
                ExtractionRunPage
                       ↓
                KnowledgeReviewPage
                       ↓
            ✨ KnowledgePackageDetailPage (NEW)
                       ↓
                  GraphPage (可选查看)
```

### Writing Line Flow

```text
StoryBibleWizardPage
       ↓
Create Project → ProjectHomePage
                       ↓
            ✨ StoryBibleReviewPage (NEW)
                       ↓
               PlannerPage
                       ↓
        ✨ ChapterDirectionSetupPage (NEW)
                       ↓
            ✨ WritingRunDetailPage (NEW)
                       ↓
        ✨ QualityReviewPage (NEW)
                       ↓
        ✨ ChapterApprovalPage (NEW)
                       ↓
               正式 Manuscript
```

## 相关数据结构和 API

### Knowledge Package Detail API

```
GET /api/knowledge-packages/{packageId}
  → PackageDetailResponse {
      package_id: string
      source_ref: string
      status: "committed" | "draft"
      extraction_run_id: string
      created_at: string
      chapter_count: number
      scene_count: number
      object_count: number
      evidence_count: number
      objects: KnowledgeObject[]
      statistics: ExtractionStatistics
    }
```

### Writing Run Detail API

```
GET /api/writing-runs/{writingRunId}
  → WritingRunDetailResponse {
      writing_run_id: string
      project_id: string
      chapter_index: number
      status: "queued" | "running" | "completed" | "blocked"
      started_at: string
      completed_at?: string
      chapter_plan: ChapterPlan
      pipeline_stages: PipelineStage[]
      draft_content: string
      quality_report: QualityReport
      memory_package: MemoryPackage
      prompt_package: PromptPackage
    }
```

### Quality Review API

```
GET /api/projects/{projectId}/writing-runs/{writingRunId}/quality-report
  → QualityReportResponse {
      report_id: string
      writing_run_id: string
      passed: boolean
      issues: QualityIssue[] {
        issue_id: string
        type: "blocking" | "warning" | "suggestion"
        title: string
        description: string
        evidence: string
        suggested_fix?: string
        affected_section?: TextRange
      }
      summary: {
        total_issues: number
        blocking_count: number
        warning_count: number
        suggestion_count: number
      }
    }
```

## 实现优先级

1. **P0 - Critical Path**
   - KnowledgePackageDetailPage
   - ChapterDirectionSetupPage
   - WritingRunDetailPage
   - QualityReviewPage
   - ChapterApprovalPage

2. **P1 - Important**
   - StoryBibleReviewPage (standalone)
   - 路由和导航更新

3. **P2 - Enhancement**
   - 进度指示和可视化
   - 详细的日志查看
   - 高级过滤和搜索

## 实现验收标准

### Knowledge Line

- [ ] 可从 ExtractionRunPage 进入 KnowledgePackageDetailPage
- [ ] 知识包详情显示完整的对象列表和统计
- [ ] 可从知识包详情跳转到 GraphPage 查看关系
- [ ] 证据链可追踪到原始文本

### Writing Line

- [ ] 可独立进入 StoryBibleReviewPage
- [ ] 可为每章设置 ChapterDirectionSetupPage
- [ ] WritingRunDetailPage 实时显示生成进度
- [ ] QualityReviewPage 清晰展示和处理阻塞问题
- [ ] ChapterApprovalPage 完整记录审批信息

### Navigation

- [ ] 所有页面之间的导航链接正确
- [ ] 返回上一步的导航正确
- [ ] URL 参数正确传递
- [ ] 面包屑导航准确

## 参考资源

- NF-UX-001: Creator Interaction Flow Specification
- NF-PRD-001: Product Overview
- Current Router: [apps/web/src/router.tsx](apps/web/src/router.tsx)
- Pages Module: [apps/web/src/pages.tsx](apps/web/src/pages.tsx)
