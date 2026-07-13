from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from worker.core_store import load_phase_two_store
from worker.llm_json import generate_json


WORKSPACE_ID = "01JZWORKSPACE0000000000001"
PROJECT_ID = "01JZPROJECT000000000000001"
CHAPTER_PLAN_ID = "01JZCHPLAN000000000000001"
CHAPTER_PLAN_TASK_ID = "01JZPLANTASK0000000000001"
SECTION_PLAN_TASK_ID = "01JZSECTTASK0000000000001"
TRACE_ID = "01JZTRC000000000000000002"

PLANNING_STAGES = [
    "story_bible_snapshot",
    "chapter_outline",
    "scene_expansion",
    "beat_alignment",
    "quality_review",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_create_chapter_plan_command(
    project_id: str = PROJECT_ID,
    chapter_plan_id: str = CHAPTER_PLAN_ID,
    task_id: str = CHAPTER_PLAN_TASK_ID,
    trace_id: str = TRACE_ID,
    dispatch_token: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "command_id": f"cmd-{chapter_plan_id}",
        "task_id": task_id,
        "task_type": "create_chapter_plan",
        "workspace_id": WORKSPACE_ID,
        "project_id": project_id,
        "chapter_plan_id": chapter_plan_id,
        "chapter_index": 1,
        "target_word_count": 3200,
        "trace_id": trace_id,
        "dispatch_token": dispatch_token,
        "requested_by": "core-service",
    }


def build_create_section_plans_command(
    chapter_plan_id: str = CHAPTER_PLAN_ID,
    task_id: str = SECTION_PLAN_TASK_ID,
    trace_id: str = TRACE_ID,
    dispatch_token: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "command_id": f"cmd-sections-{chapter_plan_id}",
        "task_id": task_id,
        "task_type": "create_section_plans",
        "workspace_id": WORKSPACE_ID,
        "chapter_plan_id": chapter_plan_id,
        "section_count": 3,
        "trace_id": trace_id,
        "dispatch_token": dispatch_token,
        "requested_by": "core-service",
    }


def build_chapter_plan_fixture(command: dict[str, Any]) -> dict[str, Any]:
    chapter_plan_id = command["chapter_plan_id"]
    project_id = command["project_id"]
    return {
        "schema_version": 1,
        "chapter_plan": {
            "schema_version": 1,
            "chapter_plan_id": chapter_plan_id,
            "workspace_id": command["workspace_id"],
            "project_id": project_id,
            "chapter_index": command["chapter_index"],
            "status": "requires_review",
            "target_word_count": command["target_word_count"],
            "payload": {
                "title": "乌坦城风起",
                "summary": "主角在第一章完成进入主线前的势能铺垫。",
            },
            "created_at": "2026-07-11T02:10:00Z",
            "updated_at": "2026-07-11T02:12:00Z",
        },
        "task": {
            "schema_version": 1,
            "task_id": command["task_id"],
            "task_type": command["task_type"],
            "workspace_id": command["workspace_id"],
            "owner_module": "ai-worker",
            "input_refs": [f"object://novel-projects/{project_id}"],
            "output_refs": [f"object://chapter-plans/{chapter_plan_id}"],
            "status": "requires_review",
            "progress": 100,
            "idempotency_key": f"plan-{project_id}-{command['chapter_index']}",
            "retry_count": 0,
            "error_code": None,
            "created_at": "2026-07-11T02:10:00Z",
            "started_at": "2026-07-11T02:10:03Z",
            "finished_at": "2026-07-11T02:12:00Z",
        },
        "events": [
            {
                "schema_version": 1,
                "task_event_id": "01JZPLANEVT0000000000001",
                "task_id": command["task_id"],
                "event_type": "created",
                "message": "Chapter plan created.",
                "payload_ref": None,
                "payload_json": {"chapter_index": command["chapter_index"]},
                "created_at": "2026-07-11T02:10:00Z",
            },
            {
                "schema_version": 1,
                "task_event_id": "01JZPLANEVT0000000000002",
                "task_id": command["task_id"],
                "event_type": "progress",
                "message": "Chapter plan ready for review.",
                "payload_ref": None,
                "payload_json": {
                    "status": "requires_review",
                    "planning_stages": PLANNING_STAGES,
                },
                "created_at": "2026-07-11T02:12:00Z",
            },
        ],
    }


def build_section_plan_fixture(command: dict[str, Any]) -> dict[str, Any]:
    chapter_plan_id = command["chapter_plan_id"]
    items = [
        {
            "schema_version": 1,
            "section_plan_id": "01JZSECT0000000000000001",
            "workspace_id": command["workspace_id"],
            "chapter_plan_id": chapter_plan_id,
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
            "workspace_id": command["workspace_id"],
            "chapter_plan_id": chapter_plan_id,
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
            "workspace_id": command["workspace_id"],
            "chapter_plan_id": chapter_plan_id,
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
    return {
        "schema_version": 1,
        "chapter_plan_id": chapter_plan_id,
        "items": items,
        "task": {
            "schema_version": 1,
            "task_id": command["task_id"],
            "task_type": command["task_type"],
            "workspace_id": command["workspace_id"],
            "owner_module": "ai-worker",
            "input_refs": [f"object://chapter-plans/{chapter_plan_id}"],
            "output_refs": [f"object://section-plans/{item['section_plan_id']}" for item in items],
            "status": "succeeded",
            "progress": 100,
            "idempotency_key": f"section-{chapter_plan_id}",
            "retry_count": 0,
            "error_code": None,
            "created_at": "2026-07-11T02:15:00Z",
            "started_at": "2026-07-11T02:15:05Z",
            "finished_at": "2026-07-11T02:18:00Z",
        },
        "events": [
            {
                "schema_version": 1,
                "task_event_id": "01JZSECTEVT0000000000001",
                "task_id": command["task_id"],
                "event_type": "created",
                "message": "Section plans created.",
                "payload_ref": None,
                "payload_json": {"section_count": len(items)},
                "created_at": "2026-07-11T02:15:00Z",
            },
            {
                "schema_version": 1,
                "task_event_id": "01JZSECTEVT0000000000002",
                "task_id": command["task_id"],
                "event_type": "progress",
                "message": "Section plans generated.",
                "payload_ref": None,
                "payload_json": {
                    "section_count": len(items),
                    "planning_stages": PLANNING_STAGES,
                },
                "created_at": "2026-07-11T02:18:00Z",
            },
        ],
    }


def _generate_chapter_plan(story_bible: dict[str, Any] | None, chapter_index: int, knowledge_context: str) -> dict[str, Any]:
    bible_payload = (story_bible or {}).get("payload", {})
    premise = bible_payload.get("premise", "")
    protagonist = bible_payload.get("protagonist", "主角")
    core_conflict = bible_payload.get("core_conflict", "")
    knowledge_block = f"\n【可用拆书知识】\n{knowledge_context}\n" if knowledge_context.strip() else ""
    generated = generate_json(
        system="你是中文网文章节规划师。基于故事圣经与已确立设定，为指定章节输出规划。只输出 JSON：{\"title\":\"章节标题\",\"summary\":\"本章推进摘要\"}，不要解释。",
        user=f"故事前提：{premise}\n主角：{protagonist}\n核心冲突：{core_conflict}\n当前章节：第{chapter_index}章{knowledge_block}",
    )
    if generated and isinstance(generated.get("title"), str) and generated.get("title").strip():
        return {"title": generated["title"].strip(), "summary": str(generated.get("summary", "")).strip() or f"{protagonist}在第{chapter_index}章推进{core_conflict or premise}。"}
    # 确定性 fallback：从 story bible 派生，非乌坦城写死
    stage = ["铺垫", "冲突", "转折", "推进", "高潮"][min(chapter_index - 1, 4)]
    return {
        "title": f"{protagonist}·第{chapter_index}章·{stage}",
        "summary": f"{protagonist}在第{chapter_index}章围绕「{core_conflict or premise}」展开{stage}，推进主线。",
    }


def run_create_chapter_plan(command: dict[str, Any]) -> dict[str, Any]:
    store = load_phase_two_store()
    chapter_plan_id = command["chapter_plan_id"]
    chapter_plan = store.STORE.chapter_plans.get(chapter_plan_id)
    metrics = {
        "planning_stages": PLANNING_STAGES,
        "current_stage": "quality_review",
        "chapter_index": command["chapter_index"],
        "target_word_count": command["target_word_count"],
        "generated_at": utc_now(),
    }
    if chapter_plan:
        project = store.STORE.novel_projects.get(command["project_id"])
        story_bible = store.STORE.story_bibles.get(project["story_bible_id"]) if project else None
        allowed_refs = project.get("allowed_knowledge_source_refs", []) if project else []
        knowledge = store.build_knowledge_context(allowed_refs)
        generated = _generate_chapter_plan(story_bible, command["chapter_index"], knowledge["context_text"])
        chapter_plan["payload"] = {
            **chapter_plan.get("payload", {}),
            "title": generated["title"],
            "summary": generated["summary"],
            "planning_stages": PLANNING_STAGES,
            "current_stage": "quality_review",
        }
    task = store.apply_task_execution_result(
        command["task_id"],
        "requires_review",
        [f"object://chapter-plans/{chapter_plan_id}"],
        metrics,
        trace_id=command["trace_id"],
        dispatch_token=command.get("dispatch_token"),
    )
    return {
        "schema_version": 1,
        "task_id": command["task_id"],
        "status": task["status"] if task else "requires_review",
        "output_refs": task["output_refs"] if task else [f"object://chapter-plans/{chapter_plan_id}"],
        "metrics": metrics,
        "errors": [],
        "trace_id": command["trace_id"],
    }


def _generate_section_plans(chapter_plan: dict[str, Any], story_bible: dict[str, Any] | None, knowledge_context: str, section_count: int, workspace_id: str) -> list[dict[str, Any]]:
    chapter_plan_id = chapter_plan["chapter_plan_id"]
    chapter_summary = chapter_plan.get("payload", {}).get("summary", "")
    protagonist = (story_bible or {}).get("payload", {}).get("protagonist", "主角")
    core_conflict = (story_bible or {}).get("payload", {}).get("core_conflict", "")
    roles = ["setup", "conflict", "turn"]
    knowledge_block = f"\n【可用拆书知识】\n{knowledge_context}\n" if knowledge_context.strip() else ""
    generated = generate_json(
        system="你是中文网文分节规划师。为本章输出 setup/conflict/turn 三段分节，每段含 scene_goal 与 2 个 beats。只输出 JSON：{\"sections\":[{\"scene_goal\":\"\",\"beats\":[\"\",\"\"]}]}，不要解释。",
        user=f"本章摘要：{chapter_summary}\n主角：{protagonist}\n核心冲突：{core_conflict}{knowledge_block}",
    )
    gen_sections = generated.get("sections") if isinstance(generated, dict) else None
    now = utc_now()
    items: list[dict[str, Any]] = []
    for index in range(1, section_count + 1):
        role = roles[min(index - 1, len(roles) - 1)]
        gen = gen_sections[index - 1] if isinstance(gen_sections, list) and len(gen_sections) >= index and isinstance(gen_sections[index - 1], dict) else None
        if gen and str(gen.get("scene_goal", "")).strip():
            scene_goal = str(gen["scene_goal"]).strip()
            raw_beats = gen.get("beats", []) if isinstance(gen.get("beats"), list) else []
            beats = [{"index": bi + 1, "summary": str(b).strip()} for bi, b in enumerate(raw_beats) if str(b).strip()] or [{"index": 1, "summary": scene_goal}]
        else:
            phase = {"setup": "铺垫", "conflict": "冲突升级", "turn": "转折"}[role]
            scene_goal = f"{protagonist}在本节推进{core_conflict or chapter_summary or '主线'}的{phase}"
            beats = [
                {"index": 1, "summary": f"{protagonist}面对{phase}情境"},
                {"index": 2, "summary": f"{phase}推动局势变化"},
            ]
        items.append({
            "schema_version": 1,
            "section_plan_id": f"{chapter_plan_id}SEC{index}",
            "workspace_id": workspace_id,
            "chapter_plan_id": chapter_plan_id,
            "section_index": index,
            "planning_role": role,
            "payload": {"scene_goal": scene_goal, "beats": beats},
            "created_at": now,
            "updated_at": now,
        })
    return items


def run_create_section_plans(command: dict[str, Any]) -> dict[str, Any]:
    store = load_phase_two_store()
    chapter_plan_id = command["chapter_plan_id"]
    items = store.STORE.section_plans_by_chapter.get(chapter_plan_id, [])
    if not items:
        chapter_plan = store.STORE.chapter_plans.get(chapter_plan_id)
        if chapter_plan:
            project = store.STORE.novel_projects.get(chapter_plan.get("project_id"))
            story_bible = store.STORE.story_bibles.get(project["story_bible_id"]) if project else None
            allowed_refs = project.get("allowed_knowledge_source_refs", []) if project else []
            knowledge = store.build_knowledge_context(allowed_refs)
            items = _generate_section_plans(chapter_plan, story_bible, knowledge["context_text"], command.get("section_count", 3), command["workspace_id"])
            store.STORE.section_plans_by_chapter[chapter_plan_id] = items
    metrics = {
        "planning_stages": PLANNING_STAGES,
        "current_stage": "quality_review",
        "section_count": len(items),
        "generated_at": utc_now(),
    }
    task = store.apply_task_execution_result(
        command["task_id"],
        "succeeded",
        [f"object://section-plans/{item['section_plan_id']}" for item in items],
        metrics,
        trace_id=command["trace_id"],
        dispatch_token=command.get("dispatch_token"),
    )
    return {
        "schema_version": 1,
        "task_id": command["task_id"],
        "status": task["status"] if task else "succeeded",
        "output_refs": task["output_refs"] if task else [f"object://section-plans/{item['section_plan_id']}" for item in items],
        "metrics": metrics,
        "errors": [],
        "trace_id": command["trace_id"],
    }
