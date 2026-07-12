from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from worker.core_store import load_phase_two_store
from worker.provider_executor import ProviderExecutionError, execute_writing_provider_pipeline


WORKSPACE_ID = "01JZWORKSPACE0000000000001"
PROJECT_ID = "01JZPROJECT000000000000001"
CHAPTER_PLAN_ID = "01JZCHPLAN000000000000001"
WRITING_RUN_ID = "01JZWRITING00000000000001"
WRITING_TASK_ID = "01JZWRITETASK0000000000001"
MEMORY_PACKAGE_ID = "01JZMEMPKG000000000000001"
PROMPT_PACKAGE_ID = "01JZPROMPTPKG000000000001"
QUALITY_REPORT_ID = "01JZQLTREP000000000000001"
CONSISTENCY_REPORT_ID = "01JZCONSIST00000000000001"
TRACE_ID = "01JZTRC000000000000000003"
MODEL_PROFILE_DEFAULT_ID = "model_profile_default"
MODEL_PROFILE_STRUCTURED_FALLBACK_ID = "model_profile_structured_fallback"

WRITING_STAGES = [
    "memory_package",
    "prompt_package",
    "writer_draft",
    "critic_review",
    "humanizer_pass",
    "consistency_review",
    "quality_gate",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_create_writing_run_command(
    project_id: str = PROJECT_ID,
    chapter_plan_id: str = CHAPTER_PLAN_ID,
    writing_run_id: str = WRITING_RUN_ID,
    task_id: str = WRITING_TASK_ID,
    trace_id: str = TRACE_ID,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "command_id": f"cmd-{writing_run_id}",
        "task_id": task_id,
        "task_type": "create_writing_run",
        "workspace_id": WORKSPACE_ID,
        "project_id": project_id,
        "chapter_plan_id": chapter_plan_id,
        "writing_run_id": writing_run_id,
        "writer_model_profile_id": MODEL_PROFILE_DEFAULT_ID,
        "critic_model_profile_id": MODEL_PROFILE_DEFAULT_ID,
        "humanizer_model_profile_id": MODEL_PROFILE_DEFAULT_ID,
        "trace_id": trace_id,
        "requested_by": "core-service",
    }


def build_writing_run_fixture(command: dict[str, Any]) -> dict[str, Any]:
    writing_run_id = command["writing_run_id"]
    return {
        "schema_version": 1,
        "writing_run": {
            "schema_version": 1,
            "writing_run_id": writing_run_id,
            "workspace_id": command["workspace_id"],
            "project_id": command["project_id"],
            "chapter_plan_id": command["chapter_plan_id"],
            "status": "requires_review",
            "task_id": command["task_id"],
            "memory_package_id": MEMORY_PACKAGE_ID,
            "prompt_package_id": PROMPT_PACKAGE_ID,
            "chapter_draft_id": "01JZDRAFT0000000000000001",
            "quality_report_id": QUALITY_REPORT_ID,
            "trace_id": command["trace_id"],
            "current_stage": "consistency_review",
            "writer_model_profile_id": command["writer_model_profile_id"],
            "critic_model_profile_id": MODEL_PROFILE_STRUCTURED_FALLBACK_ID,
            "humanizer_model_profile_id": command["humanizer_model_profile_id"],
            "assembled_chapter": "萧炎在众目睽睽下接住羞辱，也接住了自己的三年之约。",
            "model_cost": {
                "input_tokens": 4980,
                "output_tokens": 2310,
                "estimated_total_cost": 0.86,
                "retry_count": 1,
                "writer_input_tokens": 1800,
                "writer_output_tokens": 920,
                "critic_input_tokens": 1400,
                "critic_output_tokens": 540,
                "humanizer_input_tokens": 1780,
                "humanizer_output_tokens": 850,
            },
            "accepted_into_manuscript_at": None,
            "accepted_chapter_ref": None,
            "created_at": "2026-07-11T03:02:00Z",
            "updated_at": "2026-07-11T03:08:00Z",
        },
        "task": {
            "schema_version": 1,
            "task_id": command["task_id"],
            "task_type": command["task_type"],
            "workspace_id": command["workspace_id"],
            "owner_module": "ai-worker",
            "input_refs": [
                f"object://chapter-plans/{command['chapter_plan_id']}",
                f"object://memory-packages/{MEMORY_PACKAGE_ID}",
                f"object://prompt-packages/{PROMPT_PACKAGE_ID}",
            ],
            "output_refs": [f"object://writing-runs/{writing_run_id}"],
            "status": "requires_review",
            "progress": 100,
            "idempotency_key": f"writing-{command['chapter_plan_id']}",
            "retry_count": 1,
            "error_code": None,
            "created_at": "2026-07-11T03:02:00Z",
            "started_at": "2026-07-11T03:02:05Z",
            "finished_at": "2026-07-11T03:08:00Z",
        },
        "events": [
            {
                "schema_version": 1,
                "task_event_id": "01JZWRITEEVT0000000000001",
                "task_id": command["task_id"],
                "event_type": "writing_run_created",
                "message": "Writing run created.",
                "payload_ref": None,
                "payload_json": {"writing_run_id": writing_run_id},
                "created_at": "2026-07-11T03:02:00Z",
            },
            {
                "schema_version": 1,
                "task_event_id": "01JZWRITEEVT0000000000002",
                "task_id": command["task_id"],
                "event_type": "progress",
                "message": "Consistency review blocked draft and requested revision.",
                "payload_ref": None,
                "payload_json": {
                    "current_stage": "consistency_review",
                    "retry_count": 1,
                    "writing_stages": WRITING_STAGES,
                },
                "created_at": "2026-07-11T03:08:00Z",
            },
        ],
        "provider_calls": [
            {
                "schema_version": 1,
                "provider_call_id": "01JZPCALL0000000000000001",
                "workspace_id": command["workspace_id"],
                "task_id": command["task_id"],
                "writing_run_id": writing_run_id,
                "request_id": "system-worker",
                "trace_id": command["trace_id"],
                "agent_role": "writer",
                "task_type": "writer_task",
                "assignment_id": "01JZASSIGN000000000000006",
                "model_profile_id": command["writer_model_profile_id"],
                "provider_name": "anthropic",
                "provider_model_name": "claude-sonnet-5",
                "provider_account_id": "provider-account-anthropic-default",
                "prompt_package_id": PROMPT_PACKAGE_ID,
                "input_refs": [
                    f"object://chapter-plans/{command['chapter_plan_id']}",
                    f"object://memory-packages/{MEMORY_PACKAGE_ID}",
                    f"object://prompt-packages/{PROMPT_PACKAGE_ID}",
                ],
                "output_ref": "object://drafts/01JZDRAFT0000000000000001",
                "prompt_tokens": 1800,
                "completion_tokens": 920,
                "latency_ms": 1430,
                "retry_count": 0,
                "cost_estimate": 0.31,
                "cost_estimate_status": "estimated",
                "status": "succeeded",
                "error_code": None,
                "fallback_from_call_id": None,
                "created_at": "2026-07-11T03:03:00Z",
            },
            {
                "schema_version": 1,
                "provider_call_id": "01JZPCALL0000000000000002",
                "workspace_id": command["workspace_id"],
                "task_id": command["task_id"],
                "writing_run_id": writing_run_id,
                "request_id": "system-worker",
                "trace_id": command["trace_id"],
                "agent_role": "critic",
                "task_type": "critic_task",
                "assignment_id": "01JZASSIGN000000000000007",
                "model_profile_id": command["critic_model_profile_id"],
                "provider_name": "anthropic",
                "provider_model_name": "claude-sonnet-5",
                "provider_account_id": "provider-account-anthropic-default",
                "prompt_package_id": PROMPT_PACKAGE_ID,
                "input_refs": [f"object://writing-runs/{writing_run_id}"],
                "output_ref": None,
                "prompt_tokens": 1400,
                "completion_tokens": 0,
                "latency_ms": 490,
                "retry_count": 1,
                "cost_estimate": 0.11,
                "cost_estimate_status": "estimated",
                "status": "failed",
                "error_code": "structured_output_validation_failed",
                "fallback_from_call_id": None,
                "created_at": "2026-07-11T03:04:00Z",
            },
            {
                "schema_version": 1,
                "provider_call_id": "01JZPCALL0000000000000003",
                "workspace_id": command["workspace_id"],
                "task_id": command["task_id"],
                "writing_run_id": writing_run_id,
                "request_id": "system-worker",
                "trace_id": command["trace_id"],
                "agent_role": "critic",
                "task_type": "critic_task",
                "assignment_id": "01JZASSIGN000000000000007",
                "model_profile_id": MODEL_PROFILE_STRUCTURED_FALLBACK_ID,
                "provider_name": "anthropic",
                "provider_model_name": "claude-haiku-4-5-20251001",
                "provider_account_id": "provider-account-anthropic-default",
                "prompt_package_id": PROMPT_PACKAGE_ID,
                "input_refs": [f"object://writing-runs/{writing_run_id}"],
                "output_ref": f"object://consistency-reports/{CONSISTENCY_REPORT_ID}",
                "prompt_tokens": 1400,
                "completion_tokens": 540,
                "latency_ms": 980,
                "retry_count": 1,
                "cost_estimate": 0.22,
                "cost_estimate_status": "estimated",
                "status": "succeeded",
                "error_code": None,
                "fallback_from_call_id": "01JZPCALL0000000000000002",
                "created_at": "2026-07-11T03:05:00Z",
            },
            {
                "schema_version": 1,
                "provider_call_id": "01JZPCALL0000000000000004",
                "workspace_id": command["workspace_id"],
                "task_id": command["task_id"],
                "writing_run_id": writing_run_id,
                "request_id": "system-worker",
                "trace_id": command["trace_id"],
                "agent_role": "humanizer",
                "task_type": "humanizer_task",
                "assignment_id": "01JZASSIGN000000000000008",
                "model_profile_id": command["humanizer_model_profile_id"],
                "provider_name": "anthropic",
                "provider_model_name": "claude-sonnet-5",
                "provider_account_id": "provider-account-anthropic-default",
                "prompt_package_id": PROMPT_PACKAGE_ID,
                "input_refs": [f"object://writing-runs/{writing_run_id}"],
                "output_ref": f"object://writing-runs/{writing_run_id}",
                "prompt_tokens": 1780,
                "completion_tokens": 850,
                "latency_ms": 1210,
                "retry_count": 0,
                "cost_estimate": 0.33,
                "cost_estimate_status": "estimated",
                "status": "succeeded",
                "error_code": None,
                "fallback_from_call_id": None,
                "created_at": "2026-07-11T03:06:00Z",
            },
        ],
        "quality_report": {
            "schema_version": 1,
            "quality_report_id": QUALITY_REPORT_ID,
            "workspace_id": command["workspace_id"],
            "writing_run_id": writing_run_id,
            "status": "blocked",
            "ai_flavor_score": 0.34,
            "mobile_readability_score": 0.82,
            "originality_safety_score": 0.91,
            "human_review_required": True,
            "blocking_issues": [
                {
                    "issue_id": "01JZQLTISSUE000000000001",
                    "category": "character_continuity",
                    "summary": "第二节仍需补足压迫递进。",
                    "affected_text_ref": "object://drafts/01JZSECRUN00000000000002#p1",
                }
            ],
            "created_at": "2026-07-11T03:08:00Z",
            "updated_at": "2026-07-11T03:08:00Z",
        },
    }


def _prompt_template_refs(store: Any) -> list[str]:
    refs: list[str] = []
    for role in ("writer", "critic", "humanizer"):
        prompt_version = next((item for item in store.STORE.prompt_versions if item["agent_role"] == role), None)
        refs.append(prompt_version["template_ref"] if prompt_version else f"prompt://{role}/chapter-default")
    return refs


def _build_memory_package_payload(store: Any, writing_run: dict[str, Any], chapter_plan: dict[str, Any], section_plans: list[dict[str, Any]]) -> dict[str, Any]:
    project = store.STORE.novel_projects[writing_run["project_id"]]
    source_refs = [
        f"object://story-bibles/{project['story_bible_id']}",
        f"object://chapter-plans/{writing_run['chapter_plan_id']}",
        *[f"object://section-plans/{item['section_plan_id']}" for item in section_plans],
    ]
    first_graph_summary_id = next(iter(store.STORE.graph_summaries), None)
    if first_graph_summary_id:
        source_refs.append(f"object://graph-summaries/{first_graph_summary_id}")
    chapter_title = chapter_plan.get("payload", {}).get("title") or f"第{chapter_plan['chapter_index']}章"
    return {
        "summary": f"已汇总 {chapter_title} 的故事圣经、章节目标、分节 beats 与图谱证据。",
        "source_refs": source_refs,
    }


def _build_prompt_package_payload(store: Any) -> dict[str, Any]:
    return {
        "summary": "写手、批评者与润色器共用同一章级提示包，按当前配置版本组装。",
        "template_refs": _prompt_template_refs(store),
    }


def run_create_writing_run(command: dict[str, Any]) -> dict[str, Any]:
    store = load_phase_two_store()
    writing_run_id = command["writing_run_id"]
    request_id = "system-worker"
    actor_id = "ai-worker"
    now = utc_now()

    writing_run = store.STORE.writing_runs.get(writing_run_id)
    if not writing_run:
        return {
            "schema_version": 1,
            "task_id": command["task_id"],
            "status": "failed",
            "output_refs": [f"object://writing-runs/{writing_run_id}"],
            "metrics": {"error_code": "writing_run_not_found", "generated_at": now},
            "errors": ["writing run not found"],
            "trace_id": command["trace_id"],
        }

    chapter_plan = store.STORE.chapter_plans.get(command["chapter_plan_id"])
    section_plans = store.STORE.section_plans_by_chapter.get(command["chapter_plan_id"], [])
    section_runs = store.STORE.section_runs_by_writing.get(writing_run_id, [])
    if not chapter_plan or not section_plans or not section_runs:
        return {
            "schema_version": 1,
            "task_id": command["task_id"],
            "status": "failed",
            "output_refs": [f"object://writing-runs/{writing_run_id}"],
            "metrics": {"error_code": "writing_dependencies_missing", "generated_at": now},
            "errors": ["writing dependencies missing"],
            "trace_id": command["trace_id"],
        }

    memory_package = _build_memory_package_payload(store, writing_run, chapter_plan, section_plans)
    prompt_package = _build_prompt_package_payload(store)
    try:
        provider_execution = execute_writing_provider_pipeline(
            store=store,
            writing_run=writing_run,
            chapter_plan=chapter_plan,
            section_plans=section_plans,
            section_runs=section_runs,
            prompt_package=prompt_package,
        )
    except ProviderExecutionError as exc:
        metrics = {"error_code": exc.error_code, "generated_at": now}
        task = store.apply_task_execution_result(
            command["task_id"],
            "failed",
            [f"object://writing-runs/{writing_run_id}"],
            metrics,
            trace_id=command["trace_id"],
            request_id=request_id,
            actor_id=actor_id,
        )
        return {
            "schema_version": 1,
            "task_id": command["task_id"],
            "status": "failed",
            "output_refs": task["output_refs"] if task else [f"object://writing-runs/{writing_run_id}"],
            "metrics": metrics,
            "errors": [str(exc)],
            "trace_id": command["trace_id"],
        }

    section_run_updates = provider_execution["section_runs"]
    assembled_chapter = provider_execution["assembled_chapter"]
    consistency_issues = provider_execution["consistency_issues"]
    provider_calls = provider_execution["provider_calls"]
    retry_count = provider_execution["retry_count"]
    model_cost = provider_execution["model_cost"]
    issue_count = len(consistency_issues)
    blocking_issue_count = len([item for item in consistency_issues if item["resolution_status"] == "open"])
    quality_blocking_issues = [
        {
            **issue,
            "output_refs": [f"object://quality-reports/{writing_run['quality_report_id']}/issues/{index}"],
        }
        for index, issue in enumerate(consistency_issues, start=1)
    ]
    current_stage = "consistency_review" if blocking_issue_count else "quality_gate"
    status = "requires_review" if blocking_issue_count else "succeeded"
    quality_status = "blocked" if blocking_issue_count else "passed"
    ai_flavor_score = 0.34 if blocking_issue_count else 0.52
    mobile_readability_score = round(min(0.95, 0.74 + len(section_runs) * 0.03), 2)
    originality_safety_score = 0.91
    revision_change_summary = (
        "要求重写第二节，恢复主角当前境界并补足冲突升级。"
        if blocking_issue_count
        else "一致性检查通过，无需额外修订。"
    )
    consistency_report = {
        "status": "blocked" if blocking_issue_count else "passed",
        "issue_count": issue_count,
        "blocking_issue_count": blocking_issue_count,
        "checked_domains": ["character_continuity", "power_system_constraint"],
        "issues": consistency_issues,
        "input_refs": [f"object://writing-runs/{writing_run_id}"],
        "output_refs": [f"object://consistency-reports/{writing_run['consistency_report_id']}"],
    }
    revision_summary = {
        "status": "requested" if blocking_issue_count else "accepted",
        "revision_round": 1 if blocking_issue_count else 0,
        "max_revision_rounds": writing_run.get("max_revision_rounds", 3),
        "source_issue_ids": [item["issue_id"] for item in consistency_issues],
        "change_summary": revision_change_summary,
        "revision_diff_ref": None,
        "reviewer_note_ref": (
            f"object://review-notes/{writing_run.get('revision_summary_id')}"
            if blocking_issue_count and writing_run.get("revision_summary_id")
            else None
        ),
        "input_refs": [f"object://consistency-reports/{writing_run['consistency_report_id']}"],
        "output_refs": [f"object://revision-summaries/{writing_run['revision_summary_id']}"],
    }
    quality_report = {
        "status": quality_status,
        "ai_flavor_score": ai_flavor_score,
        "mobile_readability_score": mobile_readability_score,
        "originality_safety_score": originality_safety_score,
        "human_review_required": bool(blocking_issue_count),
        "blocking_issues": quality_blocking_issues,
    }
    feedback_records = [
        store._build_feedback_record(
            feedback_record_id=str(store.ulid.new()),
            workspace_id=writing_run["workspace_id"],
            target_type="writing_run",
            target_id=writing_run_id,
            feedback_type="quality",
            score=mobile_readability_score,
            source="quality_gate",
            request_id=request_id,
            trace_id=command["trace_id"],
            actor_id=actor_id,
            comment_ref=f"object://quality-comments/{writing_run_id}",
            payload={
                "quality_report_id": writing_run["quality_report_id"],
                "summary": "质量门禁已写入移动可读性、AI 味与原创安全指标。",
            },
            input_refs=[f"object://writing-runs/{writing_run_id}"],
            output_refs=[f"object://quality-reports/{writing_run['quality_report_id']}"],
            created_at=now,
        ),
        store._build_feedback_record(
            feedback_record_id=str(store.ulid.new()),
            workspace_id=writing_run["workspace_id"],
            target_type="quality_report",
            target_id=writing_run["quality_report_id"],
            feedback_type="style",
            score=0.64 if blocking_issue_count else 0.79,
            source="critic",
            request_id=request_id,
            trace_id=command["trace_id"],
            actor_id=actor_id,
            comment_ref=f"object://critic-comments/{writing_run_id}",
            payload={
                "affected_text_ref": quality_blocking_issues[0]["affected_text_ref"] if quality_blocking_issues else section_runs[-1]["humanized_object_ref"],
                "summary": revision_change_summary,
            },
            input_refs=[f"object://quality-reports/{writing_run['quality_report_id']}"],
            output_refs=[],
            created_at=now,
        ),
    ]
    metrics = {
        "writing_stages": WRITING_STAGES,
        "current_stage": current_stage,
        "section_run_count": len(section_runs),
        "retry_count": retry_count,
        "assembled_chapter": assembled_chapter,
        "blocking_issue_count": blocking_issue_count,
        "issue_count": issue_count,
        "blocking_issues": quality_blocking_issues,
        "ai_flavor_score": ai_flavor_score,
        "mobile_readability_score": mobile_readability_score,
        "originality_safety_score": originality_safety_score,
        "revision_summary": revision_change_summary,
        "generated_at": now,
        "latency_ms": sum(item.get("latency_ms", 0) for item in provider_calls),
        "provider_calls": provider_calls,
        "model_cost": model_cost,
        "memory_package": memory_package,
        "prompt_package": prompt_package,
        "section_runs": section_run_updates,
        "quality_report": quality_report,
        "consistency_report": consistency_report,
        "revision_summary": revision_summary,
        "feedback_records": feedback_records,
    }
    task = store.apply_task_execution_result(
        command["task_id"],
        status,
        [f"object://writing-runs/{writing_run_id}"],
        metrics,
        trace_id=command["trace_id"],
        request_id=request_id,
        actor_id=actor_id,
    )
    return {
        "schema_version": 1,
        "task_id": command["task_id"],
        "status": status,
        "output_refs": task["output_refs"] if task else [f"object://writing-runs/{writing_run_id}"],
        "metrics": metrics,
        "errors": [],
        "trace_id": command["trace_id"],
    }
