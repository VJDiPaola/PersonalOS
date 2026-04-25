"""Test that all sample entities pass schema validation."""

from pathlib import Path

from cli.personalos.config import find_root
from cli.personalos.validator import validate_entities


ROOT = find_root()


def test_all_entities_are_valid():
    """Every sample entity should pass its JSON schema."""
    errors = validate_entities(ROOT)
    if errors:
        msg_lines = ["Schema validation failed:"]
        for err in errors:
            msg_lines.append(f"  {err['file']} [{err['field']}]: {err['message']}")
        raise AssertionError("\n".join(msg_lines))


def test_schema_files_exist():
    """Every entity type should have a schema file."""
    from cli.personalos.config import ENTITY_TYPES

    schema_dir = ROOT / "schema"
    for entity_type in ENTITY_TYPES:
        schema_file = schema_dir / f"{entity_type}.schema.json"
        assert schema_file.exists(), f"Missing schema: {schema_file}"


def test_base_schema_exists():
    """The shared base schema should exist."""
    assert (ROOT / "schema" / "_base.schema.json").exists()
