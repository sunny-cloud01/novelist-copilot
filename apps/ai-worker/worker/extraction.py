from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_extract_knowledge_command(
    book_id: str = BOOK_ID,
    run_id: str = RUN_ID,
    task_id: str = TASK_ID,
    trace_id: str = TRACE_ID,
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
            "output_refs": [f"object://extraction-runs/{run_id}"],
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
                "payload_ref": None,
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


def run_extract_knowledge(command: dict[str, Any]) -> dict[str, Any]:
    fixture = build_extraction_fixture(command)
    return {
        "schema_version": 1,
        "task_id": command["task_id"],
        "status": "requires_review",
        "output_refs": [
            fixture["task"]["output_refs"][0],
            f"object://graph-summaries/{fixture['run']['book_id']}",
            f"object://knowledge-objects/{fixture['run']['run_id']}",
        ],
        "metrics": {
            "pipeline_stages": PIPELINE_STAGES,
            "current_stage": fixture["run"]["current_stage"],
            "chapter_count": fixture["run"]["chapter_count"],
            "scene_count": fixture["run"]["scene_count"],
            "object_count": fixture["run"]["object_count"],
            "evidence_count": fixture["run"]["evidence_count"],
            "low_confidence_count": fixture["run"]["low_confidence_count"],
            "generated_at": utc_now(),
        },
        "errors": [],
        "trace_id": command["trace_id"],
    }
