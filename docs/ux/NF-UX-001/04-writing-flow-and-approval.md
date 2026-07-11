# 4. Writing Flow and Approval

## 4.1 Story Bible Generation

新书世界观默认由 AI 生成草稿。

Creator 输入：

- genre。
- desired_tone。
- protagonist preference。
- originality boundary。
- allowed knowledge sources。
- forbidden similarities。

系统输出 Story Bible Draft：

- world rules。
- power system。
- factions。
- protagonist and core cast。
- main conflict。
- volume direction。
- style target。
- forbidden changes。

Creator 操作：

- Confirm。
- Regenerate section。
- Edit key field。
- Reject and retry。

## 4.2 Chapter Setup

章节生成前，Creator 不需要设计完整 Scene 或 Beat。

Creator 只需确认：

- chapter_goal。
- target_word_count，默认约 3000。
- main_conflict。
- reward_or_hook。
- emotional direction。
- must_include。
- must_not_change。

系统内部生成 chapter_plan、scene_plan 和 beat_plan。

## 4.3 One-Click Chapter Generation

主按钮为 Generate Chapter。

系统内部执行：

```text
Assemble Memory Package
↓
Assemble Prompt Package
↓
Generate Chapter Draft by internal sections
↓
Run Critic
↓
Auto Rewrite Blocked Sections
↓
Run Humanizer
↓
Assemble Chapter
↓
Run Quality Gate
```

UI 对 Creator 展示为一个 writing_run，而不是多个必须手动推进的 Beat run。

## 4.4 Quality Review

Quality Review 应将问题分为：

| Type       | UI Behavior             |
| ---------- | ----------------------- |
| blocking   | 必须处理后才能 approve  |
| warning    | 可忽略但记录到 approval |
| suggestion | 可选采纳                |
| passed     | 只展示摘要              |

Blocking issue 包括：

- 世界观冲突。
- 人物状态冲突。
- 关键证据缺失。
- 原创性风险。
- AI 味超阈值。
- 字数严重偏离。
- 章节目标未完成。

## 4.5 Approval

Final Chapter Approval 必须记录：

- actor_id。
- approved_at。
- chapter_version_id。
- writing_run_id。
- quality_report_id。
- unresolved warning count。
- feedback note。

Approve 后章节进入正式 manuscript。未批准的章节只能作为 draft version 保留。
