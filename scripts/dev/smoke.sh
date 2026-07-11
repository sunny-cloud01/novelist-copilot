#!/usr/bin/env bash
set -euo pipefail

pnpm lint
rtk python3 -m pytest apps/core-service/tests/test_phase_two_api.py apps/core-service/tests/test_phase_three_api.py apps/core-service/tests/test_phase_four_api.py apps/api-gateway/tests/test_phase_two_api.py apps/api-gateway/tests/test_phase_three_api.py apps/api-gateway/tests/test_phase_four_api.py -q
pnpm --filter @novel-factory/web exec vitest run src/test/phase-two-flow.test.tsx src/test/project-planning-flow.test.tsx src/test/writing-studio-flow.test.tsx src/test/feedback-flow.test.tsx src/test/configuration-flow.test.tsx
pnpm test
