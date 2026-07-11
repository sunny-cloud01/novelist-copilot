# 1. Identity and Roles

本文档定义 Novel Factory MVP 的身份、权限、服务账号、对象访问和密钥管理规则。

## 1.1 Product Assumption

Novel Factory MVP 是个人创作者平台，但仍保留 workspace 边界。workspace 用于隔离数据、配置、任务和后续可能的协作能力。

## 1.2 Actor Types

允许 actor：

| Actor           | Description                                   |
| --------------- | --------------------------------------------- |
| creator         | 个人创作者，拥有自己 workspace 的主要操作权限 |
| admin           | 本地或生产管理者，可处理配置和运维操作        |
| service_account | 服务间调用身份                                |
| system_agent    | 后台 Agent 任务身份                           |
| auditor         | 只读审计身份                                  |

## 1.3 Workspace Roles

MVP workspace role：

| Role     | Permissions                                    |
| -------- | ---------------------------------------------- |
| owner    | workspace 全权限，包括配置和删除请求           |
| creator  | 上传、生成、审核、批准章节                     |
| reviewer | 审核 knowledge、quality 和 feedback suggestion |
| viewer   | 只读查看项目、报告和图谱                       |
| service  | 后台任务执行和内部写入                         |

个人平台默认创建一个 owner 用户和一个 default workspace。
