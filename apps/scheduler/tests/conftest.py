import os
import sys
from pathlib import Path

os.environ.setdefault("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")

ROOT = Path(__file__).resolve().parents[1]
for name in list(sys.modules):
    if name == "scheduler" or name.startswith("scheduler."):
        sys.modules.pop(name)
sys.path.insert(0, str(ROOT))
