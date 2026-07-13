from dataclasses import dataclass
from datetime import datetime, timezone
import os
from time import sleep
from typing import Any, Optional

import dramatiq
from dramatiq import Message
from dramatiq.brokers.redis import RedisBroker

from scheduler.core_store import load_phase_two_store


TASK_ROUTE_MAP = {
    "extract_knowledge": ("task-extraction", "extract_knowledge"),
    "create_chapter_plan": ("task-planning", "create_chapter_plan"),
    "create_section_plans": ("task-planning", "create_section_plans"),
    "create_writing_run": ("task-writing", "create_writing_run"),
}


@dataclass
class SchedulerTickResult:
    requeued: int
    expired_leases: int
    due_retries: int
    ran_at: str


def build_broker(redis_url: str) -> RedisBroker:
    broker = RedisBroker(url=redis_url)
    dramatiq.set_broker(broker)
    return broker


def _build_command(store: Any, task: dict[str, Any]) -> Optional[dict[str, Any]]:
    _, task_kind, entity_id = store._find_task_record(task["task_id"])
    trace_id = task.get("trace_id") or "system-trace"
    if task_kind == "extraction_run":
        run = store.STORE.extraction_runs.get(entity_id)
        if not run:
            return None
        return {
            "schema_version": 1,
            "command_id": f"cmd-{entity_id}",
            "task_id": task["task_id"],
            "task_type": task["task_type"],
            "workspace_id": task["workspace_id"],
            "input_refs": [f"object://source-books/{run['book_id']}", f"object://extraction-runs/{entity_id}"],
            "idempotency_key": task["idempotency_key"],
            "trace_id": trace_id,
            "dispatch_token": task.get("current_dispatch_token"),
            "requested_by": "scheduler",
        }
    if task_kind == "chapter_plan":
        chapter_plan = store.STORE.chapter_plans.get(entity_id)
        if not chapter_plan:
            return None
        return {
            "schema_version": 1,
            "command_id": f"cmd-{entity_id}",
            "task_id": task["task_id"],
            "task_type": task["task_type"],
            "workspace_id": task["workspace_id"],
            "project_id": chapter_plan["project_id"],
            "chapter_plan_id": entity_id,
            "chapter_index": chapter_plan["chapter_index"],
            "target_word_count": chapter_plan["target_word_count"],
            "trace_id": trace_id,
            "dispatch_token": task.get("current_dispatch_token"),
            "requested_by": "scheduler",
        }
    if task_kind == "section_plan":
        return {
            "schema_version": 1,
            "command_id": f"cmd-sections-{entity_id}",
            "task_id": task["task_id"],
            "task_type": task["task_type"],
            "workspace_id": task["workspace_id"],
            "chapter_plan_id": entity_id,
            "section_count": len(store.STORE.section_plans_by_chapter.get(entity_id, [])),
            "trace_id": trace_id,
            "dispatch_token": task.get("current_dispatch_token"),
            "requested_by": "scheduler",
        }
    if task_kind == "writing_run":
        writing_run = store.STORE.writing_runs.get(entity_id)
        if not writing_run:
            return None
        return {
            "schema_version": 1,
            "command_id": f"cmd-{entity_id}",
            "task_id": task["task_id"],
            "task_type": task["task_type"],
            "workspace_id": task["workspace_id"],
            "project_id": writing_run["project_id"],
            "chapter_plan_id": writing_run["chapter_plan_id"],
            "writing_run_id": entity_id,
            "writer_model_profile_id": writing_run["writer_model_profile_id"],
            "critic_model_profile_id": writing_run["critic_model_profile_id"],
            "humanizer_model_profile_id": writing_run["humanizer_model_profile_id"],
            "trace_id": trace_id,
            "dispatch_token": task.get("current_dispatch_token"),
            "requested_by": "scheduler",
        }
    return None


def _enqueue_task(broker: RedisBroker, task: dict[str, Any], command: dict[str, Any]) -> None:
    queue_name, actor_name = TASK_ROUTE_MAP[task["task_type"]]
    broker.enqueue(
        Message(
            queue_name=queue_name,
            actor_name=actor_name,
            args=(command,),
            kwargs={},
            options={},
        )
    )


def run_scheduler_tick(now: Optional[datetime] = None, broker: Optional[RedisBroker] = None) -> SchedulerTickResult:
    current = now or datetime.now(timezone.utc)
    runtime_store = load_phase_two_store()
    active_broker = broker or build_broker(os.getenv("NOVEL_FACTORY_REDIS_URL", "redis://localhost:6379/0"))
    current_iso = current.isoformat()
    expired = runtime_store.recover_expired_runtime_tasks(
        now=current_iso,
        request_id="system-scheduler-recovery",
        trace_id="system-scheduler-recovery",
        actor_id="scheduler",
    )
    due_retry_tasks = runtime_store.list_due_retry_tasks(now=current_iso)
    dispatched = 0
    for task in [*runtime_store.list_runtime_tasks("queued"), *due_retry_tasks]:
        if task["task_type"] not in TASK_ROUTE_MAP:
            continue
        dispatched_task = runtime_store.mark_task_dispatched(task["task_id"], trace_id=task.get("trace_id") or "system-trace", dispatched_at=current_iso)
        if not dispatched_task or dispatched_task.get("status") != "running" or not dispatched_task.get("current_dispatch_token"):
            continue
        command = _build_command(runtime_store, dispatched_task)
        if not command:
            continue
        _enqueue_task(active_broker, dispatched_task, command)
        dispatched += 1
    return SchedulerTickResult(
        requeued=dispatched,
        expired_leases=len(expired),
        due_retries=len(due_retry_tasks),
        ran_at=current_iso,
    )


def run_scheduler_loop(interval_seconds: float) -> None:
    while True:
        print(run_scheduler_tick())
        sleep(interval_seconds)


if __name__ == "__main__":
    run_scheduler_loop(float(os.getenv("NOVEL_FACTORY_SCHEDULER_INTERVAL_SECONDS", "5")))
