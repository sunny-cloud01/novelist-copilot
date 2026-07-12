from pathlib import Path
import json


def test_root_workspace_files_exist_and_expose_required_scripts() -> None:
    package = json.loads(Path("package.json").read_text())
    assert package["private"] is True
    assert package["scripts"]["contracts:lint"] == "pnpm --filter @novel-factory/contracts lint"
    assert package["scripts"]["contracts:test"] == "pnpm --filter @novel-factory/contracts test"
    assert package["scripts"]["packages:lint"] == "pnpm --filter @novel-factory/shared-types lint && pnpm --filter @novel-factory/prompt-schemas lint && pnpm --filter @novel-factory/config lint && pnpm --filter @novel-factory/ui lint"
    assert package["scripts"]["lint"] == "python3 scripts/build_docs.py --check && docker compose -f infra/docker-compose.yml config >/tmp/novel-factory.compose.out && python3 -m pytest tests/test_build_docs.py tests/test_repo_layout.py tests/test_infra_compose.py tests/test_contract_baseline.py -q && pnpm contracts:lint && pnpm packages:lint && pnpm --filter @novel-factory/web lint"
    assert package["scripts"]["test"] == "python3 -m pytest -q && pnpm contracts:test && pnpm --filter @novel-factory/web test --run"
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


def test_workspace_package_skeletons_exist() -> None:
    assert Path("packages/shared-types/package.json").exists()
    assert Path("packages/shared-types/src/api.ts").exists()
    assert Path("packages/shared-types/src/schemas.ts").exists()
    assert Path("packages/prompt-schemas/package.json").exists()
    assert Path("packages/prompt-schemas/src/index.ts").exists()
    assert Path("packages/config/package.json").exists()
    assert Path("packages/config/src/index.ts").exists()
    assert Path("packages/ui/package.json").exists()
    assert Path("packages/ui/src/index.ts").exists()


def test_smoke_script_runs_root_lint_and_test_checks() -> None:
    script = Path("scripts/dev/smoke.sh").read_text()
    assert "pnpm lint" in script
    assert "apps/core-service/tests/test_phase_two_api.py" in script
    assert "apps/api-gateway/tests/test_phase_four_api.py" in script
    assert "src/test/phase-two-flow.test.tsx" in script
    assert "src/test/configuration-flow.test.tsx" in script
    assert "pnpm test" in script


def test_package1_dev_scripts_exist() -> None:
    bootstrap = Path("scripts/dev/bootstrap-package1.sh").read_text()
    assert "docker compose -f infra/docker-compose.yml up -d --build" in bootstrap
    assert "core-service" in bootstrap
    assert "scheduler" in bootstrap

    reset_script = Path("scripts/dev/reset-package1-state.py").read_text()
    assert "store.reset_store()" in reset_script
    assert "store.seed_phase_two_demo_data()" in reset_script

    verify = Path("scripts/dev/verify-package1.sh").read_text()
    assert "docker compose -f infra/docker-compose.yml config" in verify
    assert "apps/core-service/tests/test_persistence.py" in verify


def test_ci_workflow_exists_and_runs_minimum_gate() -> None:
    workflow = Path(".github/workflows/ci.yml").read_text()
    assert "pnpm lint" in workflow
    assert "pnpm contracts:lint" in workflow
    assert "pnpm contracts:test" in workflow
    assert "pnpm test" in workflow
    assert "pnpm smoke" in workflow
