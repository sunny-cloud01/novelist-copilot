# 9. Task State, Output and Feedback

## 9.1 Writing Run

每次写作任务必须创建 writing_run。

最小字段：

- writing_run_id
- generation_request_id
- target_project_id
- target_chapter_id
- genre_playbook_id
- model_router_profile_id
- status
- current_stage
- current_beat_id
- input_refs
- output_refs
- started_at
- finished_at

## 9.2 Beat Run

每个 Beat 必须创建 beat_run。

最小字段：

- section_run_id
- writing_run_id
- beat_id
- writer_model_profile_id
- critic_model_profile_id
- humanizer_model_profile_id
- status
- retry_count
- draft_ref
- critic_report_ref
- humanized_ref
- accepted_at

## 9.3 Status Model

状态流：

```text
planned
↓
style_ready
↓
writing_beat
↓
critic_review
↓
rewrite_required
↓
writing_beat
↓
humanizer_pass
↓
beat_approved
↓
chapter_assembly
↓
chapter_review
↓
approved or requires_human_review
```

## 9.4 Output Package

Writing Output Package：

```text
WritingOutputPackage
├── metadata
├── story_context_package
├── chapter_plan
├── scene_plan
├── beat_plans
├── style_profile
├── memory_package
├── beat_drafts
├── critic_reports
├── humanizer_reports
├── assembled_chapter
├── quality_report
├── feedback_records
└── export_manifest
```

## 9.5 Feedback Capture

Feedback Service 必须记录：

- beat_acceptance_rate
- rewrite_reason
- ai_flavor_issue_category
- forbidden_phrase_hit
- voice_drift_signal
- human_edit_distance
- reader_reward_signal
- genre_playbook_fit
- model_cost_quality_ratio

## 9.6 Learning Targets

反馈可用于优化：

- model router profile
- prompt template
- style profile
- expression taxonomy
- forbidden phrase rules
- genre playbook
- retrieval strategy
- beat planning strategy

任何影响正式生成策略的自动调整都必须可追踪并可回滚。
