from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from worker.core_store import load_phase_two_store


WORKSPACE_ID = "01JZWORKSPACE0000000000001"
BOOK_ID = "01JZBOOK000000000000000001"
RUN_ID = "01JZRUN0000000000000000001"
TASK_ID = "01JZTASK000000000000000001"
TRACE_ID = "01JZTRC000000000000000001"

PIPELINE_STAGES = [
    "source_submission",
    "book_registration",
    "file_intake",
    "text_normalization",
    "chapter_segmentation",
    "scene_segmentation",
    "knowledge_extraction",
    "evidence_binding",
    "object_normalization",
    "quality_review",
]


class ChapterAnalysisProviderError(RuntimeError):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_extract_knowledge_command(
    book_id: str = BOOK_ID,
    run_id: str = RUN_ID,
    task_id: str = TASK_ID,
    trace_id: str = TRACE_ID,
    dispatch_token: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "command_id": f"cmd-{run_id}",
        "task_id": task_id,
        "task_type": "extract_knowledge",
        "workspace_id": WORKSPACE_ID,
        "input_refs": [f"object://source-books/{book_id}", f"object://extraction-runs/{run_id}"],
        "idempotency_key": f"extract-{book_id}-001",
        "trace_id": trace_id,
        "dispatch_token": dispatch_token,
        "requested_by": "core-service",
    }


def build_extraction_fixture(command: dict[str, Any]) -> dict[str, Any]:
    run_ref = next(
        ref for ref in command["input_refs"]
        if ref.startswith("object://extraction-runs/")
    )
    book_ref = next(
        ref for ref in command["input_refs"]
        if ref.startswith("object://source-books/")
    )
    run_id = run_ref.rsplit("/", 1)[-1]
    book_id = book_ref.rsplit("/", 1)[-1]

    low_confidence_items = [
        {
            "schema_version": 1,
            "object_id": "01JZOBJ0000000000000000001",
            "workspace_id": command["workspace_id"],
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
            "workspace_id": command["workspace_id"],
            "object_type": "mentor",
            "canonical_name": "Yao Lao",
            "lifecycle_status": "candidate",
            "review_status": "pending",
            "confidence": 0.44,
            "evidence_refs": ["evidence://01JZEVIDENCE0000000000002"],
            "payload": {"schema_version": 1, "aliases": ["Old Yao"]},
        },
    ]
    approved_items = [
        {
            "schema_version": 1,
            "object_id": "01JZOBJ0000000000000000003",
            "workspace_id": command["workspace_id"],
            "object_type": "clan",
            "canonical_name": "Xiao Clan",
            "lifecycle_status": "approved",
            "review_status": "approved",
            "confidence": 0.97,
            "evidence_refs": ["evidence://01JZEVIDENCE0000000000003"],
            "payload": {"schema_version": 1, "aliases": []},
        }
    ]

    knowledge_package_ref = f"object://knowledge-packages/{run_id}"
    graph_package_ref = f"object://graph-packages/{book_id}"
    extraction_report_ref = f"object://extraction-reports/{run_id}"
    quality_report_ref = f"object://quality-reports/{run_id}"

    return {
        "schema_version": 1,
        "run": {
            "schema_version": 1,
            "run_id": run_id,
            "book_id": book_id,
            "workspace_id": command["workspace_id"],
            "task_id": command["task_id"],
            "status": "requires_review",
            "current_stage": "quality_review",
            "chapter_count": 2,
            "scene_count": 6,
            "object_count": 3,
            "evidence_count": 3,
            "low_confidence_count": 2,
            "knowledge_package_ref": knowledge_package_ref,
            "graph_package_ref": graph_package_ref,
            "extraction_report_ref": extraction_report_ref,
            "quality_report_ref": quality_report_ref,
            "errors": [],
            "created_at": "2026-07-11T00:00:00Z",
            "started_at": "2026-07-11T00:00:05Z",
            "finished_at": None,
        },
        "task": {
            "schema_version": 1,
            "task_id": command["task_id"],
            "task_type": command["task_type"],
            "workspace_id": command["workspace_id"],
            "owner_module": "ai-worker",
            "input_refs": command["input_refs"],
            "output_refs": [
                f"object://extraction-runs/{run_id}",
                knowledge_package_ref,
                graph_package_ref,
                extraction_report_ref,
                quality_report_ref,
            ],
            "status": "requires_review",
            "progress": 88,
            "idempotency_key": command["idempotency_key"],
            "retry_count": 0,
            "error_code": None,
            "created_at": "2026-07-11T00:00:00Z",
            "started_at": "2026-07-11T00:00:05Z",
            "finished_at": None,
        },
        "events": [
            {
                "schema_version": 1,
                "task_event_id": "01JZEVT000000000000000001",
                "task_id": command["task_id"],
                "event_type": "created",
                "message": "Extraction run created.",
                "payload_ref": None,
                "payload_json": None,
                "created_at": "2026-07-11T00:00:00Z",
            },
            {
                "schema_version": 1,
                "task_event_id": "01JZEVT000000000000000002",
                "task_id": command["task_id"],
                "event_type": "progress",
                "message": "Low confidence objects require review.",
                "payload_ref": extraction_report_ref,
                "payload_json": {
                    "current_stage": "quality_review",
                    "low_confidence_count": 2,
                    "pipeline_stages": PIPELINE_STAGES,
                },
                "created_at": "2026-07-11T00:01:00Z",
            },
        ],
        "knowledge_objects": low_confidence_items + approved_items,
        "graph_summary": {
            "schema_version": 1,
            "book_id": book_id,
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
        },
    }


def _strip_json_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _message_content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        fragments = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                fragments.append(str(item.get("text", "")))
            elif isinstance(item, dict) and "text" in item:
                fragments.append(str(item["text"]))
            elif isinstance(item, str):
                fragments.append(item)
        text = "".join(fragments).strip()
        if text:
            return text
    raise ChapterAnalysisProviderError("provider_response_invalid", "provider response missing message content")


def _openai_json_completion(*, model_profile: dict[str, Any], system: str, user: str) -> dict[str, Any]:
    base_url = os.getenv("NOVELIST_LLM_BASE_URL")
    api_key = os.getenv("NOVELIST_LLM_API_KEY")
    if not base_url or not api_key:
        raise ChapterAnalysisProviderError("provider_credentials_missing", "provider credentials missing")
    endpoint = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps(
        {
            "model": model_profile["provider_model_name"],
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.3,
            "max_tokens": 1800,
            "response_format": {"type": "json_object"},
        }
    ).encode("utf-8")
    request = Request(
        endpoint,
        data=body,
        headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=90) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise ChapterAnalysisProviderError("provider_http_error", f"provider request failed: {exc.code}") from exc
    except URLError as exc:
        raise ChapterAnalysisProviderError("provider_network_error", "provider request failed") from exc
    except TimeoutError as exc:
        raise ChapterAnalysisProviderError("provider_timeout", "provider request timed out") from exc
    try:
        content = _message_content_to_text(payload["choices"][0]["message"]["content"])
        return json.loads(_strip_json_fence(content))
    except ChapterAnalysisProviderError:
        raise
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise ChapterAnalysisProviderError("provider_response_invalid", "provider response missing valid JSON") from exc


def _object_ref_map(knowledge_objects: list[dict[str, Any]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for item in knowledge_objects:
        object_ref = f"object://knowledge-objects/{item['object_id']}"
        mapping[item["canonical_name"].strip().lower()] = object_ref
        for alias in item.get("payload", {}).get("aliases", []):
            if isinstance(alias, str) and alias.strip():
                mapping[alias.strip().lower()] = object_ref
    return mapping


def _participant_refs(names: list[Any], object_refs: dict[str, str], fallback_ref: str) -> list[str]:
    refs: list[str] = []
    for name in names:
        if not isinstance(name, str) or not name.strip():
            continue
        refs.append(object_refs.get(name.strip().lower(), name.strip()))
    if not refs:
        refs.append(fallback_ref)
    return refs


def _object_ref(name: Any, object_refs: dict[str, str], fallback_ref: str) -> str:
    if isinstance(name, str) and name.strip():
        return object_refs.get(name.strip().lower(), name.strip())
    return fallback_ref


def _text(value: Any, default: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return default


def _confidence(value: Any, default: float) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return default


def _intensity(value: Any, default: float) -> float:
    return _confidence(value, default)


def _escalation_level(value: Any, default: int) -> int:
    try:
        parsed = int(value)
        return max(0, parsed)
    except (TypeError, ValueError):
        return default


def _chapter_excerpt(chapter: dict[str, Any]) -> str:
    return (chapter.get("text_excerpt") or chapter.get("raw_text") or "")[:160]


def _build_fallback_chapter_analysis(chapter: dict[str, Any], chapter_index: int, knowledge_objects: list[dict[str, Any]]) -> dict[str, Any]:
    protagonist = knowledge_objects[0]["canonical_name"] if knowledge_objects else "主角"
    pressure = knowledge_objects[-1]["canonical_name"] if knowledge_objects else "外部压力"
    excerpt = _chapter_excerpt(chapter) or "章节主场景推进。"
    return {
        "summary": excerpt,
        "scenes": [
            {
                "title": f"{chapter.get('title', f'第{chapter_index}章')}主场景",
                "summary": excerpt,
                "text_range": chapter.get("text_range") or f"c{chapter_index}:p1-p1",
                "participants": [protagonist, pressure],
                "event": {
                    "event_type": "turning_point",
                    "cause": "主角遭遇新的压力或线索。",
                    "action": excerpt,
                    "result": "场景目标被推进。",
                    "consequence": "后续冲突获得动机。",
                    "participants": [protagonist],
                    "confidence": 0.78,
                },
                "conflict": {
                    "parties": [protagonist, pressure],
                    "objective": "在压力下保住目标并寻找突破口。",
                    "pressure": "外部规则或人物施压。",
                    "escalation_level": 2 + chapter_index,
                    "resolution_state": "open",
                    "confidence": 0.76,
                },
                "hook": {
                    "hook_type": "growth_question",
                    "open_question": "主角如何从当前压力中反转？",
                    "introduced_at": f"chapter:{chapter.get('chapter_index', chapter_index)}",
                    "expected_resolution_range": "future_chapters",
                    "confidence": 0.74,
                },
                "reward": {
                    "reward_type": "anticipation",
                    "beneficiary_character_id": protagonist,
                    "reader_effect": "制造后续反击期待。",
                    "intensity": 0.68,
                    "payoff_target": "future_reversal",
                    "confidence": 0.72,
                },
                "climax": {
                    "scope_type": "chapter",
                    "intensity": 0.8,
                    "aftermath": "章节留下后续解决期待。",
                    "confidence": 0.73,
                },
            }
        ],
        "relationships": [
            {
                "source": protagonist,
                "relation_type": "pressured_by",
                "target": pressure,
                "confidence": 0.7,
            }
        ],
    }


def _build_chapter_prompt(chapter: dict[str, Any]) -> str:
    chapter_index = chapter.get("chapter_index", 1)
    raw_text = (chapter.get("raw_text") or chapter.get("text_excerpt") or "")[:6000]
    return (
        "按小说结构分析当前章节。只输出 JSON 对象，不要解释。\n"
        "JSON 结构：{\n"
        '  "summary": "章节摘要",\n'
        '  "scenes": [\n'
        "    {\n"
        '      "title": "场景标题",\n'
        '      "summary": "场景摘要",\n'
        '      "text_range": "c%d:p1-p2",\n'
        '      "participants": ["人物或势力"],\n'
        '      "event": {"event_type": "", "cause": "", "action": "", "result": "", "consequence": "", "participants": [""], "confidence": 0.0},\n'
        '      "conflict": {"parties": [""], "objective": "", "pressure": "", "escalation_level": 0, "resolution_state": "open", "confidence": 0.0},\n'
        '      "hook": {"hook_type": "", "open_question": "", "introduced_at": "chapter:%d", "expected_resolution_range": "future_chapters", "confidence": 0.0},\n'
        '      "reward": {"reward_type": "", "beneficiary_character_id": "", "reader_effect": "", "intensity": 0.0, "payoff_target": "", "confidence": 0.0},\n'
        '      "climax": {"scope_type": "chapter", "intensity": 0.0, "aftermath": "", "confidence": 0.0}\n'
        "    }\n"
        "  ],\n"
        '  "relationships": [{"source": "", "relation_type": "", "target": "", "confidence": 0.0}]\n'
        "}\n"
        "要求：\n"
        "1. scenes 至少 1 个。\n"
        "2. 每个 scene 都补 event/conflict/hook/reward/climax。\n"
        "3. 只根据章节文本，不编不存在设定。\n"
        "4. 文本字段用简洁中文。\n"
        f"章节标题：{chapter.get('title', f'第{chapter_index}章')}\n"
        f"章节文本：\n{raw_text}"
    ) % (chapter_index, chapter_index)


def _resolve_extraction_profile(store: Any) -> tuple[dict[str, Any] | None, list[dict[str, Any]], dict[str, Any] | None]:
    if not hasattr(store, "resolve_model_profile"):
        return None, [], None
    default_profile_id = getattr(store, "DEFAULT_MODEL_PROFILE_ID", "model_profile_default")
    resolution = store.resolve_model_profile("extraction", default_profile_id, require_structured_output=True)
    return resolution.get("selected_profile"), list(resolution.get("provider_calls", [])), resolution.get("assignment")


def _append_provider_call(
    store: Any,
    provider_calls: list[dict[str, Any]],
    *,
    command: dict[str, Any],
    model_profile: dict[str, Any],
    task_type: str,
    assignment_id: str | None,
    input_refs: list[str],
    output_ref: str,
    status: str,
    retry_count: int,
    error_code: str | None = None,
) -> None:
    if hasattr(store, "_build_provider_call"):
        provider_calls.append(
            store._build_provider_call(
                "extraction",
                model_profile["model_profile_id"],
                model_profile["provider_name"],
                status,
                retry_count,
                error_code=error_code,
                workspace_id=command["workspace_id"],
                task_id=command["task_id"],
                request_id=command.get("command_id", "system-extraction"),
                trace_id=command["trace_id"],
                task_type=task_type,
                assignment_id=assignment_id,
                input_refs=input_refs,
                output_ref=output_ref,
                fallback_from_call_id=provider_calls[-1]["provider_call_id"] if provider_calls and status == "succeeded" and provider_calls[-1].get("status") == "failed" else None,
            )
        )
        return
    provider_calls.append(
        {
            "schema_version": 1,
            "provider_call_id": f"provider-call-{len(provider_calls) + 1}",
            "workspace_id": command["workspace_id"],
            "task_id": command["task_id"],
            "trace_id": command["trace_id"],
            "agent_role": "extraction",
            "task_type": task_type,
            "assignment_id": assignment_id,
            "model_profile_id": model_profile["model_profile_id"],
            "provider_name": model_profile["provider_name"],
            "provider_model_name": model_profile["provider_model_name"],
            "input_refs": input_refs,
            "output_ref": output_ref,
            "retry_count": retry_count,
            "status": status,
            "error_code": error_code,
            "created_at": utc_now(),
        }
    )


def _chapter_provider_analysis(
    *,
    store: Any,
    command: dict[str, Any],
    chapter: dict[str, Any],
    model_profile: dict[str, Any] | None,
    provider_calls: list[dict[str, Any]],
    assignment: dict[str, Any] | None,
    output_ref: str,
    knowledge_objects: list[dict[str, Any]],
) -> tuple[dict[str, Any], bool]:
    chapter_index = chapter.get("chapter_index", 1)
    fallback = _build_fallback_chapter_analysis(chapter, chapter_index, knowledge_objects)
    if not model_profile:
        return fallback, False
    if model_profile.get("provider_name") not in {"deepseek", "openai_compatible"}:
        _append_provider_call(
            store,
            provider_calls,
            command=command,
            model_profile=model_profile,
            task_type=command["task_type"],
            assignment_id=assignment.get("assignment_id") if assignment else None,
            input_refs=[*command["input_refs"], chapter.get("text_object_ref", f"object://source-chapters/{chapter['chapter_id']}")],
            output_ref=output_ref,
            status="failed",
            retry_count=max((call.get("retry_count", 0) for call in provider_calls), default=0) + 1,
            error_code="provider_not_supported",
        )
        return fallback, False
    try:
        payload = _openai_json_completion(
            model_profile=model_profile,
            system="你是中文网文拆书分析师。输出章节结构化 JSON。不要输出解释。",
            user=_build_chapter_prompt(chapter),
        )
        _append_provider_call(
            store,
            provider_calls,
            command=command,
            model_profile=model_profile,
            task_type=command["task_type"],
            assignment_id=assignment.get("assignment_id") if assignment else None,
            input_refs=[*command["input_refs"], chapter.get("text_object_ref", f"object://source-chapters/{chapter['chapter_id']}")],
            output_ref=output_ref,
            status="succeeded",
            retry_count=max((call.get("retry_count", 0) for call in provider_calls), default=0),
        )
        return payload, True
    except ChapterAnalysisProviderError as exc:
        _append_provider_call(
            store,
            provider_calls,
            command=command,
            model_profile=model_profile,
            task_type=command["task_type"],
            assignment_id=assignment.get("assignment_id") if assignment else None,
            input_refs=[*command["input_refs"], chapter.get("text_object_ref", f"object://source-chapters/{chapter['chapter_id']}")],
            output_ref=output_ref,
            status="failed",
            retry_count=max((call.get("retry_count", 0) for call in provider_calls), default=0) + 1,
            error_code=exc.error_code,
        )
        return fallback, False


def _normalize_chapter_analysis(
    *,
    run_id: str,
    book_id: str,
    workspace_id: str,
    chapter: dict[str, Any],
    chapter_analysis: dict[str, Any],
    knowledge_objects: list[dict[str, Any]],
    evidence_ref: str,
    evidence_id: str,
) -> dict[str, Any]:
    chapter_index = chapter["chapter_index"]
    chapter_id = chapter["chapter_id"]
    object_refs = _object_ref_map(knowledge_objects)
    protagonist_ref = f"object://knowledge-objects/{knowledge_objects[0]['object_id']}" if knowledge_objects else "protagonist"
    fallback_parties = [knowledge_objects[0]["canonical_name"], knowledge_objects[-1]["canonical_name"]] if len(knowledge_objects) >= 2 else ["protagonist", "external_pressure"]
    raw_scenes = chapter_analysis.get("scenes") if isinstance(chapter_analysis.get("scenes"), list) else []
    if not raw_scenes:
        raw_scenes = _build_fallback_chapter_analysis(chapter, chapter_index, knowledge_objects)["scenes"]

    normalized = {
        "scenes": [],
        "events": [],
        "conflicts": {},
        "hooks": {},
        "rewards": {},
        "climaxes": {},
        "relationships": {},
    }

    last_conflict_id = None
    last_event_id = None
    last_hook_id = None
    last_reward_id = None

    for scene_index, raw_scene in enumerate(raw_scenes, start=1):
        scene_id = f"{run_id}SCENE{chapter_index:02d}{scene_index:02d}"
        event_id = f"{run_id}EVENT{chapter_index:02d}{scene_index:02d}"
        conflict_id = f"{run_id}CONFLICT{chapter_index:02d}{scene_index:02d}"
        hook_id = f"{run_id}HOOK{chapter_index:02d}{scene_index:02d}"
        reward_id = f"{run_id}REWARD{chapter_index:02d}{scene_index:02d}"
        climax_id = f"{run_id}CLIMAX{chapter_index:02d}{scene_index:02d}"

        text_range = _text(raw_scene.get("text_range"), chapter.get("text_range") or f"c{chapter_index}:p1-p1")
        scene_summary = _text(raw_scene.get("summary"), _chapter_excerpt(chapter) or "章节主冲突场景。")
        scene = {
            "schema_version": 1,
            "scene_id": scene_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "workspace_id": workspace_id,
            "scene_index": scene_index,
            "title": _text(raw_scene.get("title"), f"{chapter.get('title', f'第{chapter_index}章')}场景{scene_index}"),
            "text_range": text_range,
            "segmentation_status": "segmented",
            "segmentation_confidence": _confidence(raw_scene.get("segmentation_confidence"), 0.84),
            "summary": scene_summary,
            "evidence_refs": [evidence_ref],
            "payload": {"source": "provider"},
        }
        normalized["scenes"].append(scene)

        raw_event = raw_scene.get("event") if isinstance(raw_scene.get("event"), dict) else {}
        participants = _participant_refs(raw_event.get("participants") or raw_scene.get("participants") or [], object_refs, protagonist_ref)
        event = {
            "schema_version": 1,
            "event_id": event_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
            "event_index": scene_index,
            "event_type": _text(raw_event.get("event_type"), "turning_point"),
            "cause": _text(raw_event.get("cause"), "章节压力或线索推动局势变化。"),
            "action": _text(raw_event.get("action"), scene_summary),
            "result": _text(raw_event.get("result"), "场景目标被推进。"),
            "consequence": _text(raw_event.get("consequence"), "后续冲突获得动机。"),
            "participants": participants,
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_event.get("confidence"), 0.79),
            "payload": {"source": "provider"},
        }
        normalized["events"].append(event)

        raw_conflict = raw_scene.get("conflict") if isinstance(raw_scene.get("conflict"), dict) else {}
        conflict = {
            "schema_version": 1,
            "conflict_id": conflict_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
            "parties": [str(item) for item in (raw_conflict.get("parties") or fallback_parties)],
            "objective": _text(raw_conflict.get("objective"), "在压力下保住目标并寻找突破口。"),
            "pressure": _text(raw_conflict.get("pressure"), "外部规则或人物施压。"),
            "escalation_level": _escalation_level(raw_conflict.get("escalation_level"), 2 + scene_index),
            "resolution_state": _text(raw_conflict.get("resolution_state"), "open") if _text(raw_conflict.get("resolution_state"), "open") in {"open", "escalated", "resolved", "deferred"} else "open",
            "trigger_event_id": event_id,
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_conflict.get("confidence"), 0.77),
            "payload": {"source": "provider"},
        }
        normalized["conflicts"][conflict_id] = conflict

        raw_hook = raw_scene.get("hook") if isinstance(raw_scene.get("hook"), dict) else {}
        hook = {
            "schema_version": 1,
            "hook_id": hook_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
            "hook_type": _text(raw_hook.get("hook_type"), "growth_question"),
            "open_question": _text(raw_hook.get("open_question"), "主角如何从当前压力中反转？"),
            "introduced_at": _text(raw_hook.get("introduced_at"), f"chapter:{chapter_index}"),
            "expected_resolution_range": _text(raw_hook.get("expected_resolution_range"), "future_chapters"),
            "linked_conflict_id": conflict_id,
            "linked_event_id": event_id,
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_hook.get("confidence"), 0.75),
            "payload": {"source": "provider"},
        }
        normalized["hooks"][hook_id] = hook

        raw_reward = raw_scene.get("reward") if isinstance(raw_scene.get("reward"), dict) else {}
        reward = {
            "schema_version": 1,
            "reward_id": reward_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
            "reward_type": _text(raw_reward.get("reward_type"), "anticipation"),
            "trigger_event_id": event_id,
            "beneficiary_character_id": _object_ref(raw_reward.get("beneficiary_character_id"), object_refs, protagonist_ref),
            "reader_effect": _text(raw_reward.get("reader_effect"), "制造后续反击期待。"),
            "intensity": _intensity(raw_reward.get("intensity"), 0.7),
            "payoff_target": _text(raw_reward.get("payoff_target"), "future_reversal"),
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_reward.get("confidence"), 0.73),
            "payload": {"source": "provider"},
        }
        normalized["rewards"][reward_id] = reward

        raw_climax = raw_scene.get("climax") if isinstance(raw_scene.get("climax"), dict) else {}
        scope_type = _text(raw_climax.get("scope_type"), "chapter")
        if scope_type not in {"chapter", "scene", "volume", "book"}:
            scope_type = "chapter"
        climax = {
            "schema_version": 1,
            "climax_id": climax_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
            "scope_type": scope_type,
            "scope_id": scene_id if scope_type == "scene" else chapter_id,
            "event_id": event_id,
            "conflict_id": conflict_id,
            "reward_refs": [reward_id],
            "hook_refs": [hook_id],
            "intensity": _intensity(raw_climax.get("intensity"), 0.8),
            "aftermath": _text(raw_climax.get("aftermath"), "章节留下后续解决期待。"),
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_climax.get("confidence"), 0.74),
            "payload": {"source": "provider"},
        }
        normalized["climaxes"][climax_id] = climax

        last_conflict_id = conflict_id
        last_event_id = event_id
        last_hook_id = hook_id
        last_reward_id = reward_id

    raw_relationships = chapter_analysis.get("relationships") if isinstance(chapter_analysis.get("relationships"), list) else []
    if not raw_relationships and len(knowledge_objects) >= 2:
        raw_relationships = [{
            "source": knowledge_objects[0]["canonical_name"],
            "relation_type": "pressured_by",
            "target": knowledge_objects[-1]["canonical_name"],
            "confidence": 0.7,
        }]
    for relationship_index, raw_relationship in enumerate(raw_relationships, start=1):
        edge_id = f"{run_id}RELATION{chapter_index:02d}{relationship_index:02d}"
        normalized["relationships"][edge_id] = {
            "schema_version": 1,
            "edge_id": edge_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": normalized["scenes"][0]["scene_id"] if normalized["scenes"] else None,
            "workspace_id": workspace_id,
            "source_id": _object_ref(raw_relationship.get("source"), object_refs, protagonist_ref),
            "relation_type": _text(raw_relationship.get("relation_type"), "pressured_by"),
            "target_id": _object_ref(raw_relationship.get("target"), object_refs, protagonist_ref),
            "confidence": _confidence(raw_relationship.get("confidence"), 0.7),
            "evidence_id": evidence_id,
            "evidence_refs": [evidence_ref],
            "payload": {
                "source": "provider",
                "linked_conflict_id": last_conflict_id,
                "linked_event_id": last_event_id,
                "linked_hook_id": last_hook_id,
                "linked_reward_id": last_reward_id,
            },
        }

    return normalized


def run_extract_knowledge(command: dict[str, Any]) -> dict[str, Any]:
    store = load_phase_two_store()
    run_ref = next(
        ref for ref in command["input_refs"]
        if ref.startswith("object://extraction-runs/")
    )
    run_id = run_ref.rsplit("/", 1)[-1]
    fixture = build_extraction_fixture(command)
    book_ref = next(
        ref for ref in command["input_refs"]
        if ref.startswith("object://source-books/")
    )
    book_id = book_ref.rsplit("/", 1)[-1]
    source_content = store.get_book_source_content(book_id) if hasattr(store, "get_book_source_content") else None
    chapters = store.list_book_chapters(book_id) if hasattr(store, "list_book_chapters") else []
    evidences = []
    if source_content and chapters:
        evidences = [
            {
                "schema_version": 1,
                "evidence_id": f"{run_id}EVIDENCE{index:02d}",
                "evidence_ref": f"evidence://{run_id}EVIDENCE{index:02d}",
                "book_id": book_id,
                "chapter_id": chapter["chapter_id"],
                "chapter_index": chapter["chapter_index"],
                "text_range": chapter.get("text_range") or f"c{chapter['chapter_index']}:p1-p1",
                "excerpt": (chapter.get("text_excerpt") or chapter.get("raw_text") or source_content["content"])[:160],
                "source_object_refs": [f"object://knowledge-objects/{fixture['knowledge_objects'][min(index - 1, len(fixture['knowledge_objects']) - 1)]['object_id']}"],
                "source_content_ref": source_content["object_ref"],
                "confidence": 0.82 if index == 1 else 0.76,
                "trace_id": command["trace_id"],
            }
            for index, chapter in enumerate(chapters[:3], start=1)
        ]
        for index, item in enumerate(fixture["knowledge_objects"]):
            if evidences:
                item["evidence_refs"] = [evidences[min(index, len(evidences) - 1)]["evidence_ref"]]
        fixture["graph_summary"]["nodes"] = [
            {**node, "evidence_refs": fixture["knowledge_objects"][min(index, len(fixture["knowledge_objects"]) - 1)].get("evidence_refs", node["evidence_refs"])}
            for index, node in enumerate(fixture["graph_summary"]["nodes"])
        ]

    deep_analysis = {"scenes_by_chapter": {}, "events_by_scene": {}, "conflicts": {}, "hooks": {}, "rewards": {}, "climaxes": {}, "relationship_edges": {}}
    model_profile, provider_calls, assignment = _resolve_extraction_profile(store)
    provider_used = False

    if chapters:
        for index, chapter in enumerate(chapters[:3], start=1):
            evidence = evidences[min(index - 1, len(evidences) - 1)] if evidences else {
                "evidence_id": f"{run_id}EVIDENCE{index:02d}",
                "evidence_ref": f"evidence://{run_id}EVIDENCE{index:02d}",
            }
            chapter_analysis, used_provider = _chapter_provider_analysis(
                store=store,
                command=command,
                chapter=chapter,
                model_profile=model_profile,
                provider_calls=provider_calls,
                assignment=assignment,
                output_ref=fixture["run"]["extraction_report_ref"],
                knowledge_objects=fixture["knowledge_objects"],
            )
            provider_used = provider_used or used_provider
            normalized = _normalize_chapter_analysis(
                run_id=run_id,
                book_id=book_id,
                workspace_id=command["workspace_id"],
                chapter=chapter,
                chapter_analysis=chapter_analysis,
                knowledge_objects=fixture["knowledge_objects"],
                evidence_ref=evidence["evidence_ref"],
                evidence_id=evidence["evidence_id"],
            )
            deep_analysis["scenes_by_chapter"][chapter["chapter_id"]] = normalized["scenes"]
            for scene in normalized["scenes"]:
                deep_analysis["events_by_scene"][scene["scene_id"]] = [event for event in normalized["events"] if event["scene_id"] == scene["scene_id"]]
            deep_analysis["conflicts"].update(normalized["conflicts"])
            deep_analysis["hooks"].update(normalized["hooks"])
            deep_analysis["rewards"].update(normalized["rewards"])
            deep_analysis["climaxes"].update(normalized["climaxes"])
            deep_analysis["relationship_edges"].update(normalized["relationships"])

    scene_count = sum(len(items) for items in deep_analysis["scenes_by_chapter"].values())
    object_count = len(fixture["knowledge_objects"])
    low_confidence_count = len([
        item for item in fixture["knowledge_objects"]
        if item.get("review_status") == "pending" and item.get("confidence", 1) < 0.8
    ])
    metrics = {
        "pipeline_stages": PIPELINE_STAGES,
        "current_stage": fixture["run"]["current_stage"],
        "chapter_count": len(chapters) or fixture["run"]["chapter_count"],
        "scene_count": scene_count or fixture["run"]["scene_count"],
        "object_count": object_count,
        "evidence_count": len(evidences),
        "low_confidence_count": low_confidence_count,
        "knowledge_package_ref": fixture["run"]["knowledge_package_ref"],
        "graph_package_ref": fixture["run"]["graph_package_ref"],
        "extraction_report_ref": fixture["run"]["extraction_report_ref"],
        "quality_report_ref": fixture["run"]["quality_report_ref"],
        "graph_summary": fixture["graph_summary"],
        "knowledge_objects": fixture["knowledge_objects"],
        "evidences": evidences,
        "deep_analysis": deep_analysis,
        "provider_calls": provider_calls,
        "analysis_mode": "provider" if provider_used else "fallback",
        "errors": fixture["run"]["errors"],
        "generated_at": utc_now(),
    }
    task = store.apply_task_execution_result(
        command["task_id"],
        "requires_review",
        fixture["task"]["output_refs"],
        metrics,
        trace_id=command["trace_id"],
        dispatch_token=command.get("dispatch_token"),
    )
    return {
        "schema_version": 1,
        "task_id": command["task_id"],
        "status": task["status"] if task else "requires_review",
        "output_refs": task["output_refs"] if task else fixture["task"]["output_refs"],
        "metrics": metrics,
        "errors": [],
        "trace_id": command["trace_id"],
    }
