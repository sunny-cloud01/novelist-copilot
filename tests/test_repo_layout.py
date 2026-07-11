from pathlib import Path
import json


def test_root_workspace_files_exist_and_expose_required_scripts() -> None:
    package = json.loads(Path("package.json").read_text())
    assert package["private"] is True
    assert package["scripts"]["contracts:lint"] == "python3 scripts/build_docs.py --check"
    assert package["scripts"]["contracts:test"] == "python3 -m pytest tests/test_build_docs.py tests/test_repo_layout.py -q"
    assert package["scripts"]["lint"] == "python3 scripts/build_docs.py --check && python3 -m pytest tests/test_build_docs.py tests/test_repo_layout.py -q"
    assert package["scripts"]["test"] == "python3 -m pytest tests/test_build_docs.py tests/test_repo_layout.py -q"


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
