from __future__ import annotations

import importlib
import sys
from pathlib import Path
from uuid import uuid4


def _purge_app_modules() -> None:
    for name in list(sys.modules):
        if name == "app" or name.startswith("app.") or name == "phase_two_persistence":
            sys.modules.pop(name)


def _snapshot_file(database: str) -> Path:
    return Path("/tmp") / f"{database}-localhost-5999-core-store.snapshot.json"


def _load_store_module():
    _purge_app_modules()
    return importlib.import_module("app.core.phase_two_store")


def test_phase_two_store_restores_persisted_workspace_and_project(monkeypatch) -> None:
    database = f"package1_persistence_{uuid4().hex}"
    snapshot_file = _snapshot_file(database)
    if snapshot_file.exists():
        snapshot_file.unlink()

    monkeypatch.setenv("NOVEL_FACTORY_POSTGRES_URL", f"postgresql://novel:novel@localhost:5999/{database}")

    store = _load_store_module()
    created = store.create_workspace({"name": "持久化工作区", "slug": "persist-workspace"})
    workspace_id = created["workspace"]["workspace_id"]
    project_bundle = store.create_novel_project(
        {
            "workspace_id": workspace_id,
            "title": "持久化项目",
            "genre_scope": ["xianxia"],
        },
        trace_id="trace-persist-project",
        actor_id=store.USER_ID,
        actor_role="owner",
        workspace_id=workspace_id,
    )
    project_id = project_bundle["project"]["project_id"]

    reloaded = _load_store_module()
    workspace = reloaded.get_workspace(workspace_id)
    project = reloaded.get_novel_project(project_id)

    assert workspace is not None
    assert workspace["workspace"]["name"] == "持久化工作区"
    assert project is not None
    assert project["project"]["title"] == "持久化项目"
    assert project["project"]["workspace_id"] == workspace_id

    if snapshot_file.exists():
        snapshot_file.unlink()
