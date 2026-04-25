"""Smoke tests for the PersonalOS CLI."""

import os
import shutil
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from cli.personalos.main import app

runner = CliRunner()

ROOT = Path(__file__).resolve().parent.parent


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "personalos" in result.output


def test_validate_passes():
    result = runner.invoke(app, ["validate"])
    assert result.exit_code == 0
    assert "valid" in result.output.lower()


def test_check_passes():
    result = runner.invoke(app, ["check"])
    assert result.exit_code == 0


def test_doctor_passes():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Everything looks good" in result.output


def test_generate_all():
    result = runner.invoke(app, ["generate", "all"])
    assert result.exit_code == 0
    assert "Generated" in result.output


def test_generate_dashboard():
    result = runner.invoke(app, ["generate", "dashboard"])
    assert result.exit_code == 0
    assert (ROOT / "views" / "dashboard.md").exists()


def test_generate_graph():
    result = runner.invoke(app, ["generate", "graph"])
    assert result.exit_code == 0
    assert (ROOT / "views" / "graph.mmd").exists()


def test_generate_contexts():
    result = runner.invoke(app, ["generate", "contexts"])
    assert result.exit_code == 0


def test_new_entity_in_temp_dir():
    """Test creating a new entity in a temporary workspace."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        # Copy schema and config
        shutil.copytree(ROOT / "schema", tmp / "schema")
        shutil.copy(ROOT / "personalos.toml", tmp / "personalos.toml")
        (tmp / "entities" / "projects").mkdir(parents=True)

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp)
            result = runner.invoke(app, ["new", "project", "Test Project"])
            assert result.exit_code == 0
            assert "Created" in result.output
            created_file = tmp / "entities" / "projects" / "test-project.md"
            assert created_file.exists()
            content = created_file.read_text(encoding="utf-8")
            assert "title: Test Project" in content
            assert "type: project" in content
        finally:
            os.chdir(old_cwd)


def test_archive_dry_run():
    result = runner.invoke(app, ["archive"])
    assert result.exit_code == 0


def test_diff():
    result = runner.invoke(app, ["diff"])
    assert result.exit_code == 0
