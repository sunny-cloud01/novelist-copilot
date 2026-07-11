from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class SchedulerTickResult:
    requeued: int
    expired_leases: int
    due_retries: int
    ran_at: str


def run_scheduler_tick(now: Optional[datetime] = None) -> SchedulerTickResult:
    current = now or datetime.now(timezone.utc)
    return SchedulerTickResult(
        requeued=0,
        expired_leases=0,
        due_retries=0,
        ran_at=current.isoformat(),
    )


if __name__ == "__main__":
    print(run_scheduler_tick())
