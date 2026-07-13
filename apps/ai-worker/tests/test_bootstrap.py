from worker.core_store import load_phase_two_store
from worker.extraction import (
    BOOK_ID,
    PIPELINE_STAGES,
    RUN_ID,
    TASK_ID,
    build_extract_knowledge_command,
    build_extraction_fixture,
    run_extract_knowledge,
)
from worker.main import extract_knowledge, noop_task
import worker.extraction as extraction_module


def dispatch_task(store, task_id: str, trace_id: str) -> str:
    task = store.mark_task_dispatched(task_id, trace_id=trace_id)
    assert task is not None
    assert task["current_dispatch_token"] is not None
    return task["current_dispatch_token"]


def test_build_extraction_fixture_matches_phase_two_shape() -> None:
    command = build_extract_knowledge_command()

    fixture = build_extraction_fixture(command)

    assert fixture["run"]["run_id"] == RUN_ID
    assert fixture["run"]["book_id"] == BOOK_ID
    assert fixture["run"]["current_stage"] == "quality_review"
    assert fixture["run"]["low_confidence_count"] == 0
    assert fixture["run"]["knowledge_package_ref"] == f"object://knowledge-packages/{RUN_ID}"
    assert fixture["run"]["graph_package_ref"] == f"object://graph-packages/{BOOK_ID}"
    assert fixture["run"]["extraction_report_ref"] == f"object://extraction-reports/{RUN_ID}"
    assert fixture["run"]["quality_report_ref"] == f"object://quality-reports/{RUN_ID}"
    assert isinstance(fixture["knowledge_objects"], list)
    assert isinstance(fixture["graph_summary"]["nodes"], list)
    assert fixture["events"][1]["payload_json"]["pipeline_stages"] == PIPELINE_STAGES


def test_run_extract_knowledge_returns_requires_review_result() -> None:
    store = load_phase_two_store()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_book = store.create_book(
        {
            "title": "Worker Extraction Book",
            "author_name": "demo",
            "source_type": "reference_novel",
            "source_text": "第一章 雨夜\n主角在雨夜进入旧书楼。\n第二章 旧约\n旧书楼里出现新的修行线索。",
        },
        trace_id="trace-worker-book",
    )
    created_run = store.create_extraction_run(created_book["book_id"], trace_id="trace-worker")
    dispatch_token = dispatch_task(store, created_run["task"]["task_id"], trace_id="trace-worker")
    command = build_extract_knowledge_command(
        book_id=created_book["book_id"],
        run_id=created_run["run_id"],
        task_id=created_run["task"]["task_id"],
        trace_id="trace-worker",
        dispatch_token=dispatch_token,
    )

    result = run_extract_knowledge(command)
    report = load_phase_two_store().get_extraction_report(created_run["run_id"])

    assert result["task_id"] == created_run["task"]["task_id"]
    assert result["status"] == "requires_review"
    assert result["trace_id"] == "trace-worker"
    assert result["metrics"]["current_stage"] == "quality_review"
    assert result["metrics"]["analysis_mode"] == "fallback"
    assert result["metrics"]["low_confidence_count"] == 2
    assert result["metrics"]["provider_calls"]
    assert result["metrics"]["deep_analysis"]["scenes_by_chapter"]
    assert result["metrics"]["deep_analysis"]["events_by_scene"]
    assert result["metrics"]["deep_analysis"]["conflicts"]
    assert result["metrics"]["deep_analysis"]["hooks"]
    assert result["metrics"]["deep_analysis"]["rewards"]
    assert result["metrics"]["deep_analysis"]["climaxes"]
    assert result["metrics"]["deep_analysis"]["relationship_edges"]
    assert result["metrics"]["evidences"][0]["excerpt"].startswith("第一章 雨夜")
    assert result["output_refs"] == [
        f"object://extraction-runs/{created_run['run_id']}",
        f"object://knowledge-packages/{created_run['run_id']}",
        f"object://graph-packages/{created_book['book_id']}",
        f"object://extraction-reports/{created_run['run_id']}",
        f"object://quality-reports/{created_run['run_id']}",
    ]
    assert report["run"]["status"] == "requires_review"
    assert report["run"]["book_id"] == created_book["book_id"]
    assert report["run"]["knowledge_package_ref"] == f"object://knowledge-packages/{created_run['run_id']}"
    assert report["run"]["graph_package_ref"] == f"object://graph-packages/{created_book['book_id']}"
    assert report["run"]["extraction_report_ref"] == f"object://extraction-reports/{created_run['run_id']}"
    assert report["run"]["quality_report_ref"] == f"object://quality-reports/{created_run['run_id']}"
    assert len(report["low_confidence_items"]) == 2




def test_run_extract_knowledge_uses_provider_when_structured_json_returns(monkeypatch) -> None:
    store = load_phase_two_store()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_book = store.create_book(
        {
            "title": "Provider Extraction Book",
            "author_name": "demo",
            "source_type": "reference_novel",
            "source_text": "第一章 雨夜\n主角在雨夜进入旧书楼。",
        },
        trace_id="trace-provider-book",
    )
    created_run = store.create_extraction_run(created_book["book_id"], trace_id="trace-provider")
    store.STORE.model_profiles[store.DEFAULT_MODEL_PROFILE_ID]["provider_name"] = "deepseek"
    store.STORE.model_profiles[store.MODEL_PROFILE_STRUCTURED_FALLBACK_ID]["provider_name"] = "deepseek"
    dispatch_token = dispatch_task(store, created_run["task"]["task_id"], trace_id="trace-provider")
    command = build_extract_knowledge_command(
        book_id=created_book["book_id"],
        run_id=created_run["run_id"],
        task_id=created_run["task"]["task_id"],
        trace_id="trace-provider",
        dispatch_token=dispatch_token,
    )

    def fake_completion(**_: object) -> dict[str, object]:
        return {
            "summary": "主角夜探旧书楼，线索出现。",
            "scenes": [
                {
                    "title": "雨夜入楼",
                    "summary": "主角冒雨进入旧书楼。",
                    "text_range": "c1:p1-p2",
                    "participants": ["Xiao Yan"],
                    "event": {
                        "event_type": "discovery",
                        "cause": "主角主动追查。",
                        "action": "进入旧书楼搜寻。",
                        "result": "发现修行线索。",
                        "consequence": "后续成长线被开启。",
                        "participants": ["Xiao Yan"],
                        "confidence": 0.93,
                    },
                    "conflict": {
                        "parties": ["Xiao Yan", "unknown pressure"],
                        "objective": "找到逆转契机。",
                        "pressure": "时间和未知风险逼近。",
                        "escalation_level": 4,
                        "resolution_state": "open",
                        "confidence": 0.88,
                    },
                    "hook": {
                        "hook_type": "mystery",
                        "open_question": "旧书楼线索会把主角带向哪里？",
                        "introduced_at": "chapter:1",
                        "expected_resolution_range": "future_chapters",
                        "confidence": 0.86,
                    },
                    "reward": {
                        "reward_type": "discovery",
                        "beneficiary_character_id": "Xiao Yan",
                        "reader_effect": "看到逆转苗头。",
                        "intensity": 0.84,
                        "payoff_target": "cultivation_upgrade",
                        "confidence": 0.83,
                    },
                    "climax": {
                        "scope_type": "chapter",
                        "intensity": 0.87,
                        "aftermath": "读者期待主角继续追查。",
                        "confidence": 0.82,
                    },
                }
            ],
            "relationships": [
                {
                    "source": "Xiao Yan",
                    "relation_type": "seeks",
                    "target": "Yao Lao",
                    "confidence": 0.71,
                }
            ],
        }

    monkeypatch.setattr(extraction_module, "_openai_json_completion", fake_completion)

    result = run_extract_knowledge(command)

    assert result["metrics"]["analysis_mode"] == "provider"
    assert result["metrics"]["provider_calls"][-1]["status"] == "succeeded"
    chapter_scenes = next(iter(result["metrics"]["deep_analysis"]["scenes_by_chapter"].values()))
    assert chapter_scenes[0]["title"] == "雨夜入楼"
    relationship = next(iter(result["metrics"]["deep_analysis"]["relationship_edges"].values()))
    assert relationship["relation_type"] == "seeks"





def test_run_extract_knowledge_keeps_running_on_stale_dispatch_token() -> None:
    store = load_phase_two_store()
    store.reset_store()
    store.seed_phase_two_demo_data()
    created_book = store.create_book(
        {
            "title": "Worker Extraction Stale Book",
            "author_name": "demo",
            "source_type": "reference_novel",
            "source_text": "第一章 雨夜\n主角在雨夜进入旧书楼。\n第二章 旧约\n旧书楼里出现新的修行线索。",
        },
        trace_id="trace-worker-stale-book",
    )
    created_run = store.create_extraction_run(created_book["book_id"], trace_id="trace-worker-stale")
    first_token = dispatch_task(store, created_run["task"]["task_id"], trace_id="trace-worker-stale")
    store.schedule_task_retry(created_run["task"]["task_id"], "lease_expired", trace_id="trace-worker-stale")
    fresh_token = store.mark_task_dispatched(
        created_run["task"]["task_id"],
        trace_id="trace-worker-stale-2",
    )["current_dispatch_token"]
    command = build_extract_knowledge_command(
        book_id=created_book["book_id"],
        run_id=created_run["run_id"],
        task_id=created_run["task"]["task_id"],
        trace_id="trace-worker-stale",
        dispatch_token=first_token,
    )

    result = run_extract_knowledge(command)
    report = load_phase_two_store().get_extraction_report(created_run["run_id"])

    assert first_token != fresh_token
    assert result["status"] == "running"
    assert report["task"]["status"] == "running"
    assert report["task"]["current_dispatch_token"] == fresh_token
    assert all(event["event_type"] not in {"review_required", "succeeded", "failed"} for event in report["events"][-2:])


def test_extract_knowledge_actor_uses_extraction_queue() -> None:
    assert extract_knowledge.queue_name == "task-extraction"


def test_noop_task_actor_name_is_stable() -> None:
    assert noop_task.actor_name == "noop_task"
