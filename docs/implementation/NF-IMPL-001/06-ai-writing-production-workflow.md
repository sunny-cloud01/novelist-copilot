# 6. AI Writing Production Workflow

## 6.1 Writing Studio Contract

Writing Studio 是产品落地的核心工作台。

它必须展示：

- current project state
- chapter plan
- scene plan
- beat list
- memory package summary
- style profile summary
- writer draft
- critic issues
- humanizer diff
- quality gate result
- human review actions

## 6.2 Beat Production Contract

每个 Beat 生产必须有独立状态：

```text
planned
writing
critic_review
rewrite_required
humanizer_pass
beat_approved
blocked
```

Writer 不得默认一次生成完整章节。默认每次生成 300 到 800 中文字。

## 6.3 Quality Gate Contract

章节进入正式稿前必须满足：

- no blocking knowledge consistency issue
- no blocking character consistency issue
- ai_flavor_score <= configured threshold
- mobile_readability_score >= configured threshold
- originality_safety_score >= configured threshold
- Humanizer revision_diff persisted
- human_review_required is false or approved by reviewer

## 6.4 Human Review Actions

Writing Reviewer 可执行：

- accept_section
- accept_chapter
- request_rewrite
- edit_and_accept
- send_to_planner
- update_rule_request
- mark_style_preference
- block_generation

所有人工操作必须记录 reason。

## 6.5 Manuscript Assembly

正式 manuscript 只接受 approved chapter。

章节进入 manuscript 后，系统必须生成 chapter_snapshot，并更新 current_story_state、character_dynamic_state、relationship_state、hook_state 和 prior_summary_pack。

后续章节检索必须读取最新动态状态，不得只依赖角色静态卡或旧摘要。
