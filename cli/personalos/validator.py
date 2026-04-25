"""Validate PersonalOS entities against JSON schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver, ValidationError

from .config import ENTITY_TYPES
from .entities import load_all_entities, schema_dir


def _build_resolver(schema_path: Path) -> tuple[dict[str, Any], RefResolver]:
    """Build a JSON Schema resolver with all schema files loaded."""
    store: dict[str, Any] = {}
    for schema_file in schema_path.glob("*.schema.json"):
        with open(schema_file, "r", encoding="utf-8") as f:
            schema = json.load(f)
        schema_id = schema.get("$id", schema_file.name)
        store[schema_id] = schema
        # Also store by filename for relative $ref resolution
        store[schema_file.name] = schema
    return store, RefResolver(
        base_uri=f"file:///{schema_path.as_posix()}/",
        referrer={},
        store=store,
    )


def _get_schema_for_type(
    entity_type: str, schema_path: Path, store: dict[str, Any]
) -> dict[str, Any] | None:
    """Get the JSON schema for a given entity type."""
    filename = f"{entity_type}.schema.json"
    if filename in store:
        return store[filename]
    filepath = schema_path / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def validate_entities(
    root: Path,
) -> list[dict[str, str]]:
    """Validate all entities and return a list of error dicts.

    Each error dict has keys: 'file', 'field', 'message'.
    Returns an empty list if all entities are valid.
    """
    s_dir = schema_dir(root)
    if not s_dir.exists():
        return [{"file": "", "field": "", "message": f"Schema directory not found: {s_dir}"}]

    store, resolver = _build_resolver(s_dir)
    entities = load_all_entities(root)
    errors: list[dict[str, str]] = []

    for entity in entities:
        entity_path = entity.get("_path", "unknown")
        entity_type = entity.get("type")

        if not entity_type:
            errors.append({
                "file": entity_path,
                "field": "type",
                "message": "Missing 'type' field in frontmatter.",
            })
            continue

        if entity_type not in ENTITY_TYPES:
            errors.append({
                "file": entity_path,
                "field": "type",
                "message": f"Unknown entity type: '{entity_type}'.",
            })
            continue

        schema = _get_schema_for_type(entity_type, s_dir, store)
        if schema is None:
            errors.append({
                "file": entity_path,
                "field": "",
                "message": f"No schema found for type '{entity_type}'.",
            })
            continue

        # Strip internal keys before validation
        data = {k: v for k, v in entity.items() if not k.startswith("_")}

        validator = Draft202012Validator(schema, resolver=resolver)
        for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            field = ".".join(str(p) for p in error.absolute_path) or "(root)"
            errors.append({
                "file": entity_path,
                "field": field,
                "message": error.message,
            })

    return errors


def check_structure(root: Path) -> list[dict[str, str]]:
    """Run structural checks beyond schema validation.

    Checks for:
    - Missing required directories
    - Orphan ID references (IDs referenced but not found)
    """
    from .config import ENTITY_SUBDIRS, load_config
    from .entities import entities_dir, entity_index

    config = load_config(root)
    errors: list[dict[str, str]] = []

    # Check required directories
    ent_dir = entities_dir(root, config)
    for subdir_name in ENTITY_SUBDIRS.values():
        subdir = ent_dir / subdir_name
        if not subdir.exists():
            errors.append({
                "file": str(subdir),
                "field": "",
                "message": f"Missing entity directory: {subdir_name}/",
            })

    # Check for orphan references
    entities = load_all_entities(root, config)
    index = entity_index(entities)
    id_ref_fields = ["project_id", "tool_ids", "contact_ids", "related_entity_ids"]

    for entity in entities:
        entity_path = entity.get("_path", "unknown")
        for field in id_ref_fields:
            value = entity.get(field)
            if value is None:
                continue
            refs = [value] if isinstance(value, str) else value
            for ref_id in refs:
                if ref_id not in index:
                    errors.append({
                        "file": entity_path,
                        "field": field,
                        "message": f"Referenced ID '{ref_id}' not found in any entity.",
                    })

    return errors
