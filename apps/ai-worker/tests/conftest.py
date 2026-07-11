import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for name in list(sys.modules):
    if name == "worker" or name.startswith("worker."):
        sys.modules.pop(name)
sys.path.insert(0, str(ROOT))
