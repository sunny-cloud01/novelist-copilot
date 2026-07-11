# 2. Operations Principles

## 2.1 Traceable Operations

所有生产环境变更必须可追踪到 operator、change_id、timestamp 和 rollback_strategy。

## 2.2 Backup Before Risky Change

高风险迁移、数据回填、批量删除、索引重建和模型切换前必须确认备份或恢复点。

## 2.3 Observability First

所有核心流水线必须具备基本指标、日志和错误追踪。

## 2.4 Human Approval for Production

生产发布、数据修正和 Approved/Frozen 文档相关变更必须有人审查。

## 2.5 Degraded Operation

外部 LLM、OCR、向量索引或图数据库异常时，系统应支持降级运行或停止高风险任务。
