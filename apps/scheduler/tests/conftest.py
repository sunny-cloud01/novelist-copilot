import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for name in list(sys.modules):
    if name == "scheduler" or name.startswith("scheduler."):
        sys.modules.pop(name)
sys.path.insert(0, str(ROOT))
