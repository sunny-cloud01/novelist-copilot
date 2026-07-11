from pathlib import Path
import json


def test_root_workspace_files_exist_and_expose_required_scripts() -> None:
    package = json.loads(Path("package.json").read_text())
    assert package["private"] is True
    assert package["scripts"]["contracts:lint"] == "pnpm --filter @novel-factory/contracts lint"
    assert package["scripts"]["contracts:test"] == "pnpm --filter @novel-factory/contracts test"
    assert package["scripts"]["lint"] == "python3 scripts/build_docs.py --check && docker compose -f infra/docker-compose.yml config >/tmp/novel-factory.compose.out && python3 -m pytest tests/test_build_docs.py tests/test_repo_layout.py tests/test_infra_compose.py tests/test_contract_baseline.py -q && pnpm contracts:lint"
    assert package["scripts"]["test"] == "docker compose -f infra/docker-compose.yml config >/tmp/novel-factory.compose.out && python3 -m pytest tests/test_build_docs.py tests/test_repo_layout.py tests/test_infra_compose.py tests/test_contract_baseline.py -q && pnpm contracts:test"
    assert package["scripts"]["smoke"] == "bash scripts/dev/smoke.sh"


def test_workspace_membership_and_bootstrap_docs_are_present() -> None:
    workspace = Path("pnpm-workspace.yaml").read_text()
    assert "apps/web" in workspace
    assert "packages/*" in workspace

    tsconfig = json.loads(Path("tsconfig.base.json").read_text())
    assert tsconfig["compilerOptions"]["strict"] is True
    assert tsconfig["compilerOptions"]["module"] == "ESNext"

    readme = Path("README.md").read_text()
    assert "## Implementation Bootstrap" in readme
    assert "python3 scripts/build_docs.py --check" in readme
    assert "Later scaffold tasks add pnpm workspace apps and infra commands after those paths exist." in readme


def test_smoke_script_runs_contracts_pytest_and_web_checks() -> None:
    script = Path("scripts/dev/smoke.sh").read_text()
    assert "pnpm contracts:lint" in script
    assert "pnpm contracts:test" in script
    assert "python3 -m pytest -q" in script
    assert "pnpm --filter @novel-factory/web test --run" in script
