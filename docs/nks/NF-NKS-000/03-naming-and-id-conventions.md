# 3. Naming and ID Conventions

## 3.1 Canonical Name

每个领域对象必须有唯一英文 Canonical Name。

| Chinese Name | Canonical Name        |
| ------------ | --------------------- |
| 角色         | Character             |
| 事件         | Event                 |
| 势力         | Faction               |
| 地点         | Location              |
| 伏笔         | Foreshadowing         |
| 爽点         | Reward                |
| 表达分类     | Expression Type       |
| 角色口吻     | Speaker Voice Profile |
| 风格约束     | Style Constraint      |

## 3.2 Display Name

Display Name 用于界面、人类阅读和本地化展示，不得替代 Canonical Name。

## 3.3 Alias

Alias 只用于检索、兼容旧数据或用户输入归一化。Alias 不得在正式 Schema、API 或 Prompt 参数中作为主字段使用。

## 3.4 ID Convention

推荐格式：

```text
{PREFIX}-{NUMBER}
```

Prefix 使用 3 到 6 位大写英文字母。Number 使用 6 位数字，不足补零。ID 一经发布不得复用。

| Object Type     | Prefix | Example    |
| --------------- | ------ | ---------- |
| Book            | BOK    | BOK-000001 |
| Chapter         | CHP    | CHP-000001 |
| Scene           | SCN    | SCN-000001 |
| Character       | CHR    | CHR-000001 |
| Faction         | FAC    | FAC-000001 |
| Location        | LOC    | LOC-000001 |
| Event           | EVT    | EVT-000001 |
| Pattern         | PAT    | PAT-000001 |
| Artifact        | ART    | ART-000001 |
| Foreshadowing   | FSH    | FSH-000001 |
| Rule            | RUL    | RUL-000001 |
| Prompt Template | PRM    | PRM-000001 |
| Expression Type | EXP    | EXP-000001 |
| Voice Profile   | VOI    | VOI-000001 |
