from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


WORKSPACE_ID = "01JZWORKSPACE0000000000001"
PROJECT_ID = "01JZPROJECT000000000000001"
CHAPTER_PLAN_ID = "01JZCHPLAN000000000000001"
WRITING_RUN_ID = "01JZWRITING00000000000001"
WRITING_TASK_ID = "01JZWRITETASK0000000000001"
MEMORY_PACKAGE_ID = "01JZMEMPKG000000000000001"
PROMPT_PACKAGE_ID = "01JZPROMPTPKG000000000001"
QUALITY_REPORT_ID = "01JZQLTREP000000000000001"
TRACE_ID = "01JZTRC000000000000000003"
MODEL_PROFILE_DEFAULT_ID = "model_profile_default"
MODEL_PROFILE_STRUCTURED_FALLBACK_ID = "model_profile_structured_fallback"

WRITING_STAGES = [
    "memory_package",
    "prompt_package",
    "writer_draft",
    "critic_review",
    "humanizer_pass",
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
            "current_stage": "humanizer_pass",
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
                "message": "Humanizer pass completed, waiting for review.",
                "payload_ref": None,
                "payload_json": {
                    "current_stage": "humanizer_pass",
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
                "agent_role": "writer",
                "model_profile_id": command["writer_model_profile_id"],
                "provider_name": "anthropic",
                "prompt_tokens": 1800,
                "completion_tokens": 920,
                "latency_ms": 1430,
                "retry_count": 0,
                "cost_estimate": 0.31,
                "status": "succeeded",
                "error_code": None,
            },
            {
                "schema_version": 1,
                "provider_call_id": "01JZPCALL0000000000000002",
                "agent_role": "critic",
                "model_profile_id": command["critic_model_profile_id"],
                "provider_name": "anthropic",
                "prompt_tokens": 1400,
                "completion_tokens": 0,
                "latency_ms": 490,
                "retry_count": 1,
                "cost_estimate": 0.11,
                "status": "failed",
                "error_code": "structured_output_validation_failed",
            },
            {
                "schema_version": 1,
                "provider_call_id": "01JZPCALL0000000000000003",
                "agent_role": "critic",
                "model_profile_id": MODEL_PROFILE_STRUCTURED_FALLBACK_ID,
                "provider_name": "anthropic",
                "prompt_tokens": 1400,
                "completion_tokens": 540,
                "latency_ms": 980,
                "retry_count": 1,
                "cost_estimate": 0.22,
                "status": "succeeded",
                "error_code": None,
            },
            {
                "schema_version": 1,
                "provider_call_id": "01JZPCALL0000000000000004",
                "agent_role": "humanizer",
                "model_profile_id": command["humanizer_model_profile_id"],
                "provider_name": "anthropic",
                "prompt_tokens": 1780,
                "completion_tokens": 850,
                "latency_ms": 1210,
                "retry_count": 0,
                "cost_estimate": 0.33,
                "status": "succeeded",
                "error_code": None,
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
                    "category": "character_consistency",
                    "summary": "第二节仍需补足压迫递进。",
                    "affected_text_ref": "object://drafts/01JZSECRUN00000000000002#p1",
                }
            ],
            "created_at": "2026-07-11T03:08:00Z",
            "updated_at": "2026-07-11T03:08:00Z",
        },
    }


def run_create_writing_run(command: dict[str, Any]) -> dict[str, Any]:
    fixture = build_writing_run_fixture(command)
    return {
        "schema_version": 1,
        "task_id": command["task_id"],
        "status": "requires_review",
        "output_refs": fixture["task"]["output_refs"],
        "metrics": {
            "writing_stages": WRITING_STAGES,
            "current_stage": "humanizer_pass",
            "section_run_count": 3,
            "retry_count": 1,
            "generated_at": utc_now(),
        },
        "errors": [],
        "trace_id": command["trace_id"],
    }
