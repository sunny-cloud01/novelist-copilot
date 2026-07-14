"""
Synchronous extraction pipeline that runs inside core-service.
Reads book chapters from the in-memory store, analyzes each chapter
(LLM when credentials are available, fallback to rules otherwise),
and writes scenes / events / conflicts / hooks / rewards / climaxes /
relationships / knowledge objects / graph back to the store.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# helpers – kept self-contained so we don't need worker.extraction
# ---------------------------------------------------------------------------

_ENTITY_TYPE_HINTS: dict[str, str] = {
    "宗": "faction",
    "门": "faction",
    "派": "faction",
    "族": "clan",
    "家": "clan",
    "城": "location",
    "山": "location",
    "谷": "location",
    "殿": "location",
    "府": "location",
    "阁": "faction",
    "院": "location",
    "村": "location",
    "塔": "location",
    "域": "location",
    "界": "location",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


def _chapter_excerpt(chapter: dict[str, Any]) -> str:
    return (chapter.get("text_excerpt") or chapter.get("raw_text") or "")[:160]


def _guess_entity_type(name: str) -> str:
    for suffix, entity_type in _ENTITY_TYPE_HINTS.items():
        if name.endswith(suffix):
            return entity_type
    return "character"


# ---------------------------------------------------------------------------
# Entity extraction (regex-based, no LLM required)
# ---------------------------------------------------------------------------

def _extract_entity_candidates(chapter: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract named-entity candidates from chapter text using regex."""
    text = (chapter.get("raw_text") or chapter.get("text_excerpt") or "")
    title = str(chapter.get("title") or "").strip()

    tokens: list[str] = re.findall(r"[\u4e00-\u9fff]{2,4}", text)
    freq: dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))

    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()

    if title and title not in seen:
        seen.add(title)
        candidates.append(
            {
                "name": title,
                "type": _guess_entity_type(title),
                "aliases": [],
                "confidence": 0.55,
                "summary": f"章节《{title}》核心对象。",
            }
        )

    for name, count in ranked:
        if count < 2 or name in seen:
            continue
        seen.add(name)
        candidates.append(
            {
                "name": name,
                "type": _guess_entity_type(name),
                "aliases": [],
                "confidence": min(0.75, 0.5 + count * 0.05),
                "summary": f"章节高频对象 {name}。",
            }
        )
        if len(candidates) >= 8:
            break

    return candidates


# ---------------------------------------------------------------------------
# Entity aggregation across chapters
# ---------------------------------------------------------------------------

def _aggregate_entities(
    entity_lists: list[list[dict[str, Any]]],
    run_id: str,
    workspace_id: str,
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for entity_list in entity_lists:
        for entity in entity_list:
            name = str(entity.get("name", "")).strip()
            if not name:
                continue
            key = name.lower()
            confidence_val = _confidence(entity.get("confidence"), 0.5)
            aliases = [
                a.strip()
                for a in entity.get("aliases", [])
                if isinstance(a, str) and a.strip()
            ]
            if key not in merged:
                merged[key] = {
                    "canonical_name": name,
                    "object_type": str(entity.get("type") or "character"),
                    "aliases": set(aliases),
                    "confidence": confidence_val,
                    "summary": _text(entity.get("summary"), f"{name} 相关对象。"),
                }
            else:
                record = merged[key]
                record["aliases"].update(aliases)
                if confidence_val > record["confidence"]:
                    record["confidence"] = confidence_val
                    record["object_type"] = str(
                        entity.get("type") or record["object_type"]
                    )

    objects: list[dict[str, Any]] = []
    for index, (_, record) in enumerate(merged.items(), start=1):
        confidence_val = record["confidence"]
        lifecycle = "approved" if confidence_val >= 0.95 else "candidate"
        objects.append(
            {
                "schema_version": 1,
                "object_id": f"{run_id}OBJ{index:03d}",
                "workspace_id": workspace_id,
                "object_type": record["object_type"],
                "canonical_name": record["canonical_name"],
                "lifecycle_status": lifecycle,
                "review_status": "approved" if lifecycle == "approved" else "pending",
                "confidence": confidence_val,
                "evidence_refs": [],
                "payload": {
                    "schema_version": 1,
                    "aliases": sorted(record["aliases"]),
                    "summary": record["summary"],
                },
            }
        )
    return objects


# ---------------------------------------------------------------------------
# Object reference helpers for normalization
# ---------------------------------------------------------------------------

def _object_ref_map(knowledge_objects: list[dict[str, Any]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for item in knowledge_objects:
        object_ref = f"object://knowledge-objects/{item['object_id']}"
        mapping[item["canonical_name"].strip().lower()] = object_ref
        for alias in item.get("payload", {}).get("aliases", []):
            if isinstance(alias, str) and alias.strip():
                mapping[alias.strip().lower()] = object_ref
    return mapping


def _participant_refs(
    names: list[Any], object_refs: dict[str, str], fallback_ref: str
) -> list[str]:
    refs: list[str] = []
    for name in names:
        if not isinstance(name, str) or not name.strip():
            continue
        refs.append(object_refs.get(name.strip().lower(), name.strip()))
    if not refs:
        refs.append(fallback_ref)
    return refs


def _object_ref(
    name: Any, object_refs: dict[str, str], fallback_ref: str
) -> str:
    if isinstance(name, str) and name.strip():
        return object_refs.get(name.strip().lower(), name.strip())
    return fallback_ref


# ---------------------------------------------------------------------------
# LLM provider call (OpenAI-compatible)
# ---------------------------------------------------------------------------

def _call_llm_json(
    *, system: str, user: str, model_name: str = "deepseek-chat"
) -> dict[str, Any] | None:
    """Call an OpenAI-compatible endpoint for structured JSON output."""
    base_url = os.getenv("NOVELIST_LLM_BASE_URL")
    api_key = os.getenv("NOVELIST_LLM_API_KEY")
    if not base_url or not api_key:
        return None
    endpoint = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps(
        {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.3,
            "max_tokens": 1800,
            "response_format": {"type": "json_object"},
        }
    ).encode("utf-8")
    req = Request(
        endpoint,
        data=body,
        headers={
            "authorization": f"Bearer {api_key}",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        from urllib.request import urlopen as _uo

        with _uo(req, timeout=90) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        logger.warning("LLM call failed: %s", exc)
        return None

    try:
        content = payload["choices"][0]["message"]["content"]
        if isinstance(content, list):
            content = "".join(
                str(item.get("text", "")) for item in content if isinstance(item, dict)
            )
        if not isinstance(content, str):
            return None
        content = content.strip()
        if content.startswith("```"):
            lines = content.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines).strip()
        return json.loads(content)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        logger.warning("LLM response parse failed: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Chapter prompt builder
# ---------------------------------------------------------------------------

def _build_chapter_prompt(chapter: dict[str, Any]) -> str:
    chapter_index = chapter.get("chapter_index", 1)
    raw_text = (chapter.get("raw_text") or chapter.get("text_excerpt") or "")[:6000]
    return (
        "按小说结构分析当前章节。只输出 JSON 对象，不要解释。\n"
        "JSON 结构：{\n"
        '  "summary": "章节摘要",\n'
        '  "entities": [{"name": "人物或势力名", "type": "character|clan|mentor|faction|location", "aliases": ["别名"], "confidence": 0.0, "summary": "一句话说明"}],\n'
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


# ---------------------------------------------------------------------------
# Fallback chapter analysis (rule-based, no LLM)
# ---------------------------------------------------------------------------

def _build_fallback_chapter_analysis(
    chapter: dict[str, Any],
    chapter_index: int,
    knowledge_objects: list[dict[str, Any]],
    chapter_entities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    entity_names = [
        str(entity.get("name", "")).strip()
        for entity in (chapter_entities or [])
        if str(entity.get("name", "")).strip()
    ]
    if knowledge_objects:
        protagonist = knowledge_objects[0]["canonical_name"]
        pressure = knowledge_objects[-1]["canonical_name"]
    elif len(entity_names) >= 2:
        protagonist = entity_names[0]
        pressure = entity_names[1]
    elif entity_names:
        protagonist = entity_names[0]
        pressure = "外部压力"
    else:
        protagonist = "主角"
        pressure = "外部压力"

    excerpt = _chapter_excerpt(chapter) or "章节主场景推进。"
    chapter_title = chapter.get("title", f"第{chapter_index}章")

    return {
        "summary": excerpt,
        "scenes": [
            {
                "title": f"{chapter_title}主场景",
                "summary": excerpt,
                "text_range": chapter.get("text_range")
                or f"c{chapter_index}:p1-p1",
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


# ---------------------------------------------------------------------------
# Normalize chapter analysis → store records
# ---------------------------------------------------------------------------

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

    protagonist_ref = (
        f"object://knowledge-objects/{knowledge_objects[0]['object_id']}"
        if knowledge_objects
        else "protagonist"
    )
    fallback_parties = (
        [knowledge_objects[0]["canonical_name"], knowledge_objects[-1]["canonical_name"]]
        if len(knowledge_objects) >= 2
        else ["protagonist", "external_pressure"]
    )

    raw_scenes = (
        chapter_analysis.get("scenes")
        if isinstance(chapter_analysis.get("scenes"), list)
        else []
    )
    if not raw_scenes:
        raw_scenes = _build_fallback_chapter_analysis(
            chapter, chapter_index, knowledge_objects
        )["scenes"]

    normalized: dict[str, Any] = {
        "scenes": [],
        "events": [],
        "conflicts": {},
        "hooks": {},
        "rewards": {},
        "climaxes": {},
        "relationships": {},
    }

    for scene_index, raw_scene in enumerate(raw_scenes, start=1):
        scene_id = f"{run_id}SCENE{chapter_index:02d}{scene_index:02d}"
        event_id = f"{run_id}EVENT{chapter_index:02d}{scene_index:02d}"
        conflict_id = f"{run_id}CONFLICT{chapter_index:02d}{scene_index:02d}"
        hook_id = f"{run_id}HOOK{chapter_index:02d}{scene_index:02d}"
        reward_id = f"{run_id}REWARD{chapter_index:02d}{scene_index:02d}"
        climax_id = f"{run_id}CLIMAX{chapter_index:02d}{scene_index:02d}"

        text_range = _text(
            raw_scene.get("text_range"),
            chapter.get("text_range") or f"c{chapter_index}:p1-p1",
        )
        scene_summary = _text(
            raw_scene.get("summary"),
            _chapter_excerpt(chapter) or "章节主冲突场景。",
        )

        scene = {
            "schema_version": 1,
            "scene_id": scene_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "workspace_id": workspace_id,
            "scene_index": scene_index,
            "title": _text(
                raw_scene.get("title"),
                f"{chapter.get('title', f'第{chapter_index}章')}场景{scene_index}",
            ),
            "text_range": text_range,
            "segmentation_status": "segmented",
            "segmentation_confidence": _confidence(
                raw_scene.get("segmentation_confidence"), 0.84
            ),
            "evidence_refs": [evidence_ref],
            "payload": {"source": "pipeline"},
        }
        normalized["scenes"].append(scene)

        # --- event ---
        raw_event = (
            raw_scene.get("event")
            if isinstance(raw_scene.get("event"), dict)
            else {}
        )
        participants = _participant_refs(
            raw_event.get("participants")
            or raw_scene.get("participants")
            or [],
            object_refs,
            protagonist_ref,
        )
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
            "consequence": _text(
                raw_event.get("consequence"), "后续冲突获得动机。"
            ),
            "participants": participants,
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_event.get("confidence"), 0.79),
            "payload": {"source": "pipeline"},
        }
        normalized["events"].append(event)

        # --- conflict ---
        raw_conflict = (
            raw_scene.get("conflict")
            if isinstance(raw_scene.get("conflict"), dict)
            else {}
        )
        conflict = {
            "schema_version": 1,
            "conflict_id": conflict_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
            "parties": [
                str(item)
                for item in (raw_conflict.get("parties") or fallback_parties)
            ],
            "objective": _text(
                raw_conflict.get("objective"), "在压力下保住目标并寻找突破口。"
            ),
            "pressure": _text(
                raw_conflict.get("pressure"), "外部规则或人物施压。"
            ),
            "escalation_level": _escalation_level(
                raw_conflict.get("escalation_level"), 2 + scene_index
            ),
            "resolution_state": (
                _text(raw_conflict.get("resolution_state"), "open")
                if _text(raw_conflict.get("resolution_state"), "open")
                in {"open", "escalated", "resolved", "deferred"}
                else "open"
            ),
            "trigger_event_id": event_id,
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_conflict.get("confidence"), 0.77),
            "payload": {"source": "pipeline"},
        }
        normalized["conflicts"][conflict_id] = conflict

        # --- hook ---
        raw_hook = (
            raw_scene.get("hook")
            if isinstance(raw_scene.get("hook"), dict)
            else {}
        )
        hook = {
            "schema_version": 1,
            "hook_id": hook_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
            "hook_type": _text(raw_hook.get("hook_type"), "growth_question"),
            "open_question": _text(
                raw_hook.get("open_question"), "主角如何从当前压力中反转？"
            ),
            "introduced_at": _text(
                raw_hook.get("introduced_at"), f"chapter:{chapter_index}"
            ),
            "expected_resolution_range": _text(
                raw_hook.get("expected_resolution_range"), "future_chapters"
            ),
            "linked_conflict_id": conflict_id,
            "linked_event_id": event_id,
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_hook.get("confidence"), 0.75),
            "payload": {"source": "pipeline"},
        }
        normalized["hooks"][hook_id] = hook

        # --- reward ---
        raw_reward = (
            raw_scene.get("reward")
            if isinstance(raw_scene.get("reward"), dict)
            else {}
        )
        reward = {
            "schema_version": 1,
            "reward_id": reward_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
            "reward_type": _text(raw_reward.get("reward_type"), "anticipation"),
            "trigger_event_id": event_id,
            "beneficiary_character_id": _object_ref(
                raw_reward.get("beneficiary_character_id"),
                object_refs,
                protagonist_ref,
            ),
            "reader_effect": _text(
                raw_reward.get("reader_effect"), "制造后续反击期待。"
            ),
            "intensity": _intensity(raw_reward.get("intensity"), 0.7),
            "payoff_target": _text(
                raw_reward.get("payoff_target"), "future_reversal"
            ),
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_reward.get("confidence"), 0.73),
            "payload": {"source": "pipeline"},
        }
        normalized["rewards"][reward_id] = reward

        # --- climax ---
        raw_climax = (
            raw_scene.get("climax")
            if isinstance(raw_scene.get("climax"), dict)
            else {}
        )
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
            "aftermath": _text(
                raw_climax.get("aftermath"), "章节留下后续解决期待。"
            ),
            "evidence_refs": [evidence_ref],
            "confidence": _confidence(raw_climax.get("confidence"), 0.74),
            "payload": {"source": "pipeline"},
        }
        normalized["climaxes"][climax_id] = climax

    # --- relationships ---
    raw_relationships = (
        chapter_analysis.get("relationships")
        if isinstance(chapter_analysis.get("relationships"), list)
        else []
    )
    if not raw_relationships and len(knowledge_objects) >= 2:
        raw_relationships = [
            {
                "source": knowledge_objects[0]["canonical_name"],
                "relation_type": "pressured_by",
                "target": knowledge_objects[-1]["canonical_name"],
                "confidence": 0.7,
            }
        ]
    for rel_index, raw_rel in enumerate(raw_relationships, start=1):
        edge_id = f"{run_id}RELATION{chapter_index:02d}{rel_index:02d}"
        normalized["relationships"][edge_id] = {
            "schema_version": 1,
            "edge_id": edge_id,
            "book_id": book_id,
            "chapter_id": chapter_id,
            "scene_id": (
                normalized["scenes"][0]["scene_id"]
                if normalized["scenes"]
                else None
            ),
            "workspace_id": workspace_id,
            "source_id": _object_ref(
                raw_rel.get("source"), object_refs, protagonist_ref
            ),
            "relation_type": _text(raw_rel.get("relation_type"), "pressured_by"),
            "target_id": _object_ref(
                raw_rel.get("target"), object_refs, protagonist_ref
            ),
            "confidence": _confidence(raw_rel.get("confidence"), 0.7),
            "evidence_id": evidence_id,
            "evidence_refs": [evidence_ref],
            "payload": {"source": "pipeline"},
        }

    return normalized


# ---------------------------------------------------------------------------
# Knowledge graph builder
# ---------------------------------------------------------------------------

def _build_graph_from_analysis(
    knowledge_objects: list[dict[str, Any]],
    relationship_edges: dict[str, dict[str, Any]],
    book_id: str,
    run_id: str,
) -> dict[str, Any]:
    node_by_object: dict[str, str] = {}
    node_details: dict[str, dict[str, Any]] = {}
    summary_nodes: list[dict[str, Any]] = []

    for index, obj in enumerate(knowledge_objects, start=1):
        node_id = f"{run_id}NODE{index:03d}"
        node_by_object[obj["object_id"]] = node_id
        aliases = obj.get("payload", {}).get("aliases", [])
        node_details[node_id] = {
            "schema_version": 1,
            "node_id": node_id,
            "book_id": book_id,
            "label": obj["canonical_name"],
            "node_type": obj["object_type"],
            "canonical_object_id": obj["object_id"],
            "review_status": obj.get("review_status", "pending"),
            "lifecycle_status": obj.get("lifecycle_status", "candidate"),
            "confidence": obj.get("confidence", 0.5),
            "aliases": aliases,
            "summary": obj.get("payload", {}).get(
                "summary", f"{obj['canonical_name']} 相关对象。"
            ),
            "evidence_refs": obj.get("evidence_refs", []),
        }
        summary_nodes.append(
            {
                "node_id": node_id,
                "label": obj["canonical_name"],
                "node_type": obj["object_type"],
                "evidence_refs": obj.get("evidence_refs", []),
            }
        )

    name_to_node: dict[str, str] = {}
    for obj in knowledge_objects:
        node_id = node_by_object[obj["object_id"]]
        canonical = obj.get("canonical_name")
        if isinstance(canonical, str) and canonical.strip():
            name_to_node.setdefault(canonical.strip().lower(), node_id)
        for alias in obj.get("payload", {}).get("aliases", []):
            if isinstance(alias, str) and alias.strip():
                name_to_node.setdefault(alias.strip().lower(), node_id)

    def _resolve(ref: Any) -> str | None:
        if not isinstance(ref, str):
            return node_by_object.get(ref) if isinstance(ref, str) else None
        raw = ref.rsplit("/", 1)[-1]
        node = node_by_object.get(raw)
        if node is not None:
            return node
        return name_to_node.get(raw.strip().lower())

    neighbors: dict[str, list[dict[str, Any]]] = {
        nid: [] for nid in node_details
    }
    edge_count = 0
    for edge in relationship_edges.values():
        source_node = _resolve(edge.get("source_id"))
        target_node = _resolve(edge.get("target_id"))
        if not source_node or not target_node or source_node == target_node:
            continue
        edge_count += 1
        relation = edge.get("relation_type", "related_to")
        confidence_val = edge.get("confidence", 0.7)
        evidence_refs = edge.get("evidence_refs", [])
        neighbors[source_node].append(
            {
                "edge_id": edge["edge_id"],
                "relation_type": relation,
                "direction": "outgoing",
                "neighbor_node_id": target_node,
                "neighbor_label": node_details[target_node]["label"],
                "neighbor_type": node_details[target_node]["node_type"],
                "confidence": confidence_val,
                "evidence_refs": evidence_refs,
            }
        )
        neighbors[target_node].append(
            {
                "edge_id": edge["edge_id"],
                "relation_type": relation,
                "direction": "incoming",
                "neighbor_node_id": source_node,
                "neighbor_label": node_details[source_node]["label"],
                "neighbor_type": node_details[source_node]["node_type"],
                "confidence": confidence_val,
                "evidence_refs": evidence_refs,
            }
        )

    return {
        "summary": {
            "schema_version": 1,
            "book_id": book_id,
            "node_count": len(summary_nodes),
            "edge_count": edge_count,
            "nodes": summary_nodes,
        },
        "node_details": node_details,
        "neighbors": neighbors,
    }


# ---------------------------------------------------------------------------
# Main extraction entry point – called from create_extraction_run
# ---------------------------------------------------------------------------

def run_sync_extraction(
    *,
    store: Any,
    book_id: str,
    run_id: str,
    task_id: str,
    workspace_id: str,
    trace_id: str,
) -> None:
    """
    Synchronously extract knowledge from all chapters of a book.
    Uses LLM when credentials are available, falls back to rule-based analysis.
    Results are written directly into the store.
    """
    chapters = store.chapters_by_book.get(book_id, [])
    if not chapters:
        logger.warning("No chapters found for book %s – extraction skipped", book_id)
        return

    # Build evidence records for the first 3 chapters
    source_content_id = store.source_content_by_book.get(book_id)
    source_content = store.source_contents.get(source_content_id) if source_content_id else None

    evidences: list[dict[str, Any]] = []
    for index, chapter in enumerate(chapters[:3], start=1):
        evidence_id = f"{run_id}EVIDENCE{index:02d}"
        evidence_ref = f"evidence://{run_id}EVIDENCE{index:02d}"
        evidences.append(
            {
                "schema_version": 1,
                "evidence_id": evidence_id,
                "evidence_ref": evidence_ref,
                "book_id": book_id,
                "chapter_id": chapter["chapter_id"],
                "chapter_index": chapter["chapter_index"],
                "text_range": chapter.get("text_range")
                or f"c{chapter['chapter_index']}:p1-p1",
                "excerpt": (
                    chapter.get("text_excerpt")
                    or chapter.get("raw_text")
                    or (source_content.get("content", "") if source_content else "")
                )[:160],
                "source_object_refs": (
                    [source_content.get("object_ref", "")]
                    if source_content and source_content.get("object_ref")
                    else []
                ),
                "source_content_ref": source_content.get("object_ref")
                if source_content
                else None,
                "confidence": 0.82 if index == 1 else 0.76,
                "trace_id": trace_id,
            }
        )
        store.evidences[evidence_id] = evidences[-1]

    # Register evidence under book for lookup
    store.evidence_by_book[book_id] = [
        e["evidence_id"] for e in evidences
    ]

    # --- Phase 1: entity extraction (regex) ---
    entity_lists: list[list[dict[str, Any]]] = []
    chapter_title_pattern = re.compile(r"^第[\u4e00-\u9fff\d]{1,6}章")
    for chapter in chapters[:5]:
        candidates = _extract_entity_candidates(chapter)
        # Filter out chapter titles from entity candidates
        candidates = [
            e for e in candidates
            if not chapter_title_pattern.match(e.get("name", ""))
        ]
        entity_lists.append(candidates)

    knowledge_objects = _aggregate_entities(entity_lists, run_id, workspace_id)

    # --- Phase 2: chapter analysis (LLM or fallback) ---
    deep_analysis: dict[str, Any] = {
        "scenes_by_chapter": {},
        "events_by_scene": {},
        "conflicts": {},
        "hooks": {},
        "rewards": {},
        "climaxes": {},
        "relationship_edges": {},
    }

    llm_used = False
    for index, chapter in enumerate(chapters[:3], start=1):
        evidence = evidences[min(index - 1, len(evidences) - 1)] if evidences else {
            "evidence_id": f"{run_id}EVIDENCE{index:02d}",
            "evidence_ref": f"evidence://{run_id}EVIDENCE{index:02d}",
        }
        chapter_candidates = entity_lists[min(index - 1, len(entity_lists) - 1)] if entity_lists else []

        # Try LLM first
        chapter_analysis: dict[str, Any] | None = None
        if not llm_used:  # Only try LLM once (first chapter)
            prompt = _build_chapter_prompt(chapter)
            chapter_analysis = _call_llm_json(
                system="你是中文网文拆书分析师。输出章节结构化 JSON。不要输出解释。",
                user=prompt,
            )
            if chapter_analysis is not None:
                llm_used = True
                logger.info(
                    "LLM analysis succeeded for chapter %d of book %s",
                    chapter["chapter_index"],
                    book_id,
                )

        # Fallback to rules if LLM failed or wasn't tried
        if chapter_analysis is None:
            chapter_analysis = _build_fallback_chapter_analysis(
                chapter,
                chapter["chapter_index"],
                [],  # empty — entities are aggregated at the end
                chapter_candidates,
            )

        # Use LLM entities if available, otherwise regex candidates
        raw_entities = (
            chapter_analysis.get("entities")
            if isinstance(chapter_analysis.get("entities"), list)
            else []
        )
        if not raw_entities:
            raw_entities = chapter_candidates

        normalized = _normalize_chapter_analysis(
            run_id=run_id,
            book_id=book_id,
            workspace_id=workspace_id,
            chapter=chapter,
            chapter_analysis=chapter_analysis,
            knowledge_objects=[],
            evidence_ref=evidence["evidence_ref"],
            evidence_id=evidence["evidence_id"],
        )

        deep_analysis["scenes_by_chapter"][chapter["chapter_id"]] = normalized[
            "scenes"
        ]
        for scene in normalized["scenes"]:
            deep_analysis["events_by_scene"][scene["scene_id"]] = [
                e
                for e in normalized["events"]
                if e["scene_id"] == scene["scene_id"]
            ]
        deep_analysis["conflicts"].update(normalized["conflicts"])
        deep_analysis["hooks"].update(normalized["hooks"])
        deep_analysis["rewards"].update(normalized["rewards"])
        deep_analysis["climaxes"].update(normalized["climaxes"])
        deep_analysis["relationship_edges"].update(normalized["relationships"])

    # Re-aggregate entities with LLM data if available
    if llm_used:
        # entity_lists already has regex entities; LLM entities are used inline
        # Re-aggregate to include any LLM-provided entities
        knowledge_objects = _aggregate_entities(
            entity_lists, run_id, workspace_id
        )

    # Bind evidence to knowledge objects
    for obj_index, obj in enumerate(knowledge_objects):
        if evidences:
            obj["evidence_refs"] = [
                evidences[min(obj_index, len(evidences) - 1)]["evidence_ref"]
            ]

    # Build graph
    graph = _build_graph_from_analysis(
        knowledge_objects,
        deep_analysis["relationship_edges"],
        book_id=book_id,
        run_id=run_id,
    )

    # --- Write everything into the store ---
    for chapter_id, scenes in deep_analysis["scenes_by_chapter"].items():
        store.source_scenes_by_chapter[chapter_id] = scenes

    for scene_id, events in deep_analysis["events_by_scene"].items():
        store.events_by_scene[scene_id] = events

    store.conflicts.update(deep_analysis["conflicts"])
    store.hooks.update(deep_analysis["hooks"])
    store.rewards.update(deep_analysis["rewards"])
    store.climaxes.update(deep_analysis["climaxes"])
    store.relationship_edges.update(deep_analysis["relationship_edges"])

    for obj in knowledge_objects:
        store.knowledge_objects[obj["object_id"]] = obj
    store.knowledge_by_run[run_id] = [
        obj["object_id"] for obj in knowledge_objects
    ]

    store.graph_node_details.update(graph["node_details"])
    store.graph_neighbors_by_node.update(graph["neighbors"])
    store.graph_summaries[book_id] = graph["summary"]

    # Update the extraction run record
    run = store.extraction_runs.get(run_id)
    if run:
        scene_count = sum(
            len(items)
            for items in deep_analysis["scenes_by_chapter"].values()
        )
        run["status"] = "requires_review"
        run["current_stage"] = "quality_review"
        run["chapter_count"] = len(chapters)
        run["scene_count"] = scene_count
        run["object_count"] = len(knowledge_objects)
        run["evidence_count"] = len(evidences)
        run["low_confidence_count"] = len(
            [
                item
                for item in knowledge_objects
                if item.get("review_status") == "pending"
                and item.get("confidence", 1) < 0.8
            ]
        )
        run["finished_at"] = _utc_now()
        task = run.get("task")
        if task:
            task["status"] = "requires_review"
            task["progress"] = 100
            task["finished_at"] = _utc_now()

    logger.info(
        "Extraction complete for book %s: %d scenes, %d objects, %d events, llm=%s",
        book_id,
        scene_count,
        len(knowledge_objects),
        sum(len(v) for v in deep_analysis["events_by_scene"].values()),
        llm_used,
    )
