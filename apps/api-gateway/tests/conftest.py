import os
import sys
from pathlib import Path

import pytest

os.environ.setdefault("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")

ROOT = Path(__file__).resolve().parents[1]
for name in list(sys.modules):
    if name == "app" or name.startswith("app."):
        sys.modules.pop(name)
sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def seed_gateway_store():
    try:
        from app.core import phase_two_adapter
    except Exception:
        return
    phase_two_adapter._STORE.reset_store()
    phase_two_adapter._STORE.seed_phase_two_demo_data()
