# 1. Purpose and Build Boundary

本文档定义 Novel Factory MVP 的服务构建计划。

NF-IMPL-002 定义 MVP 交付范围。NF-IMPL-003 将该范围拆成可进入代码实现的仓库结构、服务模块、数据库迁移、API/任务契约、AI Worker、前端页面、测试与交付顺序。

## 1.1 Build Goal

构建目标：

- 建立可运行的 monorepo skeleton。
- 启动 web、api-gateway、core-service、ai-worker、scheduler。
- 通过 Docker Compose 启动 PostgreSQL、Redis、MinIO。
- 实现从 Source Import 到 Writing Studio 单章成稿的 MVP 主链路。
- 确保 trace、task、audit、object_ref、quality_report 和 feedback_record 可用。

## 1.2 Build Boundary

本文档定义实现顺序和模块契约，不定义完整业务代码、完整 DDL 或视觉设计稿。

具体实现时，应将本文档拆成开发任务或代码仓库 issue。任何偏离本文档的服务边界、表族、API envelope 或任务状态模型都必须更新 NF-IMPL-003 或对应权威规范。

## 1.3 Non-Goals

本构建计划不包含：

- 云上生产部署。
- 多租户计费。
- 发布平台接入。
- 独立图数据库或专用向量数据库。
- 全自动长篇连载。
- 大规模读者行为埋点。
