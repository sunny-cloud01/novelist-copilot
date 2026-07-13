from __future__ import annotations

import importlib
import sys
from pathlib import Path
from uuid import uuid4

import pytest


def _purge_app_modules() -> None:
    for name in list(sys.modules):
        if name == "app" or name.startswith("app.") or name == "phase_two_persistence":
            sys.modules.pop(name)


def _snapshot_file(database: str) -> Path:
    return Path("/tmp") / f"{database}-localhost-5999-core-store.snapshot.json"


def _projection_file(database: str) -> Path:
    return Path("/tmp") / f"{database}-localhost-5999-runtime-projection.snapshot.json"


def _load_store_module():
    _purge_app_modules()
    return importlib.import_module("app.core.phase_two_store")


def _load_business_persistence_module():
    _purge_app_modules()
    return importlib.import_module("app.core.business_persistence")


def test_phase_two_store_restores_persisted_workspace_and_project(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_persistence_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    created = store.create_workspace({"name": "持久化工作区", "slug": "persist-workspace"})
    workspace_id = created["workspace"]["workspace_id"]
    project_bundle = store.create_novel_project(
        {
            "workspace_id": workspace_id,
            "title": "持久化项目",
            "genre_scope": ["xianxia"],
        },
        trace_id="trace-persist-project",
        actor_id=store.USER_ID,
        actor_role="owner",
        workspace_id=workspace_id,
    )
    project_id = project_bundle["project"]["project_id"]

    reloaded = _load_store_module()
    workspace = reloaded.get_workspace(workspace_id)
    project = reloaded.get_novel_project(project_id)

    assert workspace is not None
    assert workspace["workspace"]["name"] == "持久化工作区"
    assert project is not None
    assert project["project"]["title"] == "持久化项目"
    assert project["project"]["workspace_id"] == workspace_id

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()


def test_runtime_projection_uses_canonical_object_refs_and_stable_checksums(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_projection_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    store._persist_store()

    created = store.create_book(
        {
            "title": "对象元数据测试书",
            "author_name": "tester",
            "source_type": "reference_novel",
            "source_text": "第一章\n测试正文。",
        },
        trace_id="trace-object-metadata",
    )
    projection = store.load_runtime_projection()
    object_rows = {item["object_ref"]: item for item in projection["objects"]}

    assert f"object://source-books/{store.BOOK_ID}" in object_rows
    assert f"object://writing-runs/{store.WRITING_RUN_ID}" in object_rows
    assert f"object://knowledge-objects/01JZOBJ0000000000000000001" in object_rows
    assert f"object://graph-summaries/{store.BOOK_ID}" in object_rows
    source_content_id = store.STORE.source_content_by_book[created["book_id"]]
    source_content = store.STORE.source_contents[source_content_id]
    assert object_rows[f"object://source-books/{store.BOOK_ID}"]["storage_key"] == f"source-books/{store.BOOK_ID}"
    assert object_rows[f"object://source-contents/{source_content_id}"]["checksum"] == source_content["checksum"]
    assert object_rows[f"object://source-contents/{source_content_id}"]["byte_size"] == source_content["byte_size"]
    assert object_rows[f"object://source-contents/{source_content_id}"]["mime_type"] == "text/plain; charset=utf-8"
    assert object_rows[f"object://source-contents/{source_content_id}"]["storage_key"] == f"source-contents/{source_content_id}"
    assert all(not ref.startswith("object://source-book/") for ref in object_rows)
    assert all(not ref.startswith("object://writing-run/") for ref in object_rows)

    first_checksum = object_rows[f"object://writing-runs/{store.WRITING_RUN_ID}"]["checksum"]
    reloaded = _load_store_module()
    reloaded_projection = reloaded.load_runtime_projection()
    reloaded_rows = {item["object_ref"]: item for item in reloaded_projection["objects"]}

    assert reloaded_rows[f"object://writing-runs/{store.WRITING_RUN_ID}"]["checksum"] == first_checksum

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()


def test_runtime_projection_restores_task_state_machine_fields(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_runtime_tasks_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 21, "target_word_count": 4200, "payload": {}},
        trace_id="trace-persist-plan",
    )
    assert created_plan is not None
    task_id = created_plan["task"]["task_id"]
    task = store.STORE.chapter_plan_tasks[created_plan["chapter_plan"]["chapter_plan_id"]]
    task["lease_owner"] = "scheduler-node-1"
    task["lease_expires_at"] = "2026-07-12T00:05:00Z"
    task["heartbeat_at"] = "2026-07-12T00:01:00Z"
    task["next_retry_at"] = "2026-07-12T00:10:00Z"
    task["max_retry_count"] = 5
    task["blocked_reason"] = "waiting_on_story_bible"
    store._persist_store()

    projection = store.load_runtime_projection()
    task_lock = next(item for item in projection["task_locks"] if item["task_id"] == task_id)
    assert task_lock["lock_owner"] == "scheduler-node-1"
    assert task_lock["lease_expires_at"] == "2026-07-12T00:05:00Z"
    assert task_lock["heartbeat_at"] == "2026-07-12T00:01:00Z"

    reloaded = _load_store_module()
    runtime_task = next(item for item in reloaded.list_runtime_tasks() if item["task_id"] == task_id)

    assert runtime_task["lease_owner"] == "scheduler-node-1"
    assert runtime_task["lease_expires_at"] == "2026-07-12T00:05:00Z"
    assert runtime_task["heartbeat_at"] == "2026-07-12T00:01:00Z"
    assert runtime_task["next_retry_at"] == "2026-07-12T00:10:00Z"
    assert runtime_task["max_retry_count"] == 5
    assert runtime_task["blocked_reason"] == "waiting_on_story_bible"

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()



def test_runtime_projection_restores_retrying_and_review_recovery_fields(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_runtime_recovery_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 22, "target_word_count": 4300, "payload": {}},
        trace_id="trace-retry-restore",
    )
    task_id = created_plan["task"]["task_id"]
    first_dispatch = store.mark_task_dispatched(
        task_id,
        trace_id="trace-retry-restore",
        dispatched_at="2026-07-12T00:00:00+00:00",
    )
    assert first_dispatch is not None
    first_token = first_dispatch["current_dispatch_token"]
    store.schedule_task_retry(task_id, "lease_expired", trace_id="trace-retry-restore", retry_at="2026-07-12T00:10:00+00:00")
    store._persist_store()

    reloaded = _load_store_module()
    runtime_task = next(item for item in reloaded.list_runtime_tasks() if item["task_id"] == task_id)
    chapter_plan = reloaded.get_chapter_plan(created_plan["chapter_plan"]["chapter_plan_id"])

    assert runtime_task["status"] == "retrying"
    assert runtime_task["next_retry_at"] == "2026-07-12T00:10:00+00:00"
    assert runtime_task["lease_owner"] is None
    assert runtime_task["current_dispatch_token"] is None
    assert chapter_plan["chapter_plan"]["status"] == "retrying"

    second_dispatch = reloaded.mark_task_dispatched(
        task_id,
        trace_id="trace-retry-restore",
        dispatched_at="2026-07-12T00:11:00+00:00",
    )
    assert second_dispatch is not None
    assert second_dispatch["current_dispatch_token"] != first_token

    created_writing = reloaded.create_writing_run(
        {"project_id": reloaded.PROJECT_ID, "chapter_plan_id": reloaded.CHAPTER_PLAN_ID},
        trace_id="trace-review-restore",
    )
    writing_task_id = created_writing["task"]["task_id"]
    writing_task = reloaded.STORE.writing_run_tasks[created_writing["writing_run"]["writing_run_id"]]
    writing_task["status"] = "running"
    writing_task["lease_owner"] = "worker-review"
    writing_task["lease_expires_at"] = "2026-07-12T00:00:00+00:00"
    writing_task["heartbeat_at"] = "2026-07-12T00:00:00+00:00"
    writing_task["retry_count"] = writing_task["max_retry_count"]
    writing_task["error_code"] = "structured_output_validation_failed"
    reloaded.recover_task_for_manual_review(writing_task_id, "structured_output_validation_failed", trace_id="trace-review-restore")
    reloaded._persist_store()

    recovered = _load_store_module().get_writing_run(created_writing["writing_run"]["writing_run_id"])
    assert recovered["task"]["status"] == "requires_review"
    assert recovered["task"]["review_required"] is True
    assert recovered["task"]["lease_owner"] is None
    assert recovered["writing_run"]["status"] == "requires_review"

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()


def test_runtime_projection_persists_extraction_artifact_refs_and_memory_snapshot(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_runtime_objects_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    store._persist_store()

    projection = store.load_runtime_projection()
    object_rows = {item["object_ref"]: item for item in projection["objects"]}

    knowledge_package_ref = f"object://knowledge-packages/{store.RUN_ID}"
    graph_package_ref = f"object://graph-packages/{store.BOOK_ID}"
    extraction_report_ref = f"object://extraction-reports/{store.RUN_ID}"
    quality_report_ref = f"object://quality-reports/{store.RUN_ID}"
    assert knowledge_package_ref in object_rows
    assert graph_package_ref in object_rows
    assert extraction_report_ref in object_rows
    assert quality_report_ref in object_rows
    assert object_rows[knowledge_package_ref]["mime_type"] == "application/json"
    assert object_rows[knowledge_package_ref]["byte_size"] > 0
    assert object_rows[graph_package_ref]["mime_type"] == "application/json"
    assert object_rows[graph_package_ref]["byte_size"] > 0
    assert object_rows[extraction_report_ref]["mime_type"] == "application/json"
    assert object_rows[extraction_report_ref]["byte_size"] > 0
    assert object_rows[quality_report_ref]["mime_type"] == "application/json"
    assert object_rows[quality_report_ref]["byte_size"] > 0

    reloaded = _load_store_module()
    memory_package = reloaded.STORE.memory_packages[reloaded.MEMORY_PACKAGE_ID]
    extraction_run = reloaded.get_extraction_run(reloaded.RUN_ID)

    assert memory_package["source_snapshot_id"] == f"snapshot://knowledge-state/{reloaded.WRITING_RUN_ID}"
    assert extraction_run["knowledge_package_ref"] == knowledge_package_ref
    assert extraction_run["graph_package_ref"] == graph_package_ref
    assert extraction_run["extraction_report_ref"] == extraction_report_ref
    assert extraction_run["quality_report_ref"] == quality_report_ref

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()


def test_runtime_projection_persists_writing_artifact_metadata(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_writing_objects_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    store._persist_store()

    projection = store.load_runtime_projection()
    object_rows = {item["object_ref"]: item for item in projection["objects"]}

    section_run = store.STORE.section_runs_by_writing[store.WRITING_RUN_ID][1]
    draft_ref = section_run["draft_object_ref"]
    critic_ref = section_run["critic_report_ref"]
    humanized_ref = section_run["humanized_object_ref"]
    reviewer_note_ref = store.STORE.revision_summaries["01JZREVISION0000000000001"]["reviewer_note_ref"]
    quality_comment_ref = store.STORE.feedback_records["01JZFDBK0000000000000001"]["comment_ref"]
    critic_comment_ref = store.STORE.feedback_records["01JZFDBK0000000000000002"]["comment_ref"]

    assert object_rows[draft_ref]["mime_type"] == "text/plain; charset=utf-8"
    assert object_rows[draft_ref]["byte_size"] == len(section_run["writer_output"].encode("utf-8"))
    assert object_rows[critic_ref]["mime_type"] == "application/json"
    assert object_rows[critic_ref]["byte_size"] > 0
    assert object_rows[humanized_ref]["mime_type"] == "text/plain; charset=utf-8"
    assert object_rows[humanized_ref]["byte_size"] == len(section_run["humanized_text"].encode("utf-8"))
    assert object_rows[reviewer_note_ref]["mime_type"] == "text/plain; charset=utf-8"
    assert object_rows[reviewer_note_ref]["byte_size"] == len(store.STORE.revision_summaries["01JZREVISION0000000000001"]["change_summary"].encode("utf-8"))
    assert object_rows[quality_comment_ref]["bucket"] == "quality-comments"
    assert object_rows[quality_comment_ref]["mime_type"] == "text/plain; charset=utf-8"
    assert object_rows[quality_comment_ref]["byte_size"] > 0
    assert object_rows[critic_comment_ref]["bucket"] == "critic-comments"
    assert object_rows[critic_comment_ref]["mime_type"] == "text/plain; charset=utf-8"
    assert object_rows[critic_comment_ref]["byte_size"] > 0

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()


def test_save_snapshot_requires_explicit_fallback_when_postgres_unavailable(monkeypatch) -> None:
    monkeypatch.delenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", raising=False)
    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{uuid4().hex}")

    persistence = importlib.import_module("app.core.persistence")

    with pytest.raises(RuntimeError, match="file persistence fallback disabled"):
        persistence.save_snapshot({"hello": "world"}, snapshot_key="fallback-disabled")



def test_save_snapshot_uses_file_fallback_only_when_enabled(monkeypatch) -> None:
    database = f"package1_fallback_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    persistence = importlib.import_module("app.core.persistence")
    payload = {"hello": "fallback"}
    persistence.save_snapshot(payload, snapshot_key="core-store")

    assert snapshot_file.exists()
    assert persistence.load_snapshot() == payload

    snapshot_file.unlink()



def test_sync_runtime_projection_requires_explicit_fallback_when_postgres_unavailable(monkeypatch) -> None:
    database = f"package1_projection_blocked_{uuid4().hex}"
    projection_file = _projection_file(database)
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.delenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", raising=False)
    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    persistence = importlib.import_module("app.core.persistence")

    with pytest.raises(RuntimeError, match="file persistence fallback disabled"):
        persistence.sync_runtime_projection(objects=[], tasks=[], task_locks=[], task_events=[], audit_events=[])

    assert not projection_file.exists()





def test_mark_task_dispatched_ignores_illegal_duplicate_dispatch(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_dispatch_guard_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 23, "target_word_count": 4100, "payload": {}},
        trace_id="trace-dispatch-guard",
    )
    task_id = created_plan["task"]["task_id"]

    first = store.mark_task_dispatched(task_id, trace_id="trace-dispatch-guard", request_id="dispatch-1", dispatched_at="2026-07-12T00:00:00+00:00")
    second = store.mark_task_dispatched(task_id, trace_id="trace-dispatch-guard-2", request_id="dispatch-2", dispatched_at="2026-07-12T00:01:00+00:00")
    refreshed = store.get_chapter_plan(created_plan["chapter_plan"]["chapter_plan_id"])
    dispatched_events = [event for event in refreshed["events"] if event["event_type"] == "dispatched"]

    assert first is not None
    assert second is not None
    assert first["current_dispatch_token"] == second["current_dispatch_token"]
    assert refreshed["task"]["lease_owner"] == "scheduler"
    assert refreshed["task"]["heartbeat_at"] == "2026-07-12T00:00:00+00:00"
    assert len(dispatched_events) == 1

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()


def test_apply_task_execution_result_ignores_stale_completion_after_retry(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_stale_completion_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_plan = store.create_chapter_plan(
        {"project_id": store.PROJECT_ID, "chapter_index": 24, "target_word_count": 4200, "payload": {}},
        trace_id="trace-stale-completion",
    )
    task_id = created_plan["task"]["task_id"]
    dispatched = store.mark_task_dispatched(task_id, trace_id="trace-stale-completion", request_id="dispatch-1", dispatched_at="2026-07-12T00:00:00+00:00")
    stale_token = dispatched["current_dispatch_token"]
    store.schedule_task_retry(task_id, "lease_expired", trace_id="trace-stale-completion", retry_at="2026-07-12T00:01:00+00:00")
    redispached = store.mark_task_dispatched(task_id, trace_id="trace-stale-completion", request_id="dispatch-2", dispatched_at="2026-07-12T00:01:00+00:00")

    stale = store.apply_task_execution_result(
        task_id,
        "succeeded",
        [f"object://chapter-plans/{created_plan['chapter_plan']['chapter_plan_id']}"],
        {"current_stage": "quality_review", "latency_ms": 50},
        trace_id="trace-stale-completion",
        dispatch_token=stale_token,
    )
    refreshed = store.get_chapter_plan(created_plan["chapter_plan"]["chapter_plan_id"])

    assert stale is not None
    assert redispached is not None
    assert refreshed["task"]["status"] == "running"
    assert refreshed["task"]["current_dispatch_token"] == redispached["current_dispatch_token"]
    assert refreshed["events"][-1]["event_type"] == "dispatched"

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

def test_source_content_and_chapters_round_trip_through_runtime_projection(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_source_content_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    source_text = "第一章 山边小村\n韩立站在村口。\n第二章 入门试炼\n少年踏上青石阶。"
    created = store.create_book(
        {
            "title": "凡人修仙传",
            "author_name": "忘语",
            "source_type": "reference_novel",
            "source_text": source_text,
        },
        trace_id="trace-source-content-persist",
    )
    store._persist_store()

    reloaded = _load_store_module()
    source_content = reloaded.get_book_source_content(created["book_id"])
    chapters = reloaded.list_book_chapters(created["book_id"])
    projection = reloaded.load_runtime_projection()
    object_refs = {item["object_ref"] for item in projection["objects"]}

    assert source_content["content"] == source_text
    assert len(chapters) == 2
    assert chapters[0]["text_object_ref"].startswith("object://source-chapters/")
    assert created["source_content_ref"] in object_refs
    assert chapters[0]["text_object_ref"] in object_refs

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

def test_runtime_projection_persists_manuscript_object_metadata_after_acceptance(monkeypatch) -> None:
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    database = f"package1_manuscript_objects_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    projection_file = _projection_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    store.reset_store()
    store.seed_phase_two_demo_data()
    store.apply_writing_review_action(
        store.WRITING_RUN_ID,
        {
            "action": "mark_issue_resolved",
            "issue_id": "01JZCONSISTISSUE000000001",
            "note": "resolved",
            "output_ref": f"object://revision-summaries/{store.STORE.writing_runs[store.WRITING_RUN_ID]['revision_summary_id']}",
        },
        trace_id="trace-manuscript-objects",
    )
    store.apply_writing_review_action(
        store.WRITING_RUN_ID,
        {
            "action": "approve_draft",
            "note": "approved",
            "output_ref": "object://review-notes/approved",
        },
        trace_id="trace-manuscript-objects",
    )
    accepted = store.accept_chapter(store.WRITING_RUN_ID, trace_id="trace-manuscript-objects")
    assert accepted is not None

    projection = store.load_runtime_projection()
    object_rows = {item["object_ref"]: item for item in projection["objects"]}
    accepted_ref = accepted["data"]["writing_run"]["accepted_chapter_ref"] if "data" in accepted else accepted["writing_run"]["accepted_chapter_ref"]
    chapter_snapshot_id = accepted["data"]["chapter_snapshot"]["chapter_snapshot_id"] if "data" in accepted else accepted["chapter_snapshot"]["chapter_snapshot_id"]

    assert accepted_ref in object_rows
    assert object_rows[accepted_ref]["bucket"] == "manuscripts"
    assert object_rows[accepted_ref]["storage_key"] == accepted_ref.removeprefix("object://")
    assert object_rows[accepted_ref]["mime_type"] == "text/plain; charset=utf-8"
    assert object_rows[accepted_ref]["byte_size"] == len(store.STORE.writing_runs[store.WRITING_RUN_ID]["assembled_chapter"].encode("utf-8"))
    assert object_rows[f"object://chapter-snapshots/{chapter_snapshot_id}"]["checksum"] == object_rows[accepted_ref]["checksum"]

    reloaded = _load_store_module()
    reloaded_run = reloaded.get_writing_run(store.WRITING_RUN_ID)
    assert reloaded_run["writing_run"]["accepted_chapter_ref"] == accepted_ref
    assert reloaded_run["chapter_snapshot"]["accepted_chapter_ref"] == accepted_ref

    if snapshot_file.exists():
        snapshot_file.unlink()
    if projection_file.exists():
        projection_file.unlink()


def test_business_backfill_records_migration_event(monkeypatch) -> None:
    psycopg = pytest.importorskip("psycopg")
    database = f"business_backfill_{uuid4().hex}"
    admin_url = "postgresql://novel:novel@localhost:5436/novel_factory"
    target_url = f"postgresql://novel:novel@localhost:5436/{database}"
    try:
        with psycopg.connect(admin_url, autocommit=True) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f'CREATE DATABASE "{database}"')
    except Exception as exc:
        pytest.skip(f"local postgres unavailable: {exc}")

    try:
        monkeypatch.delenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", raising=False)
        monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", target_url)

        store = _load_store_module()
        store.reset_store()
        store.seed_phase_two_demo_data()
        snapshot = store.asdict(store.STORE)
        snapshot_hash = _load_business_persistence_module()._snapshot_hash(snapshot)
        _load_business_persistence_module().backfill_business_state_from_snapshot(snapshot)

        reloaded = _load_store_module()
        assert reloaded.STORE.migration_events
        migration_event = reloaded.STORE.migration_events[-1]
        assert migration_event["migration_id"].startswith("business-backfill:")
        assert migration_event["snapshot_hash"] == snapshot_hash
        assert migration_event["rollback_note"] == "business tables backfilled from snapshot"
        assert "core.source_books" in migration_event["affected_tables"]
        assert migration_event["row_counts"]["books"] >= 1
        assert migration_event["row_counts"]["writing_runs"] >= 1

        with psycopg.connect(target_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT snapshot_hash, rollback_note FROM audit.migration_events ORDER BY created_at DESC, migration_id DESC LIMIT 1")
                row = cursor.fetchone()
                assert row is not None
                assert row[0] == snapshot_hash
                assert row[1] == "business tables backfilled from snapshot"
    finally:
        _purge_app_modules()
        with psycopg.connect(admin_url, autocommit=True) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s AND pid <> pg_backend_pid()",
                    (database,),
                )
                cursor.execute(f'DROP DATABASE IF EXISTS "{database}"')


def test_business_tables_round_trip_without_snapshot(monkeypatch) -> None:
    psycopg = pytest.importorskip("psycopg")
    database = f"business_tables_{uuid4().hex}"
    admin_url = "postgresql://novel:novel@localhost:5436/novel_factory"
    target_url = f"postgresql://novel:novel@localhost:5436/{database}"
    try:
        with psycopg.connect(admin_url, autocommit=True) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f'CREATE DATABASE "{database}"')
    except Exception as exc:
        pytest.skip(f"local postgres unavailable: {exc}")

    try:
        monkeypatch.delenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", raising=False)
        monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", target_url)

        store = _load_store_module()
        created_book = store.create_book(
            {
                "title": "真实业务表测试书",
                "author_name": "测试作者",
                "source_type": "reference_novel",
                "source_text": "第一章 真表\n主角在雨夜进入旧书楼。",
            },
            trace_id="trace-business-proof",
        )
        created_project = store.create_novel_project(
            {
                "title": "真实业务表项目",
                "genre_scope": "玄幻",
                "story_bible_payload": {
                    "premise": "真实业务表恢复测试。",
                    "protagonist": "林澈",
                    "core_conflict": "旧书楼秘密。",
                },
            },
            trace_id="trace-business-project",
        )

        with psycopg.connect(target_url) as connection:
            with connection.cursor() as cursor:
                expected_counts = {
                    "identity.workspaces": 1,
                    "config.model_profiles": 2,
                    "core.source_books": 2,
                    "core.source_contents": 1,
                    "core.source_chapters": 3,
                    "core.knowledge_objects": 3,
                    "core.graph_snapshots": 1,
                    "core.novel_projects": 2,
                    "core.story_bibles": 2,
                    "ai.writing_runs": 1,
                    "core.quality_reports": 1,
                    "core.feedback_records": 2,
                }
                for table_name, minimum in expected_counts.items():
                    cursor.execute(f"SELECT count(*) FROM {table_name}")
                    assert cursor.fetchone()[0] >= minimum, table_name
                cursor.execute("DELETE FROM app_state_snapshots")
            connection.commit()

        reloaded = _load_store_module()
        assert reloaded.get_book(created_book["book_id"])["title"] == "真实业务表测试书"
        assert reloaded.get_book_source_content(created_book["book_id"])["content"].startswith("第一章 真表")
        assert reloaded.get_novel_project(created_project["project"]["project_id"])["project"]["title"] == "真实业务表项目"
        assert reloaded.get_writing_run(reloaded.WRITING_RUN_ID)["writing_run"]["status"] == "requires_review"
    finally:
        _purge_app_modules()
        with psycopg.connect(admin_url, autocommit=True) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s AND pid <> pg_backend_pid()",
                    (database,),
                )
                cursor.execute(f'DROP DATABASE IF EXISTS "{database}"')

