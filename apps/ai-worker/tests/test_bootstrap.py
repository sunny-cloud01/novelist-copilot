from worker.bootstrap import build_broker
from worker.main import noop_task


def test_build_broker_sets_a_redis_broker() -> None:
    broker = build_broker("redis://localhost:6379/0")
    host = broker.client.connection_pool.connection_kwargs["host"]
    assert host == "localhost"


def test_noop_task_actor_name_is_stable() -> None:
    assert noop_task.actor_name == "noop_task"
