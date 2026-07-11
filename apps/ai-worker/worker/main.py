import os

import dramatiq

from worker.bootstrap import build_broker

build_broker(os.getenv("NOVEL_FACTORY_REDIS_URL", "redis://localhost:6379/0"))


@dramatiq.actor(queue_name="task-default")
def noop_task(task_id: str) -> dict[str, str]:
    return {"task_id": task_id, "status": "succeeded"}
