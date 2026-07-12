from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/core-service"))

import app.core.phase_two_store as store


store.reset_store()
store.seed_phase_two_demo_data()
store._normalize_seed_records()
store._persist_store()

print("package1 state reset")
