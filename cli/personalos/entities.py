"""Load and parse PersonalOS entities from markdown files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import datetime

import frontmatter

from .config import ENTITY_SUBDIRS, ENTITY_TYPES, load_config


def entities_dir(root: Path, config: dict[str, Any] | None = None) -> Path:
    """Return the entities directory."""
    if config is None:
        config = load_config(root)
    return root / config["directories"]["entities"]


def schema_dir(root: Path, config: dict[str, Any] | None = None) -> Path:
    """Return the schema directory."""
    if config is None:
        config = load_config(root)
    return root / config["directories"]["schema"]


def views_dir(root: Path, config: dict[str, Any] | None = None) -> Path:
    """Return the views directory."""
    if config is None:
        config = load_config(root)
    return root / config["directories"]["views"]


def exports_dir(root: Path, config: dict[str, Any] | None = None) -> Path:
    """Return the exports directory."""
    if config is None:
        config = load_config(root)
    return root / config["directories"]["exports"]


def load_entity(path: Path) -> dict[str, Any]:
    """Load a single entity from a markdown file.

    Returns the frontmatter metadata merged with a '_body' key for content
    and a '_path' key for the source file.
    """
    post = frontmatter.load(str(path))
    data = dict(post.metadata)
    # Coerce datetime.date/datetime objects to ISO strings for schema validation
    for key, value in data.items():
        if isinstance(value, (datetime.date, datetime.datetime)):
            data[key] = value.isoformat()
    data["_body"] = post.content
    data["_path"] = str(path)
    return data


def load_all_entities(root: Path, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Load all entities from the entities directory."""
    ent_dir = entities_dir(root, config)
    all_entities: list[dict[str, Any]] = []
    if not ent_dir.exists():
        return all_entities
    for entity_type in ENTITY_TYPES:
        subdir = ent_dir / ENTITY_SUBDIRS[entity_type]
        if not subdir.exists():
            continue
        for md_file in sorted(subdir.glob("*.md")):
            entity = load_entity(md_file)
            all_entities.append(entity)
    return all_entities


def entities_by_type(entities: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group entities by their type field."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for entity in entities:
        entity_type = entity.get("type", "unknown")
        grouped.setdefault(entity_type, []).append(entity)
    return grouped


def entity_index(entities: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Build a lookup dict from entity ID to entity data."""
    return {e["id"]: e for e in entities if "id" in e}
