from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_phase_two_store() -> ModuleType:
    module_path = Path(__file__).resolve().parents[2] / "core-service" / "app" / "core" / "phase_two_store.py"
    spec = importlib.util.spec_from_file_location(f"phase_two_store_scheduler_{id(module_path)}", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load phase two store")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
