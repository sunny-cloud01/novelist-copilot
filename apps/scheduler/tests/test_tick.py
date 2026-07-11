from datetime import datetime, timezone

from scheduler.main import run_scheduler_tick


def test_scheduler_tick_returns_expected_counters() -> None:
    result = run_scheduler_tick(datetime(2026, 7, 11, tzinfo=timezone.utc))
    assert result.requeued == 0
    assert result.expired_leases == 0
    assert result.due_retries == 0
    assert result.ran_at == "2026-07-11T00:00:00+00:00"
