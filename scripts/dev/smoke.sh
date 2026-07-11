#!/usr/bin/env bash
set -euo pipefail

pnpm contracts:lint
pnpm contracts:test
python3 -m pytest -q
pnpm --filter @novel-factory/web test --run
