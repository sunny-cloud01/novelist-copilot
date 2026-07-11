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


def test_build_extraction_fixture_matches_phase_two_shape() -> None:
    command = build_extract_knowledge_command()

    fixture = build_extraction_fixture(command)

    assert fixture["run"]["run_id"] == RUN_ID
    assert fixture["run"]["book_id"] == BOOK_ID
    assert fixture["run"]["current_stage"] == "quality_review"
    assert fixture["run"]["low_confidence_count"] == 2
    assert len(fixture["knowledge_objects"]) == 3
    assert fixture["graph_summary"]["node_count"] == 3
    assert fixture["events"][1]["payload_json"]["pipeline_stages"] == PIPELINE_STAGES


def test_run_extract_knowledge_returns_requires_review_result() -> None:
    command = build_extract_knowledge_command(trace_id="trace-worker")

    result = run_extract_knowledge(command)

    assert result["task_id"] == TASK_ID
    assert result["status"] == "requires_review"
    assert result["trace_id"] == "trace-worker"
    assert result["metrics"]["current_stage"] == "quality_review"
    assert result["metrics"]["low_confidence_count"] == 2
    assert result["output_refs"][0] == f"object://extraction-runs/{RUN_ID}"


def test_extract_knowledge_actor_name_is_stable() -> None:
    assert extract_knowledge.actor_name == "extract_knowledge"


def test_extract_knowledge_actor_uses_extraction_queue() -> None:
    assert extract_knowledge.queue_name == "task-extraction"


def test_noop_task_actor_name_is_stable() -> None:
    assert noop_task.actor_name == "noop_task"
