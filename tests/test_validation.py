from __future__ import annotations

import shutil
from pathlib import Path

from personalos.workspace import validate_workspace

ROOT = Path(__file__).resolve().parents[1]


def test_sample_workspace_is_valid() -> None:
    result = validate_workspace(ROOT)

    assert result.is_valid
    assert len(result.records) == 11
    assert result.counts == {"project": 3, "task": 5, "decision": 3}


def test_missing_required_field_fails(tmp_path: Path) -> None:
    workspace = clone_workspace(tmp_path)
    shutil.copy2(
        ROOT / "tests" / "fixtures" / "invalid" / "task-missing-title.md",
        workspace / "entities" / "tasks" / "task-missing-title.md",
    )

    result = validate_workspace(workspace)

    assert not result.is_valid
    assert any("'title' is a required property" in issue.message for issue in result.issues)


def test_broken_relationship_fails(tmp_path: Path) -> None:
    workspace = clone_workspace(tmp_path)
    shutil.copy2(
        ROOT / "tests" / "fixtures" / "invalid" / "task-bad-project.md",
        workspace / "entities" / "tasks" / "task-bad-project.md",
    )

    result = validate_workspace(workspace)

    assert not result.is_valid
    assert any("unknown project 'prj_missing_project'" in issue.message for issue in result.issues)


def test_private_content_fails(tmp_path: Path) -> None:
    workspace = clone_workspace(tmp_path)
    shutil.copy2(
        ROOT / "tests" / "fixtures" / "invalid" / "task-private-email.md",
        workspace / "entities" / "tasks" / "task-private-email.md",
    )

    result = validate_workspace(workspace)

    assert not result.is_valid
    assert any("contains a email address" in issue.message for issue in result.issues)


def clone_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "workspace"
    shutil.copytree(ROOT / "schema", workspace / "schema")
    shutil.copytree(ROOT / "entities", workspace / "entities")
    return workspace
