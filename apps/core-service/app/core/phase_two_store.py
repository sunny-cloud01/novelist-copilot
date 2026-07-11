from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import ulid


USER_ID = "demo-user"
WORKSPACE_ID = "demo-workspace"
WORKSPACE_MEMBER_ID = "demo-workspace-member"
BOOK_ID = "01JZBOOK000000000000000001"
RUN_ID = "01JZRUN0000000000000000001"
TASK_ID = "01JZTASK000000000000000001"
GRAPH_BOOK_ID = BOOK_ID
PROJECT_ID = "01JZPROJECT000000000000001"
STORY_BIBLE_ID = "01JZBIBLE0000000000000001"
CHAPTER_PLAN_ID = "01JZCHPLAN000000000000001"
CHAPTER_PLAN_TASK_ID = "01JZPLANTASK0000000000001"
SECTION_PLAN_TASK_ID = "01JZSECTTASK0000000000001"
QUALITY_GATE_PROFILE_ID = "01JZQUALITY00000000000001"
WRITING_RUN_ID = "01JZWRITING00000000000001"
WRITING_TASK_ID = "01JZWRITETASK0000000000001"
MEMORY_PACKAGE_ID = "01JZMEMPKG000000000000001"
PROMPT_PACKAGE_ID = "01JZPROMPTPKG000000000001"
QUALITY_REPORT_ID = "01JZQLTREP000000000000001"
CHAPTER_DRAFT_ID = "01JZDRAFT0000000000000001"
MODEL_PROFILE_DEFAULT_ID = "model_profile_default"
MODEL_PROFILE_STRUCTURED_FALLBACK_ID = "model_profile_structured_fallback"
DEFAULT_MODEL_PROFILE_ID = MODEL_PROFILE_DEFAULT_ID
MVP_AGENT_ROLES = [
    "extraction",
    "normalization",
    "planning",
    "memory",
    "style_analyzer",
    "writer",
    "critic",
    "humanizer",
    "review",
    "feedback",
]
ROLE_CALL_METRICS = {
    "writer": {"prompt_tokens": 1800, "completion_tokens": 920, "latency_ms": 1430, "cost_estimate": 0.31},
    "critic": {"prompt_tokens": 1400, "completion_tokens": 540, "latency_ms": 980, "cost_estimate": 0.22},
    "humanizer": {"prompt_tokens": 1780, "completion_tokens": 850, "latency_ms": 1210, "cost_estimate": 0.33},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CoreStore:
    users: dict[str, dict[str, Any]] = field(default_factory=dict)
    workspaces: dict[str, dict[str, Any]] = field(default_factory=dict)
    workspace_members: dict[str, dict[str, Any]] = field(default_factory=dict)
    books: dict[str, dict[str, Any]] = field(default_factory=dict)
    chapters_by_book: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    extraction_runs: dict[str, dict[str, Any]] = field(default_factory=dict)
    knowledge_objects: dict[str, dict[str, Any]] = field(default_factory=dict)
    knowledge_by_run: dict[str, list[str]] = field(default_factory=dict)
    graph_summaries: dict[str, dict[str, Any]] = field(default_factory=dict)
    novel_projects: dict[str, dict[str, Any]] = field(default_factory=dict)
    story_bibles: dict[str, dict[str, Any]] = field(default_factory=dict)
    chapter_plans: dict[str, dict[str, Any]] = field(default_factory=dict)
    chapter_plan_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)
    section_plan_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)
    section_plans_by_chapter: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    model_profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    agent_model_assignments: dict[str, dict[str, Any]] = field(default_factory=dict)
    quality_gate_profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    prompt_versions: list[dict[str, Any]] = field(default_factory=list)
    writing_runs: dict[str, dict[str, Any]] = field(default_factory=dict)
    writing_run_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)
    provider_calls_by_writing: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    section_runs_by_writing: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    memory_packages: dict[str, dict[str, Any]] = field(default_factory=dict)
    prompt_packages: dict[str, dict[str, Any]] = field(default_factory=dict)
    quality_reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    chapter_snapshots: dict[str, dict[str, Any]] = field(default_factory=dict)
    manuscript_states_by_project: dict[str, dict[str, Any]] = field(default_factory=dict)
    feedback_records: dict[str, dict[str, Any]] = field(default_factory=dict)
    task_events_by_task: dict[str, list[dict[str, Any]]] = field(default_factory=dict)


STORE = CoreStore()


def reset_store() -> None:
    STORE.users.clear()
    STORE.workspaces.clear()
    STORE.workspace_members.clear()
    STORE.books.clear()
    STORE.chapters_by_book.clear()
    STORE.extraction_runs.clear()
    STORE.knowledge_objects.clear()
    STORE.knowledge_by_run.clear()
    STORE.graph_summaries.clear()
    STORE.novel_projects.clear()
    STORE.story_bibles.clear()
    STORE.chapter_plans.clear()
    STORE.chapter_plan_tasks.clear()
    STORE.section_plan_tasks.clear()
    STORE.section_plans_by_chapter.clear()
    STORE.model_profiles.clear()
    STORE.agent_model_assignments.clear()
    STORE.quality_gate_profiles.clear()
    STORE.prompt_versions.clear()
    STORE.writing_runs.clear()
    STORE.writing_run_tasks.clear()
    STORE.provider_calls_by_writing.clear()
    STORE.section_runs_by_writing.clear()
    STORE.memory_packages.clear()
    STORE.prompt_packages.clear()
    STORE.quality_reports.clear()
    STORE.chapter_snapshots.clear()
    STORE.manuscript_states_by_project.clear()
    STORE.feedback_records.clear()
    STORE.task_events_by_task.clear()


def seed_phase_two_demo_data() -> None:
    if STORE.books:
        return

    STORE.users[USER_ID] = {
        "schema_version": 1,
        "user_id": USER_ID,
        "display_name": "演示作者",
        "status": "active",
        "created_at": "2026-07-11T00:00:00Z",
        "updated_at": "2026-07-11T00:10:00Z",
    }
    STORE.workspaces[WORKSPACE_ID] = {
        "schema_version": 1,
        "workspace_id": _workspace_or_default(),
        "owner_user_id": USER_ID,
        "name": "默认中文工作区",
        "slug": WORKSPACE_ID,
        "default_language": "zh-CN",
        "status": "active",
        "created_at": "2026-07-11T00:00:00Z",
        "updated_at": "2026-07-11T00:10:00Z",
    }
    STORE.workspace_members[WORKSPACE_MEMBER_ID] = {
        "schema_version": 1,
        "workspace_member_id": WORKSPACE_MEMBER_ID,
        "workspace_id": _workspace_or_default(),
        "user_id": USER_ID,
        "role": "owner",
        "status": "active",
        "created_at": "2026-07-11T00:00:00Z",
        "updated_at": "2026-07-11T00:10:00Z",
    }

    book = {
        "schema_version": 1,
        "book_id": BOOK_ID,
        "workspace_id": _workspace_or_default(),
        "title": "Battle Through the Heavens",
        "author_name": "Tian Can Tu Dou",
        "source_type": "reference_novel",
        "import_status": "ready",
        "trace_id": "01JZTRC000000000000000001",
        "created_at": "2026-07-11T00:00:00Z",
        "updated_at": "2026-07-11T00:10:00Z",
    }
    STORE.books[BOOK_ID] = book
    STORE.chapters_by_book[BOOK_ID] = [
        {
            "schema_version": 1,
            "chapter_id": "01JZCHAPTER00000000000001",
            "book_id": BOOK_ID,
            "chapter_index": 1,
            "title": "Three-Year Agreement",
            "segmentation_status": "segmented",
            "text_object_ref": "object://source-chapters/01JZCHAPTER00000000000001",
        },
        {
            "schema_version": 1,
            "chapter_id": "01JZCHAPTER00000000000002",
            "book_id": BOOK_ID,
            "chapter_index": 2,
            "title": "Yao Lao Appears",
            "segmentation_status": "segmented",
            "text_object_ref": "object://source-chapters/01JZCHAPTER00000000000002",
        },
    ]
    STORE.model_profiles[MODEL_PROFILE_DEFAULT_ID] = {
        "schema_version": 1,
        "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
        "provider_name": "anthropic",
        "provider_model_name": "claude-sonnet-5",
        "label": "默认中文长文本模型",
        "description": "大多数 Agent role 默认使用。",
        "enabled": True,
        "supports_structured_output": False,
        "fallback_profile_ids": [MODEL_PROFILE_STRUCTURED_FALLBACK_ID],
    }
    STORE.model_profiles[MODEL_PROFILE_STRUCTURED_FALLBACK_ID] = {
        "schema_version": 1,
        "model_profile_id": MODEL_PROFILE_STRUCTURED_FALLBACK_ID,
        "provider_name": "anthropic",
        "provider_model_name": "claude-haiku-4-5-20251001",
        "label": "结构化兜底模型",
        "description": "结构化输出失败后重试使用。",
        "enabled": True,
        "supports_structured_output": True,
        "fallback_profile_ids": [],
    }
    for index, role in enumerate(MVP_AGENT_ROLES, start=1):
        output_mode = "structured" if role in {"critic", "review", "feedback"} else "text"
        STORE.agent_model_assignments[f"01JZASSIGN{index:015d}"] = {
            "schema_version": 1,
            "assignment_id": f"01JZASSIGN{index:015d}",
            "agent_role": role,
            "task_type": f"{role}_task",
            "output_mode": output_mode,
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "fallback_profile_ids": [MODEL_PROFILE_STRUCTURED_FALLBACK_ID] if output_mode == "structured" or role in {"writer", "humanizer"} else [],
            "max_retry": 2 if role == "critic" else 1,
            "max_cost": 1.5 if role == "writer" else 0.8,
            "enabled": True,
        }
    STORE.quality_gate_profiles[QUALITY_GATE_PROFILE_ID] = {
        "quality_gate_profile_id": QUALITY_GATE_PROFILE_ID,
        "label": "默认质量阈值",
        "ai_flavor_threshold": 0.45,
        "originality_safety_threshold": 0.85,
    }
    STORE.prompt_versions.extend(
        [
            {"agent_role": "writer", "template_ref": "prompt://writer/chapter-default"},
            {"agent_role": "critic", "template_ref": "prompt://critic/chapter-default"},
            {"agent_role": "humanizer", "template_ref": "prompt://humanizer/chapter-default"},
            {"agent_role": "feedback", "template_ref": "prompt://feedback/chapter-default"},
        ]
    )

    knowledge_objects = [
        {
            "schema_version": 1,
            "object_id": "01JZOBJ0000000000000000001",
            "workspace_id": _workspace_or_default(),
            "object_type": "character",
            "canonical_name": "Xiao Yan",
            "lifecycle_status": "candidate",
            "review_status": "pending",
            "confidence": 0.58,
            "evidence_refs": ["evidence://01JZEVIDENCE0000000000001"],
            "payload": {"schema_version": 1, "aliases": ["Yan"]},
        },
        {
            "schema_version": 1,
            "object_id": "01JZOBJ0000000000000000002",
            "workspace_id": _workspace_or_default(),
            "object_type": "mentor",
            "canonical_name": "Yao Lao",
            "lifecycle_status": "candidate",
            "review_status": "pending",
            "confidence": 0.44,
            "evidence_refs": ["evidence://01JZEVIDENCE0000000000002"],
            "payload": {"schema_version": 1, "aliases": ["Old Yao"]},
        },
        {
            "schema_version": 1,
            "object_id": "01JZOBJ0000000000000000003",
            "workspace_id": _workspace_or_default(),
            "object_type": "clan",
            "canonical_name": "Xiao Clan",
            "lifecycle_status": "approved",
            "review_status": "approved",
            "confidence": 0.97,
            "evidence_refs": ["evidence://01JZEVIDENCE0000000000003"],
            "payload": {"schema_version": 1, "aliases": []},
        },
    ]
    for obj in knowledge_objects:
        STORE.knowledge_objects[obj["object_id"]] = obj
    STORE.knowledge_by_run[RUN_ID] = [obj["object_id"] for obj in knowledge_objects]

    STORE.extraction_runs[RUN_ID] = {
        "schema_version": 1,
        "run_id": RUN_ID,
        "book_id": BOOK_ID,
        "workspace_id": _workspace_or_default(),
        "task_id": TASK_ID,
        "status": "requires_review",
        "current_stage": "quality_review",
        "chapter_count": 2,
        "scene_count": 6,
        "object_count": 3,
        "evidence_count": 3,
        "low_confidence_count": 2,
        "errors": [],
        "created_at": "2026-07-11T00:00:00Z",
        "started_at": "2026-07-11T00:00:05Z",
        "finished_at": None,
        "task": {
            "schema_version": 1,
            "task_id": TASK_ID,
            "task_type": "extract_knowledge",
            "workspace_id": _workspace_or_default(),
            "owner_module": "ai-worker",
            "input_refs": [f"object://source-books/{BOOK_ID}"],
            "output_refs": [f"object://extraction-runs/{RUN_ID}"],
            "status": "requires_review",
            "progress": 88,
            "idempotency_key": f"extract-{BOOK_ID}-001",
            "retry_count": 0,
            "error_code": None,
            "created_at": "2026-07-11T00:00:00Z",
            "started_at": "2026-07-11T00:00:05Z",
            "finished_at": None,
        },
    }
    STORE.task_events_by_task[TASK_ID] = [
        {
            "schema_version": 1,
            "task_event_id": "01JZEVT000000000000000001",
            "task_id": TASK_ID,
            "event_type": "created",
            "message": "Extraction run created.",
            "payload_ref": None,
            "payload_json": None,
            "created_at": "2026-07-11T00:00:00Z",
        },
        {
            "schema_version": 1,
            "task_event_id": "01JZEVT000000000000000002",
            "task_id": TASK_ID,
            "event_type": "progress",
            "message": "Low confidence objects require review.",
            "payload_ref": None,
            "payload_json": {"current_stage": "quality_review", "low_confidence_count": 2},
            "created_at": "2026-07-11T00:01:00Z",
        },
    ]
    STORE.graph_summaries[GRAPH_BOOK_ID] = {
        "schema_version": 1,
        "book_id": GRAPH_BOOK_ID,
        "node_count": 3,
        "edge_count": 2,
        "nodes": [
            {
                "node_id": "01JZNODE000000000000000001",
                "label": "Xiao Yan",
                "node_type": "character",
                "evidence_refs": ["evidence://01JZEVIDENCE0000000000001"],
            },
            {
                "node_id": "01JZNODE000000000000000002",
                "label": "Yao Lao",
                "node_type": "mentor",
                "evidence_refs": ["evidence://01JZEVIDENCE0000000000002"],
            },
            {
                "node_id": "01JZNODE000000000000000003",
                "label": "Xiao Clan",
                "node_type": "clan",
                "evidence_refs": ["evidence://01JZEVIDENCE0000000000003"],
            },
        ],
    }

    project = {
        "schema_version": 1,
        "project_id": PROJECT_ID,
        "workspace_id": _workspace_or_default(),
        "title": "斗破苍穹衍生原创",
        "genre_scope": "玄幻升级流",
        "status": "planning",
        "story_bible_id": STORY_BIBLE_ID,
        "quality_gate_profile_id": QUALITY_GATE_PROFILE_ID,
        "allowed_knowledge_source_refs": [
            f"object://source-books/{BOOK_ID}",
            f"object://graph-summaries/{BOOK_ID}",
        ],
        "created_at": "2026-07-11T02:00:00Z",
        "updated_at": "2026-07-11T02:05:00Z",
    }
    STORE.novel_projects[PROJECT_ID] = project
    STORE.story_bibles[STORY_BIBLE_ID] = {
        "schema_version": 1,
        "story_bible_id": STORY_BIBLE_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "version": 1,
        "status": "approved",
        "payload": {
            "premise": "少年背负退婚耻辱后，踏上逆袭与成长之路。",
            "protagonist": "萧炎",
            "core_conflict": "天赋跌落后的家族压力与三年之约。",
        },
        "trace_id": "01JZTRC000000000000000002",
        "created_at": "2026-07-11T02:00:00Z",
        "updated_at": "2026-07-11T02:05:00Z",
    }
    STORE.chapter_plans[CHAPTER_PLAN_ID] = {
        "schema_version": 1,
        "chapter_plan_id": CHAPTER_PLAN_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "chapter_index": 1,
        "status": "requires_review",
        "target_word_count": 3200,
        "payload": {
            "title": "乌坦城风起",
            "summary": "主角在第一章完成进入主线前的势能铺垫。",
        },
        "created_at": "2026-07-11T02:10:00Z",
        "updated_at": "2026-07-11T02:12:00Z",
    }
    STORE.chapter_plan_tasks[CHAPTER_PLAN_ID] = {
        "schema_version": 1,
        "task_id": CHAPTER_PLAN_TASK_ID,
        "task_type": "create_chapter_plan",
        "workspace_id": _workspace_or_default(),
        "owner_module": "ai-worker",
        "input_refs": [f"object://novel-projects/{PROJECT_ID}"],
        "output_refs": [f"object://chapter-plans/{CHAPTER_PLAN_ID}"],
        "status": "requires_review",
        "progress": 100,
        "idempotency_key": f"plan-{PROJECT_ID}-1",
        "retry_count": 0,
        "error_code": None,
        "created_at": "2026-07-11T02:10:00Z",
        "started_at": "2026-07-11T02:10:03Z",
        "finished_at": "2026-07-11T02:12:00Z",
    }
    STORE.task_events_by_task[CHAPTER_PLAN_TASK_ID] = [
        {
            "schema_version": 1,
            "task_event_id": "01JZPLANEVT0000000000001",
            "task_id": CHAPTER_PLAN_TASK_ID,
            "event_type": "created",
            "message": "Chapter plan created.",
            "payload_ref": None,
            "payload_json": {"chapter_index": 1},
            "created_at": "2026-07-11T02:10:00Z",
        },
        {
            "schema_version": 1,
            "task_event_id": "01JZPLANEVT0000000000002",
            "task_id": CHAPTER_PLAN_TASK_ID,
            "event_type": "progress",
            "message": "Chapter plan ready for review.",
            "payload_ref": None,
            "payload_json": {"status": "requires_review"},
            "created_at": "2026-07-11T02:12:00Z",
        },
    ]
    STORE.section_plans_by_chapter[CHAPTER_PLAN_ID] = [
        {
            "schema_version": 1,
            "section_plan_id": "01JZSECT0000000000000001",
            "workspace_id": _workspace_or_default(),
            "chapter_plan_id": CHAPTER_PLAN_ID,
            "section_index": 1,
            "planning_role": "setup",
            "payload": {
                "scene_goal": "建立乌坦城压抑氛围",
                "beats": [
                    {"index": 1, "summary": "主角出场"},
                    {"index": 2, "summary": "家族压力显现"},
                ],
            },
            "created_at": "2026-07-11T02:15:00Z",
            "updated_at": "2026-07-11T02:18:00Z",
        },
        {
            "schema_version": 1,
            "section_plan_id": "01JZSECT0000000000000002",
            "workspace_id": _workspace_or_default(),
            "chapter_plan_id": CHAPTER_PLAN_ID,
            "section_index": 2,
            "planning_role": "conflict",
            "payload": {
                "scene_goal": "压强进一步落到主角身上",
                "beats": [
                    {"index": 1, "summary": "长辈对主角失望"},
                    {"index": 2, "summary": "纳兰家消息传来"},
                ],
            },
            "created_at": "2026-07-11T02:16:00Z",
            "updated_at": "2026-07-11T02:18:00Z",
        },
        {
            "schema_version": 1,
            "section_plan_id": "01JZSECT0000000000000003",
            "workspace_id": _workspace_or_default(),
            "chapter_plan_id": CHAPTER_PLAN_ID,
            "section_index": 3,
            "planning_role": "turn",
            "payload": {
                "scene_goal": "把侮辱转化为主线承诺",
                "beats": [
                    {"index": 1, "summary": "退婚现场升级"},
                    {"index": 2, "summary": "主角立下三年之约"},
                ],
            },
            "created_at": "2026-07-11T02:17:00Z",
            "updated_at": "2026-07-11T02:18:00Z",
        },
    ]
    STORE.section_plan_tasks[CHAPTER_PLAN_ID] = {
        "schema_version": 1,
        "task_id": SECTION_PLAN_TASK_ID,
        "task_type": "create_section_plans",
        "workspace_id": _workspace_or_default(),
        "owner_module": "ai-worker",
        "input_refs": [f"object://chapter-plans/{CHAPTER_PLAN_ID}"],
        "output_refs": [
            "object://section-plans/01JZSECT0000000000000001",
            "object://section-plans/01JZSECT0000000000000002",
            "object://section-plans/01JZSECT0000000000000003",
        ],
        "status": "succeeded",
        "progress": 100,
        "idempotency_key": f"section-{CHAPTER_PLAN_ID}",
        "retry_count": 0,
        "error_code": None,
        "created_at": "2026-07-11T02:15:00Z",
        "started_at": "2026-07-11T02:15:05Z",
        "finished_at": "2026-07-11T02:18:00Z",
    }
    STORE.memory_packages[MEMORY_PACKAGE_ID] = {
        "schema_version": 1,
        "memory_package_id": MEMORY_PACKAGE_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "writing_run_id": WRITING_RUN_ID,
        "summary": "已汇总故事圣经、章节目标、人物状态与来源证据。",
        "source_refs": [
            f"object://story-bibles/{STORY_BIBLE_ID}",
            f"object://chapter-plans/{CHAPTER_PLAN_ID}",
            "object://section-plans/01JZSECT0000000000000001",
            "object://graph-summaries/01JZBOOK000000000000000001",
        ],
        "created_at": "2026-07-11T03:00:00Z",
        "updated_at": "2026-07-11T03:00:00Z",
    }
    STORE.prompt_packages[PROMPT_PACKAGE_ID] = {
        "schema_version": 1,
        "prompt_package_id": PROMPT_PACKAGE_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "writing_run_id": WRITING_RUN_ID,
        "summary": "写手、批评者与润色器共用同一章级提示包。",
        "template_refs": [
            "prompt://writer/chapter-default",
            "prompt://critic/chapter-default",
            "prompt://humanizer/chapter-default",
        ],
        "created_at": "2026-07-11T03:01:00Z",
        "updated_at": "2026-07-11T03:01:00Z",
    }
    STORE.writing_runs[WRITING_RUN_ID] = {
        "schema_version": 1,
        "writing_run_id": WRITING_RUN_ID,
        "workspace_id": _workspace_or_default(),
        "project_id": PROJECT_ID,
        "chapter_plan_id": CHAPTER_PLAN_ID,
        "status": "requires_review",
        "task_id": WRITING_TASK_ID,
        "memory_package_id": MEMORY_PACKAGE_ID,
        "prompt_package_id": PROMPT_PACKAGE_ID,
        "chapter_draft_id": CHAPTER_DRAFT_ID,
        "quality_report_id": QUALITY_REPORT_ID,
        "trace_id": "01JZTRC000000000000000003",
        "current_stage": "humanizer_pass",
        "writer_model_profile_id": MODEL_PROFILE_DEFAULT_ID,
        "critic_model_profile_id": MODEL_PROFILE_STRUCTURED_FALLBACK_ID,
        "humanizer_model_profile_id": MODEL_PROFILE_DEFAULT_ID,
        "assembled_chapter": "萧炎在家族议事厅外停步，先听见堂内压抑的议论，再踏入众人目光中心。纳兰家的退婚信像利刃一样落下，他在众目睽睽之下接住羞辱，也在心底立下三年之约。",
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
        "chapter_snapshot_id": None,
        "manuscript_state_id": None,
        "created_at": "2026-07-11T03:02:00Z",
        "updated_at": "2026-07-11T03:08:00Z",
    }
    STORE.writing_run_tasks[WRITING_RUN_ID] = {
        "schema_version": 1,
        "task_id": WRITING_TASK_ID,
        "task_type": "create_writing_run",
        "workspace_id": _workspace_or_default(),
        "owner_module": "ai-worker",
        "input_refs": [
            f"object://chapter-plans/{CHAPTER_PLAN_ID}",
            f"object://memory-packages/{MEMORY_PACKAGE_ID}",
            f"object://prompt-packages/{PROMPT_PACKAGE_ID}",
        ],
        "output_refs": [f"object://writing-runs/{WRITING_RUN_ID}"],
        "status": "requires_review",
        "progress": 100,
        "idempotency_key": f"writing-{CHAPTER_PLAN_ID}",
        "retry_count": 1,
        "error_code": None,
        "created_at": "2026-07-11T03:02:00Z",
        "started_at": "2026-07-11T03:02:05Z",
        "finished_at": "2026-07-11T03:08:00Z",
    }
    STORE.provider_calls_by_writing[WRITING_RUN_ID] = [
        {
            "schema_version": 1,
            "provider_call_id": "01JZPCALL0000000000000001",
            "agent_role": "writer",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
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
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
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
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "provider_name": "anthropic",
            "prompt_tokens": 1780,
            "completion_tokens": 850,
            "latency_ms": 1210,
            "retry_count": 0,
            "cost_estimate": 0.33,
            "status": "succeeded",
            "error_code": None,
        },
    ]
    STORE.section_runs_by_writing[WRITING_RUN_ID] = [
        {
            "schema_version": 1,
            "section_run_id": "01JZSECRUN00000000000001",
            "workspace_id": _workspace_or_default(),
            "writing_run_id": WRITING_RUN_ID,
            "section_plan_id": "01JZSECT0000000000000001",
            "status": "beat_approved",
            "draft_object_ref": "object://drafts/01JZSECRUN00000000000001",
            "critic_report_ref": "object://critic-reports/01JZSECRUN00000000000001",
            "humanized_object_ref": "object://humanized/01JZSECRUN00000000000001",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "beat_status": [
                {"index": 1, "status": "beat_approved"},
                {"index": 2, "status": "beat_approved"},
            ],
            "writer_output": "乌坦城天色未亮，萧炎已经听见议事堂传来的细碎争论。",
            "critic_issues": [],
            "humanized_text": "天还没亮透，议事堂里的争论已经顺着长廊飘到萧炎耳边。",
            "created_at": "2026-07-11T03:03:00Z",
            "updated_at": "2026-07-11T03:04:00Z",
        },
        {
            "schema_version": 1,
            "section_run_id": "01JZSECRUN00000000000002",
            "workspace_id": _workspace_or_default(),
            "writing_run_id": WRITING_RUN_ID,
            "section_plan_id": "01JZSECT0000000000000002",
            "status": "rewrite_required",
            "draft_object_ref": "object://drafts/01JZSECRUN00000000000002",
            "critic_report_ref": "object://critic-reports/01JZSECRUN00000000000002",
            "humanized_object_ref": "object://humanized/01JZSECRUN00000000000002",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "beat_status": [
                {"index": 1, "status": "critic_review"},
                {"index": 2, "status": "rewrite_required"},
            ],
            "writer_output": "纳兰家的消息在厅内炸开，所有目光都压向萧炎。",
            "critic_issues": [
                {
                    "issue_id": "01JZCRTIC000000000000001",
                    "severity": "blocking",
                    "category": "character_consistency",
                    "summary": "主角情绪转折过快，缺少被压迫感铺垫。",
                    "affected_text_ref": "object://drafts/01JZSECRUN00000000000002#p1",
                }
            ],
            "humanized_text": "纳兰家的来信一到，厅里的空气像骤然压低了一层，所有审视都落到萧炎身上。",
            "created_at": "2026-07-11T03:04:00Z",
            "updated_at": "2026-07-11T03:06:00Z",
        },
        {
            "schema_version": 1,
            "section_run_id": "01JZSECRUN00000000000003",
            "workspace_id": _workspace_or_default(),
            "writing_run_id": WRITING_RUN_ID,
            "section_plan_id": "01JZSECT0000000000000003",
            "status": "humanizer_pass",
            "draft_object_ref": "object://drafts/01JZSECRUN00000000000003",
            "critic_report_ref": "object://critic-reports/01JZSECRUN00000000000003",
            "humanized_object_ref": "object://humanized/01JZSECRUN00000000000003",
            "model_profile_id": MODEL_PROFILE_DEFAULT_ID,
            "beat_status": [
                {"index": 1, "status": "humanizer_pass"},
                {"index": 2, "status": "humanizer_pass"},
            ],
            "writer_output": "萧炎当众抬头，把退婚羞辱化成三年之约。",
            "critic_issues": [
                {
                    "issue_id": "01JZCRTIC000000000000002",
                    "severity": "warning",
                    "category": "style",
                    "summary": "金手指暗示可再收敛，避免过早泄露。",
                    "affected_text_ref": "object://drafts/01JZSECRUN00000000000003#p1",
                }
            ],
            "humanized_text": "他在众人的嘲讽里抬起头，把那封退婚信压回桌上，只留下一句三年后再见。",
            "created_at": "2026-07-11T03:06:00Z",
            "updated_at": "2026-07-11T03:08:00Z",
        },
    ]
    STORE.quality_reports[QUALITY_REPORT_ID] = {
        "schema_version": 1,
        "quality_report_id": QUALITY_REPORT_ID,
        "workspace_id": _workspace_or_default(),
        "writing_run_id": WRITING_RUN_ID,
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
    }
    STORE.task_events_by_task[WRITING_TASK_ID] = [
        {
            "schema_version": 1,
            "task_event_id": "01JZWRITEEVT0000000000001",
            "task_id": WRITING_TASK_ID,
            "event_type": "writing_run_created",
            "message": "Writing run created.",
            "payload_ref": None,
            "payload_json": {"writing_run_id": WRITING_RUN_ID},
            "created_at": "2026-07-11T03:02:00Z",
        },
        {
            "schema_version": 1,
            "task_event_id": "01JZWRITEEVT0000000000002",
            "task_id": WRITING_TASK_ID,
            "event_type": "progress",
            "message": "Humanizer pass completed, waiting for review.",
            "payload_ref": None,
            "payload_json": {"current_stage": "humanizer_pass", "retry_count": 1},
            "created_at": "2026-07-11T03:08:00Z",
        },
    ]
    STORE.feedback_records["01JZFDBK0000000000000001"] = {
        "schema_version": 1,
        "feedback_record_id": "01JZFDBK0000000000000001",
        "workspace_id": _workspace_or_default(),
        "target_type": "writing_run",
        "target_id": WRITING_RUN_ID,
        "feedback_type": "quality",
        "score": 0.82,
        "source": "quality_gate",
        "comment_ref": "object://quality-comments/01JZFDBK0000000000000001",
        "payload": {
            "quality_report_id": QUALITY_REPORT_ID,
            "summary": "质量门禁通过后保留了节奏与可读性指标。",
        },
        "created_at": "2026-07-11T03:10:00Z",
        "updated_at": "2026-07-11T03:10:00Z",
    }
    STORE.feedback_records["01JZFDBK0000000000000002"] = {
        "schema_version": 1,
        "feedback_record_id": "01JZFDBK0000000000000002",
        "workspace_id": _workspace_or_default(),
        "target_type": "quality_report",
        "target_id": QUALITY_REPORT_ID,
        "feedback_type": "style",
        "score": 0.64,
        "source": "critic",
        "comment_ref": "object://critic-comments/01JZFDBK0000000000000002",
        "payload": {
            "affected_text_ref": "object://drafts/01JZSECRUN00000000000003#p1",
            "summary": "金手指暗示仍偏早，可继续收敛。",
        },
        "created_at": "2026-07-11T03:11:00Z",
        "updated_at": "2026-07-11T03:11:00Z",
    }
    STORE.section_plan_tasks[CHAPTER_PLAN_ID] = {
        "schema_version": 1,
        "task_id": SECTION_PLAN_TASK_ID,
        "task_type": "create_section_plans",
        "workspace_id": _workspace_or_default(),
        "owner_module": "ai-worker",
        "input_refs": [f"object://chapter-plans/{CHAPTER_PLAN_ID}"],
        "output_refs": [
            "object://section-plans/01JZSECT0000000000000001",
            "object://section-plans/01JZSECT0000000000000002",
            "object://section-plans/01JZSECT0000000000000003",
        ],
        "status": "succeeded",
        "progress": 100,
        "idempotency_key": f"section-{CHAPTER_PLAN_ID}",
        "retry_count": 0,
        "error_code": None,
        "created_at": "2026-07-11T02:15:00Z",
        "started_at": "2026-07-11T02:15:05Z",
        "finished_at": "2026-07-11T02:18:00Z",
    }
    STORE.task_events_by_task[SECTION_PLAN_TASK_ID] = [
        {
            "schema_version": 1,
            "task_event_id": "01JZSECTEVT0000000000001",
            "task_id": SECTION_PLAN_TASK_ID,
            "event_type": "created",
            "message": "Section plans created.",
            "payload_ref": None,
            "payload_json": {"section_count": 3},
            "created_at": "2026-07-11T02:15:00Z",
        },
        {
            "schema_version": 1,
            "task_event_id": "01JZSECTEVT0000000000002",
            "task_id": SECTION_PLAN_TASK_ID,
            "event_type": "progress",
            "message": "Section plans generated.",
            "payload_ref": None,
            "payload_json": {"section_count": 3},
            "created_at": "2026-07-11T02:18:00Z",
        },
    ]


def default_workspace_id() -> str:
    return WORKSPACE_ID if WORKSPACE_ID in STORE.workspaces else next(iter(STORE.workspaces), WORKSPACE_ID)


def default_workspace() -> Optional[dict[str, Any]]:
    return STORE.workspaces.get(default_workspace_id())


def _workspace_or_default(workspace_id: Optional[str] = None) -> str:
    if workspace_id and workspace_id in STORE.workspaces:
        return workspace_id
    return default_workspace_id()


def create_workspace(payload: dict[str, Any]) -> dict[str, Any]:
    workspace_id = payload.get("slug") or str(ulid.new())
    now = utc_now()
    workspace = {
        "schema_version": 1,
        "workspace_id": workspace_id,
        "owner_user_id": USER_ID,
        "name": payload["name"],
        "slug": payload.get("slug", workspace_id),
        "default_language": payload.get("default_language", "zh-CN"),
        "status": "active",
        "created_at": now,
        "updated_at": now,
    }
    workspace_member = {
        "schema_version": 1,
        "workspace_member_id": str(ulid.new()),
        "workspace_id": workspace_id,
        "user_id": USER_ID,
        "role": "owner",
        "status": "active",
        "created_at": now,
        "updated_at": now,
    }
    STORE.workspaces[workspace_id] = workspace
    STORE.workspace_members[workspace_member["workspace_member_id"]] = workspace_member
    return {
        "workspace": workspace,
        "workspace_member": workspace_member,
    }


def get_workspace(workspace_id: str) -> Optional[dict[str, Any]]:
    workspace = STORE.workspaces.get(workspace_id)
    if not workspace:
        return None
    members = [item for item in STORE.workspace_members.values() if item["workspace_id"] == workspace_id]
    return {
        "workspace": workspace,
        "members": members,
    }


def get_workspace_home(workspace_id: str) -> Optional[dict[str, Any]]:
    workspace = STORE.workspaces.get(workspace_id)
    if not workspace:
        return None

    recent_tasks: list[dict[str, Any]] = []
    task_sources = [
        *[run["task"] for run in STORE.extraction_runs.values() if run.get("task")],
        *STORE.chapter_plan_tasks.values(),
        *STORE.section_plan_tasks.values(),
        *STORE.writing_run_tasks.values(),
    ]
    for item in task_sources:
        target_ref = item["output_refs"][0] if item.get("output_refs") else None
        recent_tasks.append(
            {
                "task_id": item["task_id"],
                "task_type": item["task_type"],
                "status": item["status"],
                "summary": f"{item['task_type']} 当前状态：{item['status']}。",
                "updated_at": item.get("finished_at") or item.get("started_at") or item["created_at"],
                "target_ref": target_ref,
            }
        )
    recent_tasks.sort(key=lambda item: item["updated_at"], reverse=True)

    pending_reviews = []
    for item in STORE.knowledge_objects.values():
        if item["workspace_id"] == workspace_id and item["review_status"] == "pending":
            pending_reviews.append(
                {
                    "review_id": item["object_id"],
                    "review_type": "knowledge_object",
                    "status": item["review_status"],
                    "title": f"{item['canonical_name']} 待知识审核",
                    "target_ref": f"object://knowledge-objects/{item['object_id']}",
                }
            )
    for writing_run_id, section_runs in STORE.section_runs_by_writing.items():
        writing_run = STORE.writing_runs.get(writing_run_id)
        if not writing_run or writing_run["workspace_id"] != workspace_id:
            continue
        for section in section_runs:
            if section["status"] in {"rewrite_required", "critic_review", "blocked"}:
                pending_reviews.append(
                    {
                        "review_id": section["section_run_id"],
                        "review_type": "section_run",
                        "status": section["status"],
                        "title": f"章节小节 {section['section_run_id']} 需人工处理",
                        "target_ref": f"object://section-runs/{section['section_run_id']}",
                    }
                )

    quick_links = [
        {
            "label": "进入来源书库",
            "route": "/sources",
            "resource_ref": f"object://source-books/{BOOK_ID}",
        },
        {
            "label": "进入写作工作台",
            "route": "/projects/demo-project/writing/demo-run",
            "resource_ref": f"object://writing-runs/{WRITING_RUN_ID}",
        },
        {
            "label": "进入配置中心",
            "route": "/configuration",
            "resource_ref": "object://configuration/default",
        },
    ]

    return {
        "workspace": workspace,
        "recent_tasks": recent_tasks[:4],
        "pending_reviews": pending_reviews[:4],
        "quick_links": quick_links,
    }


seed_phase_two_demo_data()


def create_book(payload: dict[str, Any], trace_id: str) -> dict[str, Any]:
    book_id = str(ulid.new())
    now = utc_now()
    book = {
        "schema_version": 1,
        "book_id": book_id,
        "workspace_id": _workspace_or_default(payload.get("workspace_id")),
        "title": payload["title"],
        "author_name": payload["author_name"],
        "source_type": payload["source_type"],
        "import_status": "uploaded",
        "trace_id": trace_id,
        "created_at": now,
        "updated_at": now,
    }
    STORE.books[book_id] = book
    STORE.chapters_by_book[book_id] = []
    return book


def get_book(book_id: str) -> Optional[dict[str, Any]]:
    return STORE.books.get(book_id)


def list_book_chapters(book_id: str) -> list[dict[str, Any]]:
    return STORE.chapters_by_book.get(book_id, [])


def create_extraction_run(book_id: str, trace_id: str) -> dict[str, Any]:
    if book_id == BOOK_ID:
        return STORE.extraction_runs[RUN_ID]

    run_id = str(ulid.new())
    task_id = str(ulid.new())
    now = utc_now()
    run = {
        "schema_version": 1,
        "run_id": run_id,
        "book_id": book_id,
        "workspace_id": _workspace_or_default(),
        "task_id": task_id,
        "status": "queued",
        "current_stage": "source_submission",
        "chapter_count": 0,
        "scene_count": 0,
        "object_count": 0,
        "evidence_count": 0,
        "low_confidence_count": 0,
        "errors": [],
        "created_at": now,
        "started_at": None,
        "finished_at": None,
        "task": {
            "schema_version": 1,
            "task_id": task_id,
            "task_type": "extract_knowledge",
            "workspace_id": _workspace_or_default(),
            "owner_module": "ai-worker",
            "input_refs": [f"object://source-books/{book_id}"],
            "output_refs": [f"object://extraction-runs/{run_id}"],
            "status": "queued",
            "progress": 0,
            "idempotency_key": f"extract-{book_id}",
            "retry_count": 0,
            "error_code": None,
            "created_at": now,
            "started_at": None,
            "finished_at": None,
        },
    }
    STORE.extraction_runs[run_id] = run
    STORE.knowledge_by_run[run_id] = []
    STORE.task_events_by_task[task_id] = [
        {
            "schema_version": 1,
            "task_event_id": str(ulid.new()),
            "task_id": task_id,
            "event_type": "created",
            "message": "Extraction run queued.",
            "payload_ref": None,
            "payload_json": {"trace_id": trace_id},
            "created_at": now,
        }
    ]
    return run


def get_extraction_run(run_id: str) -> Optional[dict[str, Any]]:
    return STORE.extraction_runs.get(run_id)


def get_extraction_report(run_id: str) -> Optional[dict[str, Any]]:
    run = STORE.extraction_runs.get(run_id)
    if not run:
        return None
    task_id = run["task_id"]
    return {
        "run": run,
        "task": run["task"],
        "events": STORE.task_events_by_task.get(task_id, []),
        "low_confidence_items": [
            obj for obj in list_knowledge_objects_for_run(run_id)
            if obj["confidence"] < 0.8 and obj["review_status"] == "pending"
        ],
    }


def list_knowledge_objects_for_run(run_id: str) -> list[dict[str, Any]]:
    return [STORE.knowledge_objects[object_id] for object_id in STORE.knowledge_by_run.get(run_id, [])]


def apply_review_action(
    object_id: str,
    action: str,
    target_object_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    obj = STORE.knowledge_objects.get(object_id)
    if not obj:
        return None

    if action == "approve":
        obj["review_status"] = "approved"
        obj["lifecycle_status"] = "approved"
    elif action == "reject":
        obj["review_status"] = "rejected"
        obj["lifecycle_status"] = "rejected"
    elif action == "merge_alias":
        obj["review_status"] = "merged"
        obj["lifecycle_status"] = "approved"
        obj["payload"]["merged_into"] = target_object_id
    elif action == "request_reextract":
        obj["review_status"] = "reextract_requested"
    else:
        raise ValueError(f"unsupported action: {action}")

    for run in STORE.extraction_runs.values():
        object_ids = STORE.knowledge_by_run.get(run["run_id"], [])
        if object_id in object_ids:
            pending = [
                STORE.knowledge_objects[current_id]
                for current_id in object_ids
                if STORE.knowledge_objects[current_id]["confidence"] < 0.8
                and STORE.knowledge_objects[current_id]["review_status"] == "pending"
            ]
            run["low_confidence_count"] = len(pending)
            if run["status"] == "requires_review" and not pending:
                run["status"] = "succeeded"
                run["current_stage"] = "knowledge_package_export"
                run["task"]["status"] = "succeeded"
                run["task"]["progress"] = 100
                run["finished_at"] = utc_now()
                run["task"]["finished_at"] = run["finished_at"]
            break
    return obj


def commit_knowledge_package(run_id: str) -> Optional[dict[str, Any]]:
    run = STORE.extraction_runs.get(run_id)
    if not run:
        return None
    run["status"] = "succeeded"
    run["current_stage"] = "knowledge_base_commit"
    run["task"]["status"] = "succeeded"
    run["task"]["progress"] = 100
    run["finished_at"] = utc_now()
    run["task"]["finished_at"] = run["finished_at"]
    return {
        "run_id": run_id,
        "status": run["status"],
        "committed_object_count": len(STORE.knowledge_by_run.get(run_id, [])),
    }


def get_graph_summary(book_id: Optional[str] = None) -> dict[str, Any]:
    selected_book_id = book_id or GRAPH_BOOK_ID
    return STORE.graph_summaries.get(selected_book_id, {
        "schema_version": 1,
        "book_id": selected_book_id,
        "node_count": 0,
        "edge_count": 0,
        "nodes": [],
    })


def list_chapter_plans_for_project(project_id: str) -> list[dict[str, Any]]:
    return sorted(
        [plan for plan in STORE.chapter_plans.values() if plan["project_id"] == project_id],
        key=lambda item: item["chapter_index"],
    )


def _sorted_store_items(values: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return sorted(values, key=lambda item: item[key])


def get_configuration_snapshot() -> dict[str, Any]:
    return {
        "default_model_profile_id": DEFAULT_MODEL_PROFILE_ID,
        "model_profiles": _sorted_store_items(list(STORE.model_profiles.values()), "model_profile_id"),
        "agent_model_assignments": _sorted_store_items(list(STORE.agent_model_assignments.values()), "assignment_id"),
        "quality_gate_profiles": _sorted_store_items(list(STORE.quality_gate_profiles.values()), "quality_gate_profile_id"),
        "prompt_versions": _sorted_store_items(list(STORE.prompt_versions), "agent_role"),
    }


def set_model_profile_enabled(model_profile_id: str, enabled: bool) -> Optional[dict[str, Any]]:
    profile = STORE.model_profiles.get(model_profile_id)
    if not profile:
        return None
    profile["enabled"] = enabled
    return {
        "model_profile": profile,
        "configuration_snapshot": get_configuration_snapshot(),
    }


def _get_agent_assignment(agent_role: str) -> Optional[dict[str, Any]]:
    for assignment in _sorted_store_items(list(STORE.agent_model_assignments.values()), "assignment_id"):
        if assignment["agent_role"] == agent_role and assignment["enabled"]:
            return assignment
    return None


def _build_provider_call(
    agent_role: str,
    model_profile_id: str,
    provider_name: str,
    status: str,
    retry_count: int,
    error_code: Optional[str] = None,
) -> dict[str, Any]:
    metrics = ROLE_CALL_METRICS.get(agent_role, {"prompt_tokens": 1000, "completion_tokens": 300, "latency_ms": 800, "cost_estimate": 0.1})
    completion_tokens = metrics["completion_tokens"] if status == "succeeded" else 0
    cost_estimate = metrics["cost_estimate"] if status == "succeeded" else round(metrics["cost_estimate"] / 2, 2)
    latency_ms = metrics["latency_ms"] if status == "succeeded" else max(200, metrics["latency_ms"] // 2)
    return {
        "schema_version": 1,
        "provider_call_id": str(ulid.new()),
        "agent_role": agent_role,
        "model_profile_id": model_profile_id,
        "provider_name": provider_name,
        "prompt_tokens": metrics["prompt_tokens"],
        "completion_tokens": completion_tokens,
        "latency_ms": latency_ms,
        "retry_count": retry_count,
        "cost_estimate": cost_estimate,
        "status": status,
        "error_code": error_code,
    }


def resolve_model_profile(
    agent_role: str,
    requested_profile_id: Optional[str] = None,
    require_structured_output: bool = False,
) -> dict[str, Any]:
    assignment = _get_agent_assignment(agent_role)
    primary_profile_id = requested_profile_id
    fallback_profile_ids: list[str] = []
    if requested_profile_id:
        profile = STORE.model_profiles.get(requested_profile_id)
        fallback_profile_ids = list(profile["fallback_profile_ids"]) if profile else []
    elif assignment:
        primary_profile_id = assignment["model_profile_id"]
        fallback_profile_ids = list(assignment["fallback_profile_ids"])

    retry_count = 0
    provider_calls: list[dict[str, Any]] = []
    for candidate_id in [primary_profile_id, *fallback_profile_ids]:
        if not candidate_id:
            continue
        profile = STORE.model_profiles.get(candidate_id)
        if not profile or not profile["enabled"]:
            continue
        if require_structured_output and not profile["supports_structured_output"]:
            retry_count += 1
            provider_calls.append(
                _build_provider_call(
                    agent_role,
                    candidate_id,
                    profile["provider_name"],
                    "failed",
                    retry_count,
                    "structured_output_validation_failed",
                )
            )
            continue
        return {
            "selected_profile": profile,
            "assignment": assignment,
            "retry_count": retry_count,
            "provider_calls": provider_calls,
        }

    return {
        "selected_profile": None,
        "assignment": assignment,
        "retry_count": retry_count,
        "provider_calls": provider_calls,
    }


def _build_model_cost(provider_calls: list[dict[str, Any]], retry_count: int) -> dict[str, Any]:
    successful_calls = [item for item in provider_calls if item["status"] == "succeeded"]
    by_role = {item["agent_role"]: item for item in successful_calls}
    return {
        "input_tokens": sum(item["prompt_tokens"] for item in successful_calls),
        "output_tokens": sum(item["completion_tokens"] for item in successful_calls),
        "estimated_total_cost": round(sum(item["cost_estimate"] for item in successful_calls), 2),
        "retry_count": retry_count,
        "writer_input_tokens": by_role.get("writer", {}).get("prompt_tokens", 0),
        "writer_output_tokens": by_role.get("writer", {}).get("completion_tokens", 0),
        "critic_input_tokens": by_role.get("critic", {}).get("prompt_tokens", 0),
        "critic_output_tokens": by_role.get("critic", {}).get("completion_tokens", 0),
        "humanizer_input_tokens": by_role.get("humanizer", {}).get("prompt_tokens", 0),
        "humanizer_output_tokens": by_role.get("humanizer", {}).get("completion_tokens", 0),
    }


def create_novel_project(payload: dict[str, Any], trace_id: str) -> dict[str, Any]:
    project_id = str(ulid.new())
    story_bible_id = str(ulid.new())
    now = utc_now()
    project = {
        "schema_version": 1,
        "project_id": project_id,
        "workspace_id": _workspace_or_default(payload.get("workspace_id")),
        "title": payload["title"],
        "genre_scope": payload["genre_scope"],
        "status": "planning",
        "story_bible_id": story_bible_id,
        "quality_gate_profile_id": payload.get("quality_gate_profile_id", QUALITY_GATE_PROFILE_ID),
        "allowed_knowledge_source_refs": payload.get(
            "allowed_knowledge_source_refs",
            [f"object://source-books/{BOOK_ID}"],
        ),
        "created_at": now,
        "updated_at": now,
    }
    story_bible = {
        "schema_version": 1,
        "story_bible_id": story_bible_id,
        "workspace_id": project["workspace_id"],
        "project_id": project_id,
        "version": 1,
        "status": "draft",
        "payload": payload.get(
            "story_bible_payload",
            {
                "premise": f"{payload['title']} 的故事设定待完善。",
                "protagonist": "待设定",
                "core_conflict": "待设定",
            },
        ),
        "trace_id": trace_id,
        "created_at": now,
        "updated_at": now,
    }
    STORE.novel_projects[project_id] = project
    STORE.story_bibles[story_bible_id] = story_bible
    return {
        "project": project,
        "story_bible": story_bible,
        "chapter_plans": [],
    }


def get_novel_project(project_id: str) -> Optional[dict[str, Any]]:
    project = STORE.novel_projects.get(project_id)
    if not project:
        return None
    story_bible = STORE.story_bibles.get(project["story_bible_id"])
    return {
        "project": project,
        "story_bible": story_bible,
        "chapter_plans": list_chapter_plans_for_project(project_id),
    }


def create_chapter_plan(payload: dict[str, Any], trace_id: str) -> Optional[dict[str, Any]]:
    project_id = payload["project_id"]
    if project_id not in STORE.novel_projects:
        return None

    chapter_plan_id = str(ulid.new())
    task_id = str(ulid.new())
    now = utc_now()
    chapter_plan = {
        "schema_version": 1,
        "chapter_plan_id": chapter_plan_id,
        "workspace_id": _workspace_or_default(payload.get("workspace_id")),
        "project_id": project_id,
        "chapter_index": payload["chapter_index"],
        "status": "queued",
        "target_word_count": payload["target_word_count"],
        "payload": payload.get("payload", {}),
        "created_at": now,
        "updated_at": now,
    }
    task = {
        "schema_version": 1,
        "task_id": task_id,
        "task_type": "create_chapter_plan",
        "workspace_id": chapter_plan["workspace_id"],
        "owner_module": "ai-worker",
        "input_refs": [f"object://novel-projects/{project_id}"],
        "output_refs": [f"object://chapter-plans/{chapter_plan_id}"],
        "status": "queued",
        "progress": 0,
        "idempotency_key": f"plan-{project_id}-{payload['chapter_index']}",
        "retry_count": 0,
        "error_code": None,
        "created_at": now,
        "started_at": None,
        "finished_at": None,
    }
    STORE.chapter_plans[chapter_plan_id] = chapter_plan
    STORE.chapter_plan_tasks[chapter_plan_id] = task
    STORE.section_plans_by_chapter[chapter_plan_id] = []
    STORE.task_events_by_task[task_id] = [
        {
            "schema_version": 1,
            "task_event_id": str(ulid.new()),
            "task_id": task_id,
            "event_type": "created",
            "message": "Chapter plan queued.",
            "payload_ref": None,
            "payload_json": {"trace_id": trace_id, "chapter_index": payload["chapter_index"]},
            "created_at": now,
        }
    ]
    return {
        "chapter_plan": chapter_plan,
        "task": task,
        "events": STORE.task_events_by_task[task_id],
    }


def get_chapter_plan(chapter_plan_id: str) -> Optional[dict[str, Any]]:
    chapter_plan = STORE.chapter_plans.get(chapter_plan_id)
    if not chapter_plan:
        return None
    task = STORE.chapter_plan_tasks.get(chapter_plan_id)
    events = STORE.task_events_by_task.get(task["task_id"], []) if task else []
    return {
        "chapter_plan": chapter_plan,
        "task": task,
        "events": events,
        "section_plan_count": len(STORE.section_plans_by_chapter.get(chapter_plan_id, [])),
    }


def list_section_plans(chapter_plan_id: str) -> Optional[dict[str, Any]]:
    if chapter_plan_id not in STORE.chapter_plans:
        return None
    task = STORE.section_plan_tasks.get(chapter_plan_id)
    events = STORE.task_events_by_task.get(task["task_id"], []) if task else []
    return {
        "chapter_plan_id": chapter_plan_id,
        "items": STORE.section_plans_by_chapter.get(chapter_plan_id, []),
        "task": task,
        "events": events,
    }


def create_section_plans(chapter_plan_id: str, section_count: int, trace_id: str) -> Optional[dict[str, Any]]:
    chapter_plan = STORE.chapter_plans.get(chapter_plan_id)
    if not chapter_plan:
        return None

    existing_items = STORE.section_plans_by_chapter.get(chapter_plan_id, [])
    if existing_items:
        task = STORE.section_plan_tasks.get(chapter_plan_id)
        events = STORE.task_events_by_task.get(task["task_id"], []) if task else []
        return {
            "chapter_plan_id": chapter_plan_id,
            "items": existing_items,
            "task": task,
            "events": events,
        }

    task_id = str(ulid.new())
    now = utc_now()
    roles = ["setup", "conflict", "turn", "payoff"]
    items = []
    for section_index, role in enumerate(roles[:section_count], start=1):
        items.append(
            {
                "schema_version": 1,
                "section_plan_id": str(ulid.new()),
                "workspace_id": chapter_plan["workspace_id"],
                "chapter_plan_id": chapter_plan_id,
                "section_index": section_index,
                "planning_role": role,
                "payload": {
                    "scene_goal": f"第 {section_index} 节聚焦 {role} 段落。",
                    "beats": [
                        {"index": 1, "summary": f"{role} 节奏起势"},
                        {"index": 2, "summary": f"{role} 节奏收束"},
                    ],
                },
                "created_at": now,
                "updated_at": now,
            }
        )

    task = {
        "schema_version": 1,
        "task_id": task_id,
        "task_type": "create_section_plans",
        "workspace_id": chapter_plan["workspace_id"],
        "owner_module": "ai-worker",
        "input_refs": [f"object://chapter-plans/{chapter_plan_id}"],
        "output_refs": [f"object://section-plans/{item['section_plan_id']}" for item in items],
        "status": "succeeded",
        "progress": 100,
        "idempotency_key": f"section-{chapter_plan_id}",
        "retry_count": 0,
        "error_code": None,
        "created_at": now,
        "started_at": now,
        "finished_at": now,
    }
    STORE.section_plans_by_chapter[chapter_plan_id] = items
    STORE.section_plan_tasks[chapter_plan_id] = task
    STORE.task_events_by_task[task_id] = [
        {
            "schema_version": 1,
            "task_event_id": str(ulid.new()),
            "task_id": task_id,
            "event_type": "created",
            "message": "Section plan generation started.",
            "payload_ref": None,
            "payload_json": {"trace_id": trace_id, "section_count": len(items)},
            "created_at": now,
        },
        {
            "schema_version": 1,
            "task_event_id": str(ulid.new()),
            "task_id": task_id,
            "event_type": "progress",
            "message": "Section plans generated.",
            "payload_ref": None,
            "payload_json": {"section_count": len(items)},
            "created_at": now,
        },
    ]
    chapter_plan["status"] = "requires_review"
    chapter_plan["updated_at"] = now
    return {
        "chapter_plan_id": chapter_plan_id,
        "items": items,
        "task": task,
        "events": STORE.task_events_by_task[task_id],
    }


def create_writing_run(payload: dict[str, Any], trace_id: str) -> Optional[dict[str, Any]]:
    project_id = payload["project_id"]
    chapter_plan_id = payload["chapter_plan_id"]
    if project_id not in STORE.novel_projects or chapter_plan_id not in STORE.chapter_plans:
        return None

    if chapter_plan_id == CHAPTER_PLAN_ID:
        return get_writing_run(WRITING_RUN_ID)

    writing_run_id = str(ulid.new())
    task_id = str(ulid.new())
    memory_package_id = str(ulid.new())
    prompt_package_id = str(ulid.new())
    quality_report_id = str(ulid.new())
    chapter_draft_id = str(ulid.new())
    now = utc_now()

    section_plans = STORE.section_plans_by_chapter.get(chapter_plan_id, [])
    if not section_plans:
        return None

    writer_resolution = resolve_model_profile("writer", payload.get("writer_model_profile_id"))
    critic_resolution = resolve_model_profile(
        "critic",
        payload.get("critic_model_profile_id"),
        require_structured_output=True,
    )
    humanizer_resolution = resolve_model_profile("humanizer", payload.get("humanizer_model_profile_id"))
    if not writer_resolution["selected_profile"] or not critic_resolution["selected_profile"] or not humanizer_resolution["selected_profile"]:
        return None

    provider_calls = [
        *writer_resolution["provider_calls"],
        _build_provider_call(
            "writer",
            writer_resolution["selected_profile"]["model_profile_id"],
            writer_resolution["selected_profile"]["provider_name"],
            "succeeded",
            writer_resolution["retry_count"],
        ),
        *critic_resolution["provider_calls"],
        _build_provider_call(
            "critic",
            critic_resolution["selected_profile"]["model_profile_id"],
            critic_resolution["selected_profile"]["provider_name"],
            "succeeded",
            critic_resolution["retry_count"],
        ),
        *humanizer_resolution["provider_calls"],
        _build_provider_call(
            "humanizer",
            humanizer_resolution["selected_profile"]["model_profile_id"],
            humanizer_resolution["selected_profile"]["provider_name"],
            "succeeded",
            humanizer_resolution["retry_count"],
        ),
    ]
    retry_count = max(
        writer_resolution["retry_count"],
        critic_resolution["retry_count"],
        humanizer_resolution["retry_count"],
    )

    STORE.memory_packages[memory_package_id] = {
        "schema_version": 1,
        "memory_package_id": memory_package_id,
        "workspace_id": _workspace_or_default(payload.get("workspace_id")),
        "project_id": project_id,
        "writing_run_id": writing_run_id,
        "summary": "已组装章节规划、故事设定与知识证据。",
        "source_refs": [
            f"object://chapter-plans/{chapter_plan_id}",
            f"object://story-bibles/{STORE.novel_projects[project_id]['story_bible_id']}",
        ],
        "created_at": now,
        "updated_at": now,
    }
    STORE.prompt_packages[prompt_package_id] = {
        "schema_version": 1,
        "prompt_package_id": prompt_package_id,
        "workspace_id": _workspace_or_default(payload.get("workspace_id")),
        "project_id": project_id,
        "writing_run_id": writing_run_id,
        "summary": "写手与润色阶段共用提示包。",
        "template_refs": [
            "prompt://writer/chapter-default",
            "prompt://critic/chapter-default",
            "prompt://humanizer/chapter-default",
        ],
        "created_at": now,
        "updated_at": now,
    }

    section_runs = []
    for section in section_plans:
        section_runs.append(
            {
                "schema_version": 1,
                "section_run_id": str(ulid.new()),
                "workspace_id": _workspace_or_default(payload.get("workspace_id")),
                "writing_run_id": writing_run_id,
                "section_plan_id": section["section_plan_id"],
                "status": "planned",
                "draft_object_ref": f"object://drafts/{section['section_plan_id']}",
                "critic_report_ref": f"object://critic-reports/{section['section_plan_id']}",
                "humanized_object_ref": f"object://humanized/{section['section_plan_id']}",
                "model_profile_id": writer_resolution["selected_profile"]["model_profile_id"],
                "beat_status": [
                    {"index": beat["index"], "status": "planned"}
                    for beat in section["payload"].get("beats", [])
                ],
                "writer_output": "",
                "critic_issues": [],
                "humanized_text": "",
                "created_at": now,
                "updated_at": now,
            }
        )

    task = {
        "schema_version": 1,
        "task_id": task_id,
        "task_type": "create_writing_run",
        "workspace_id": _workspace_or_default(payload.get("workspace_id")),
        "owner_module": "ai-worker",
        "input_refs": [
            f"object://chapter-plans/{chapter_plan_id}",
            f"object://memory-packages/{memory_package_id}",
            f"object://prompt-packages/{prompt_package_id}",
        ],
        "output_refs": [f"object://writing-runs/{writing_run_id}"],
        "status": "queued",
        "progress": 0,
        "idempotency_key": f"writing-{chapter_plan_id}",
        "retry_count": retry_count,
        "error_code": None,
        "created_at": now,
        "started_at": None,
        "finished_at": None,
    }
    writing_run = {
        "schema_version": 1,
        "writing_run_id": writing_run_id,
        "workspace_id": _workspace_or_default(payload.get("workspace_id")),
        "project_id": project_id,
        "chapter_plan_id": chapter_plan_id,
        "status": "queued",
        "task_id": task_id,
        "memory_package_id": memory_package_id,
        "prompt_package_id": prompt_package_id,
        "chapter_draft_id": chapter_draft_id,
        "quality_report_id": quality_report_id,
        "trace_id": trace_id,
        "current_stage": "queued",
        "writer_model_profile_id": writer_resolution["selected_profile"]["model_profile_id"],
        "critic_model_profile_id": critic_resolution["selected_profile"]["model_profile_id"],
        "humanizer_model_profile_id": humanizer_resolution["selected_profile"]["model_profile_id"],
        "assembled_chapter": "",
        "model_cost": _build_model_cost(provider_calls, retry_count),
        "accepted_into_manuscript_at": None,
        "accepted_chapter_ref": None,
        "chapter_snapshot_id": None,
        "manuscript_state_id": None,
        "created_at": now,
        "updated_at": now,
    }
    quality_report = {
        "schema_version": 1,
        "quality_report_id": quality_report_id,
        "workspace_id": _workspace_or_default(payload.get("workspace_id")),
        "writing_run_id": writing_run_id,
        "status": "queued",
        "ai_flavor_score": 0,
        "mobile_readability_score": 0,
        "originality_safety_score": 0,
        "human_review_required": False,
        "blocking_issues": [],
        "created_at": now,
        "updated_at": now,
    }

    STORE.writing_runs[writing_run_id] = writing_run
    STORE.writing_run_tasks[writing_run_id] = task
    STORE.provider_calls_by_writing[writing_run_id] = provider_calls
    STORE.section_runs_by_writing[writing_run_id] = section_runs
    STORE.quality_reports[quality_report_id] = quality_report
    STORE.task_events_by_task[task_id] = [
        {
            "schema_version": 1,
            "task_event_id": str(ulid.new()),
            "task_id": task_id,
            "event_type": "writing_run_created",
            "message": "Writing run queued.",
            "payload_ref": None,
            "payload_json": {"trace_id": trace_id, "writing_run_id": writing_run_id},
            "created_at": now,
        }
    ]
    return get_writing_run(writing_run_id)


def list_feedback_records(target_type: Optional[str] = None, target_id: Optional[str] = None) -> list[dict[str, Any]]:
    records = list(STORE.feedback_records.values())
    if target_type:
        records = [item for item in records if item["target_type"] == target_type]
    if target_id:
        records = [item for item in records if item["target_id"] == target_id]
    return sorted(records, key=lambda item: item["created_at"])


def _build_chapter_snapshot(writing_run: dict[str, Any], section_runs: list[dict[str, Any]], chapter_plan: Optional[dict[str, Any]], accepted_chapter_ref: str, created_at: str) -> dict[str, Any]:
    chapter_snapshot_id = writing_run.get("chapter_snapshot_id") or f"chapter-snapshot:{writing_run['writing_run_id']}"
    chapter_payload = chapter_plan.get("payload", {}) if chapter_plan else {}
    return {
        "schema_version": 1,
        "chapter_snapshot_id": chapter_snapshot_id,
        "writing_run_id": writing_run["writing_run_id"],
        "project_id": writing_run["project_id"],
        "chapter_plan_id": writing_run["chapter_plan_id"],
        "accepted_chapter_ref": accepted_chapter_ref,
        "chapter_title": chapter_payload.get("title", "已接受章节"),
        "chapter_text": writing_run["assembled_chapter"],
        "source_section_refs": [
            f"object://section-runs/{section_run['section_run_id']}"
            for section_run in section_runs
        ],
        "created_at": created_at,
    }


def _build_manuscript_state(writing_run: dict[str, Any], chapter_plan: Optional[dict[str, Any]], accepted_chapter_ref: str, updated_at: str) -> dict[str, Any]:
    manuscript_state_id = writing_run.get("manuscript_state_id") or f"manuscript-state:{writing_run['project_id']}"
    chapter_payload = chapter_plan.get("payload", {}) if chapter_plan else {}
    chapter_title = chapter_payload.get("title", "当前章节")
    return {
        "schema_version": 1,
        "manuscript_state_id": manuscript_state_id,
        "project_id": writing_run["project_id"],
        "writing_run_id": writing_run["writing_run_id"],
        "current_story_state": {
            "summary": f"第 {chapter_plan['chapter_index']} 章《{chapter_title}》已进入 manuscript，三年之约正式进入主线。" if chapter_plan else f"《{chapter_title}》已进入 manuscript。",
            "accepted_chapter_ref": accepted_chapter_ref,
            "quality_gate_status": "passed",
        },
        "character_dynamic_state": [
            {
                "character_name": "萧炎",
                "state_summary": "从公开羞辱中立下三年之约，主线动机被明确激活。",
            }
        ],
        "relationship_state": [
            {
                "subject": "萧炎",
                "object": "三年之约",
                "state_summary": "人物目标从承压转为正面回应，冲突升级为长期承诺。",
            }
        ],
        "hook_state": [
            {
                "hook_key": "core_conflict",
                "status": "active",
                "summary": "天赋跌落后的家族压力与三年之约仍是当前核心挂钩。",
            }
        ],
        "prior_summary_pack": [
            {"summary_index": 1, "summary": "议事堂压抑氛围与家族压力被建立。"},
            {"summary_index": 2, "summary": "纳兰家退婚消息引爆公开冲突。"},
            {"summary_index": 3, "summary": "主角在羞辱中立下三年之约。"},
        ],
        "updated_at": updated_at,
    }


def _acceptance_ready(writing_run: dict[str, Any], quality_report: Optional[dict[str, Any]], section_runs: list[dict[str, Any]]) -> bool:
    if not quality_report or not section_runs:
        return False
    has_feedback = any(item["target_id"] in {writing_run["writing_run_id"], writing_run["quality_report_id"]} for item in STORE.feedback_records.values())
    has_section_outputs = all(section_run["writer_output"] and section_run["humanized_text"] for section_run in section_runs)
    return has_feedback and has_section_outputs


def accept_chapter(writing_run_id: str, trace_id: str) -> Optional[dict[str, Any]]:
    writing_run = STORE.writing_runs.get(writing_run_id)
    if not writing_run:
        return None

    task = STORE.writing_run_tasks.get(writing_run_id)
    quality_report = STORE.quality_reports.get(writing_run["quality_report_id"])
    section_runs = STORE.section_runs_by_writing.get(writing_run_id, [])
    if not _acceptance_ready(writing_run, quality_report, section_runs):
        return False

    chapter_plan = STORE.chapter_plans.get(writing_run["chapter_plan_id"])
    now = utc_now()

    for section_run in section_runs:
        section_run["status"] = "beat_approved"
        section_run["beat_status"] = [
            {**beat, "status": "beat_approved"}
            for beat in section_run["beat_status"]
        ]
        section_run["critic_issues"] = []
        section_run["updated_at"] = now

    accepted_chapter_ref = writing_run["accepted_chapter_ref"] or f"object://manuscripts/{writing_run_id}/chapters/1"
    chapter_snapshot = _build_chapter_snapshot(writing_run, section_runs, chapter_plan, accepted_chapter_ref, now)
    manuscript_state = _build_manuscript_state(writing_run, chapter_plan, accepted_chapter_ref, now)
    STORE.chapter_snapshots[chapter_snapshot["chapter_snapshot_id"]] = chapter_snapshot
    STORE.manuscript_states_by_project[writing_run["project_id"]] = manuscript_state

    writing_run["status"] = "succeeded"
    writing_run["current_stage"] = "quality_gate"
    writing_run["accepted_into_manuscript_at"] = writing_run["accepted_into_manuscript_at"] or now
    writing_run["accepted_chapter_ref"] = accepted_chapter_ref
    writing_run["chapter_snapshot_id"] = chapter_snapshot["chapter_snapshot_id"]
    writing_run["manuscript_state_id"] = manuscript_state["manuscript_state_id"]
    writing_run["updated_at"] = now

    if task:
        task["status"] = "succeeded"
        task["progress"] = 100
        task["finished_at"] = task["finished_at"] or now

    if quality_report:
        quality_report["status"] = "passed"
        quality_report["human_review_required"] = False
        quality_report["blocking_issues"] = []
        quality_report["updated_at"] = now

    run_records = list_feedback_records("writing_run", writing_run_id)
    run_feedback_types = {item["feedback_type"] for item in run_records}
    if "acceptance" not in run_feedback_types:
        acceptance_id = str(ulid.new())
        STORE.feedback_records[acceptance_id] = {
            "schema_version": 1,
            "feedback_record_id": acceptance_id,
            "workspace_id": writing_run["workspace_id"],
            "target_type": "writing_run",
            "target_id": writing_run_id,
            "feedback_type": "acceptance",
            "score": 1.0,
            "source": "human_review",
            "comment_ref": f"object://feedback-comments/{acceptance_id}",
            "payload": {
                "accepted_chapter_ref": writing_run["accepted_chapter_ref"],
                "chapter_snapshot_id": chapter_snapshot["chapter_snapshot_id"],
                "manuscript_state_id": manuscript_state["manuscript_state_id"],
                "summary": "人工复核已接受本章进入 manuscript。",
            },
            "created_at": now,
            "updated_at": now,
        }
    if "cost" not in run_feedback_types:
        cost_id = str(ulid.new())
        STORE.feedback_records[cost_id] = {
            "schema_version": 1,
            "feedback_record_id": cost_id,
            "workspace_id": writing_run["workspace_id"],
            "target_type": "writing_run",
            "target_id": writing_run_id,
            "feedback_type": "cost",
            "score": 0.78,
            "source": "system",
            "comment_ref": None,
            "payload": {
                "estimated_total_cost": writing_run["model_cost"]["estimated_total_cost"],
                "retry_count": writing_run["model_cost"]["retry_count"],
            },
            "created_at": now,
            "updated_at": now,
        }

    if task:
        events = STORE.task_events_by_task.setdefault(task["task_id"], [])
        if not any(event["event_type"] == "chapter_accepted" for event in events):
            events.append(
                {
                    "schema_version": 1,
                    "task_event_id": str(ulid.new()),
                    "task_id": task["task_id"],
                    "event_type": "chapter_accepted",
                    "message": "Chapter accepted into manuscript.",
                    "payload_ref": None,
                    "payload_json": {
                        "trace_id": trace_id,
                        "accepted_chapter_ref": writing_run["accepted_chapter_ref"],
                        "chapter_snapshot_id": chapter_snapshot["chapter_snapshot_id"],
                        "manuscript_state_id": manuscript_state["manuscript_state_id"],
                    },
                    "created_at": now,
                }
            )

    return get_writing_run(writing_run_id)


def get_writing_run(writing_run_id: str) -> Optional[dict[str, Any]]:
    writing_run = STORE.writing_runs.get(writing_run_id)
    if not writing_run:
        return None
    task = STORE.writing_run_tasks.get(writing_run_id)
    memory_package = STORE.memory_packages.get(writing_run["memory_package_id"])
    prompt_package = STORE.prompt_packages.get(writing_run["prompt_package_id"])
    quality_report = STORE.quality_reports.get(writing_run["quality_report_id"])
    chapter_snapshot = STORE.chapter_snapshots.get(writing_run.get("chapter_snapshot_id", "")) if writing_run.get("chapter_snapshot_id") else None
    manuscript_state = STORE.manuscript_states_by_project.get(writing_run["project_id"])
    events = STORE.task_events_by_task.get(task["task_id"], []) if task else []
    return {
        "writing_run": {
            **writing_run,
            "chapter_snapshot": chapter_snapshot,
            "manuscript_state": manuscript_state,
        },
        "task": task,
        "events": events,
        "memory_package": memory_package,
        "prompt_package": prompt_package,
        "section_runs": STORE.section_runs_by_writing.get(writing_run_id, []),
        "quality_report": quality_report,
        "provider_calls": STORE.provider_calls_by_writing.get(writing_run_id, []),
        "feedback_records": [
            item
            for item in list_feedback_records()
            if item["target_id"] in {writing_run_id, writing_run["quality_report_id"]}
        ],
        "chapter_snapshot": chapter_snapshot,
        "manuscript_state": manuscript_state,
    }


def get_quality_report(quality_report_id: str) -> Optional[dict[str, Any]]:
    return STORE.quality_reports.get(quality_report_id)

