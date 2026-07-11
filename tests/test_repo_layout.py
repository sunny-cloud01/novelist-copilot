from pathlib import Path
import json


def test_root_workspace_files_exist_and_expose_required_scripts() -> None:
    package = json.loads(Path("package.json").read_text())
    assert package["private"] is True
    assert package["scripts"]["contracts:lint"] == "pnpm --filter @novel-factory/contracts lint"
    assert package["scripts"]["contracts:test"] == "pnpm --filter @novel-factory/contracts test"
    assert package["scripts"]["lint"] == "pnpm contracts:lint && pnpm --filter @novel-factory/web lint && pytest tests/test_repo_layout.py tests/test_infra_compose.py tests/test_contract_baseline.py -q"
    assert package["scripts"]["test"] == "pytest -q && pnpm contracts:test && pnpm --filter @novel-factory/web test --run"


def test_workspace_membership_and_bootstrap_docs_are_present() -> None:
    workspace = Path("pnpm-workspace.yaml").read_text()
    assert "apps/web" in workspace
    assert "packages/*" in workspace

    tsconfig = json.loads(Path("tsconfig.base.json").read_text())
    assert tsconfig["compilerOptions"]["strict"] is True
    assert tsconfig["compilerOptions"]["module"] == "ESNext"

    readme = Path("README.md").read_text()
    assert "## Implementation Bootstrap" in readme
    assert "pnpm contracts:lint" in readme
    assert "docker compose -f infra/docker-compose.yml up -d" in readme
