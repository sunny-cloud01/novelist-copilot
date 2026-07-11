import dramatiq
from dramatiq.brokers.redis import RedisBroker


def build_broker(redis_url: str) -> RedisBroker:
    broker = RedisBroker(url=redis_url)
    dramatiq.set_broker(broker)
    return broker
