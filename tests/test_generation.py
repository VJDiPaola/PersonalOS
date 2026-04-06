from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from personalos.workspace import load_workspace, render_context_json, render_context_markdown, render_dashboard

ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_matches_checked_in_examples() -> None:
    workspace = load_workspace(ROOT)
    generated = render_dashboard(workspace)

    assert generated == (ROOT / "views" / "dashboard.example.md").read_text(encoding="utf-8")
    assert generated == (ROOT / "tests" / "golden" / "dashboard.example.md").read_text(encoding="utf-8")


def test_context_exports_match_checked_in_examples() -> None:
    workspace = load_workspace(ROOT)
    markdown = render_context_markdown(workspace)
    json_text = render_context_json(workspace)

    assert markdown == (ROOT / "exports" / "context" / "workspace-context.md").read_text(encoding="utf-8")
    assert json_text == (ROOT / "exports" / "json" / "workspace-context.json").read_text(encoding="utf-8")
    assert markdown == (ROOT / "tests" / "golden" / "workspace-context.md").read_text(encoding="utf-8")
    assert json_text == (ROOT / "tests" / "golden" / "workspace-context.json").read_text(encoding="utf-8")


def test_cli_validate_and_generate_all(tmp_path: Path) -> None:
    workspace = clone_full_workspace(tmp_path)
    env = os.environ.copy()
    pythonpath = str(ROOT / "cli")
    env["PYTHONPATH"] = pythonpath if not env.get("PYTHONPATH") else pythonpath + os.pathsep + env["PYTHONPATH"]

    validate = subprocess.run(
        [sys.executable, "-m", "personalos", "--root", str(workspace), "validate"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr

    generate = subprocess.run(
        [sys.executable, "-m", "personalos", "--root", str(workspace), "generate", "all"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
    )
    assert generate.returncode == 0, generate.stdout + generate.stderr
    assert (workspace / "views" / "dashboard.example.md").exists()
    assert (workspace / "exports" / "context" / "workspace-context.md").exists()
    assert (workspace / "exports" / "json" / "workspace-context.json").exists()


def clone_full_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "workspace"
    shutil.copytree(ROOT / "schema", workspace / "schema")
    shutil.copytree(ROOT / "entities", workspace / "entities")
    (workspace / "views").mkdir(parents=True, exist_ok=True)
    (workspace / "exports" / "context").mkdir(parents=True, exist_ok=True)
    (workspace / "exports" / "json").mkdir(parents=True, exist_ok=True)
    return workspace
