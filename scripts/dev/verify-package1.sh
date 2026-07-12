#!/usr/bin/env bash
set -euo pipefail

docker compose -f infra/docker-compose.yml config >/tmp/novel-factory.compose.out
rtk python3 -m pytest apps/core-service/tests/test_health.py apps/core-service/tests/test_persistence.py apps/api-gateway/tests/test_health.py tests/test_infra_compose.py apps/scheduler/tests/test_tick.py apps/core-service/tests/test_phase_three_api.py apps/api-gateway/tests/test_phase_three_api.py -q
