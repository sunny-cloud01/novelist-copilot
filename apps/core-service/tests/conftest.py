import os
import sys
from pathlib import Path
from uuid import uuid4

import pytest

os.environ.setdefault("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")

ROOT = Path(__file__).resolve().parents[1]
for name in list(sys.modules):
    if name == "app" or name.startswith("app."):
        sys.modules.pop(name)
sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def _isolated_persistence(monkeypatch):
    """Give every test its own persistence namespace.

    The store persists to Postgres (shared ``novel_factory`` DB) or, when
    Postgres is unavailable, to a ``/tmp`` snapshot whose path is derived from
    ``NOVEL_FACTORY_POSTGRES_URL``. Without isolation, mutating tests in one
    file leak state into the shared backend and later tests/files hydrate the
    dirty state, breaking assertions that expect a clean seed.

    This fixture points each test at a unique, unreachable Postgres URL so the
    store deterministically uses a per-test file snapshot that no other test
    shares, then removes those snapshot files afterwards. Tests that need real
    Postgres override ``NOVEL_FACTORY_POSTGRES_URL`` in their own body, which
    takes precedence over this fixture.
    """

    database = f"novel_factory_test_{uuid4().hex}"
    monkeypatch.setenv("NOVEL_FACTORY_ALLOW_FILE_PERSISTENCE_FALLBACK", "1")
    monkeypatch.setenv(
        "NOVEL_FACTORY_POSTGRES_URL",
        f"postgresql://novel:novel@localhost:5999/{database}",
    )
    try:
        yield
    finally:
        for path in Path("/tmp").glob(f"{database}-localhost-5999-*.snapshot.json"):
            try:
                path.unlink()
            except FileNotFoundError:
                pass
