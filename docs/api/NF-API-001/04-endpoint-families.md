# 4. Endpoint Families

## 4.1 Source API

负责 Book、Chapter、Scene 的导入、查询和预处理状态管理。

Representative endpoints: `POST /v1/books`, `GET /v1/books/{book_id}`, `GET /v1/books/{book_id}/chapters`, `GET /v1/chapters/{chapter_id}/scenes`。

## 4.2 Knowledge API

负责知识对象查询、候选对象管理、别名归一化和生命周期状态。

Representative endpoints: `GET /v1/knowledge-objects`, `GET /v1/knowledge-objects/{object_id}`, `POST /v1/knowledge-objects/{object_id}/review-actions`。

## 4.3 Graph API

负责 Story Graph 节点、关系和遍历查询。

Representative endpoints: `GET /v1/graph/nodes/{node_id}`, `GET /v1/graph/nodes/{node_id}/neighbors`, `POST /v1/graph/queries`。

## 4.4 Extraction API

负责抽取任务创建、状态查询、报告获取和错误记录。

Representative endpoints: `POST /v1/extraction-runs`, `GET /v1/extraction-runs/{run_id}`, `GET /v1/extraction-runs/{run_id}/report`。

## 4.5 Agent API

负责 Agent Task 创建、状态追踪、人工审核交接和结果读取。

Representative endpoints: `POST /v1/agent-tasks`, `GET /v1/agent-tasks/{task_id}`, `POST /v1/agent-tasks/{task_id}/review-actions`。

## 4.6 Prompt API

负责 Prompt Template、Prompt Package 和评估记录。

Representative endpoints: `GET /v1/prompt-templates`, `POST /v1/prompt-packages`, `GET /v1/prompt-packages/{package_id}`。

## 4.7 Generation API

负责生成请求、章节草稿、质量报告和修订请求。

Representative endpoints: `POST /v1/generation-requests`, `GET /v1/generation-requests/{request_id}`, `GET /v1/generated-chapters/{chapter_draft_id}`。

## 4.8 Feedback API

负责反馈记录、评分、排名建议和规则更新建议。

Representative endpoints: `POST /v1/feedback-records`, `GET /v1/feedback-records`, `GET /v1/rankings/prompt`。
