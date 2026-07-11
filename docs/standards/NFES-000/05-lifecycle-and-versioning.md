# 5. Lifecycle and Versioning

## 5.1 Lifecycle

所有正式文档必须经历：

```text
Draft
↓
Review
↓
Approved
↓
Frozen
↓
Deprecated
```

Draft 表示设计阶段，允许修改，不可作为生产依据。

Review 表示完成初稿，等待评审。

Approved 表示正式版本，可以被其他文档和开发任务引用。

Frozen 表示稳定版本，修改必须提交 Change Request。

Deprecated 表示废弃版本，保留历史记录，不再作为新开发依据。

## 5.2 Versioning

采用 Semantic Versioning：

```text
Major.Minor.Patch
```

Major 用于重大架构变化或不兼容修改。

Minor 用于新增功能、章节或向后兼容扩展。

Patch 用于错误修正、措辞修正或格式修正。
