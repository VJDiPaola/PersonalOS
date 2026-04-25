"""Load PersonalOS configuration from personalos.toml."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]

DEFAULTS: dict[str, Any] = {
    "directories": {
        "entities": "entities",
        "views": "views",
        "exports": "exports",
        "schema": "schema",
    },
    "id_prefixes": {
        "project": "prj_",
        "task": "tsk_",
        "tool": "tool_",
        "contact": "contact_",
        "application": "app_",
        "decision": "dec_",
        "review": "rev_",
    },
    "review": {
        "default_author": "",
    },
}

ENTITY_TYPES = list(DEFAULTS["id_prefixes"].keys())

ENTITY_SUBDIRS = {
    "project": "projects",
    "task": "tasks",
    "tool": "tools",
    "contact": "contacts",
    "application": "applications",
    "decision": "decisions",
    "review": "reviews",
}


def find_root() -> Path:
    """Walk up from cwd to find the repo root (contains personalos.toml or schema/)."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / "personalos.toml").exists() or (parent / "schema").is_dir():
            return parent
    return current


def load_config(root: Path | None = None) -> dict[str, Any]:
    """Load config from personalos.toml, falling back to defaults."""
    if root is None:
        root = find_root()
    config_path = root / "personalos.toml"
    if config_path.exists():
        with open(config_path, "rb") as f:
            user_config = tomllib.load(f)
        # Merge with defaults
        merged: dict[str, Any] = {}
        for section, defaults in DEFAULTS.items():
            merged[section] = {**defaults, **user_config.get(section, {})}
        return merged
    return {k: dict(v) for k, v in DEFAULTS.items()}
