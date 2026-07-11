import os

import dramatiq

from worker.bootstrap import build_broker
from worker.extraction import run_extract_knowledge
from worker.planning import run_create_chapter_plan, run_create_section_plans
from worker.writing import run_create_writing_run

build_broker(os.getenv("NOVEL_FACTORY_REDIS_URL", "redis://localhost:6379/0"))


@dramatiq.actor(queue_name="task-default")
def noop_task(task_id: str) -> dict[str, str]:
    return {"task_id": task_id, "status": "succeeded"}


@dramatiq.actor(queue_name="task-extraction")
def extract_knowledge(command: dict) -> dict:
    return run_extract_knowledge(command)


@dramatiq.actor(queue_name="task-planning")
def create_chapter_plan(command: dict) -> dict:
    return run_create_chapter_plan(command)


@dramatiq.actor(queue_name="task-planning")
def create_section_plans(command: dict) -> dict:
    return run_create_section_plans(command)


@dramatiq.actor(queue_name="task-writing")
def create_writing_run(command: dict) -> dict:
    return run_create_writing_run(command)
