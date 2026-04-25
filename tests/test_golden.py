"""Golden file tests for generators.

Compares generated output against committed golden files.
To update goldens, run: pytest tests/test_golden.py --update-goldens
"""

from pathlib import Path

import pytest

from cli.personalos.config import find_root
from cli.personalos.generators import generate_dashboard, generate_graph


ROOT = find_root()
GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


@pytest.fixture
def update_goldens(request):
    return request.config.getoption("--update-goldens")


def _compare_or_update(golden_path: Path, actual: str, update: bool):
    if update:
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8")
        return

    if not golden_path.exists():
        pytest.fail(
            f"Golden file not found: {golden_path}\n"
            f"Run with --update-goldens to create it."
        )

    expected = golden_path.read_text(encoding="utf-8")
    if actual != expected:
        # Find first difference for a useful error message
        actual_lines = actual.splitlines()
        expected_lines = expected.splitlines()
        for i, (a, e) in enumerate(zip(actual_lines, expected_lines)):
            if a != e:
                pytest.fail(
                    f"Golden mismatch at line {i + 1}:\n"
                    f"  expected: {e!r}\n"
                    f"  actual:   {a!r}\n\n"
                    f"Run with --update-goldens to update."
                )
        if len(actual_lines) != len(expected_lines):
            pytest.fail(
                f"Golden file has {len(expected_lines)} lines, "
                f"but generated output has {len(actual_lines)} lines.\n"
                f"Run with --update-goldens to update."
            )


def test_dashboard_golden(update_goldens):
    actual = generate_dashboard(ROOT)
    _compare_or_update(GOLDEN_DIR / "dashboard.md", actual, update_goldens)


def test_graph_golden(update_goldens):
    actual = generate_graph(ROOT)
    _compare_or_update(GOLDEN_DIR / "graph.mmd", actual, update_goldens)
