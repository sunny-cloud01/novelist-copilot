# Novel Factory 中文文档入口

本文档是 Novel Factory 文档工程的中文阅读入口。

## 定位

- 中文文档用于承载完整业务语义、领域定义、知识工程细节和实现决策。
- 当前 `docs/{category}/{document-id}.md` 仍是 canonical reading version。
- 对应 source chapters 位于 `docs/{category}/{document-id}/`。
- 英文文档用于提供国际化协作、技术摘要、术语对照和跨团队沟通入口。

## 推荐阅读顺序

1. `../standards/NFES-000.md` - 文档工程标准。
2. `../prd/NF-PRD-001.md` - 产品定位和模块边界。
3. `../nks/NF-NKS-000.md` - 术语和领域模型。
4. `../nks/NF-NKS-001.md` - NKS 文档地图。
5. `../architecture/NF-ARCH-001.md` - 系统架构。
6. `../architecture/NF-ARCH-002.md` - 后端技术架构。
7. `../database/NF-DBS-002.md` - 物理数据库和存储选型。
8. `../pipeline/NF-PIPE-001.md` - 拆书导入与抽取流水线。
9. `../pipeline/NF-PIPE-002.md` - AI 生成与修订流水线。
10. `../pipeline/NF-PIPE-003.md` - 小说写作编排与人类化流水线。
11. `../implementation/NF-IMPL-001.md` - 产品级实现蓝图。

## 目录分工

| Directory            | Purpose            |
| -------------------- | ------------------ |
| `../standards/`      | 文档标准           |
| `../prd/`            | 产品需求和产品架构 |
| `../nks/`            | 小说知识工程规范   |
| `../architecture/`   | 系统和技术架构     |
| `../database/`       | 数据库和存储规范   |
| `../pipeline/`       | 业务流水线规范     |
| `../agents/`         | Agent 协作规范     |
| `../prompts/`        | Prompt 工程规范    |
| `../api/`            | API 规范           |
| `../implementation/` | 产品级实现蓝图     |
| `../operations/`     | 运维规范           |
| `../adr/`            | 架构决策记录       |
| `../i18n/`           | 双语维护规则和映射 |

## 维护规则

中文 canonical 文档更新后，应同步检查 `../i18n/document-map.md` 中的英文摘要和术语是否需要更新。
