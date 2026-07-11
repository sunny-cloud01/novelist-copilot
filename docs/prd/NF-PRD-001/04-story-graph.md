# 4. Story Graph

Story Graph 是 Novel Factory 的核心数据结构和辅助查看界面。

在 MVP 中，Story Graph 主要用于检索、解释、证据追踪和关系查看，不作为 Creator 的默认重编辑画布。关系修正应优先通过异常处理、重新抽取或知识包修订完成。

## 4.1 Node Types

节点类型：

- Character
- Location
- Event
- Artifact
- Faction
- Rule
- Resource
- Foreshadowing

## 4.2 Relationship Types

关系类型：

- Character belongs_to Faction
- Character owns Artifact
- Event occurs_at Location
- Character hates Character
- Event causes Event
- Foreshadowing resolves_at Chapter

## 4.3 Query Requirement

所有节点必须支持 AI 实时查询，并在 NF-NKS 系列文档中获得稳定定义。Creator-facing 图谱界面必须支持搜索节点、查看节点详情、查看关系来源、查看 evidence_refs 和跳转原文证据。
