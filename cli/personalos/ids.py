"""ULID-based ID generation for PersonalOS entities."""

from __future__ import annotations

from ulid import ULID

from .config import load_config


def generate_id(entity_type: str) -> str:
    """Generate a prefixed ULID for the given entity type.

    Example: generate_id("project") -> "prj_01JYV4R2D3J7M7X9Q0N2K8A6P1"
    """
    config = load_config()
    prefix = config["id_prefixes"].get(entity_type)
    if prefix is None:
        raise ValueError(f"Unknown entity type: {entity_type}")
    return f"{prefix}{ULID()}"


def slugify(title: str) -> str:
    """Convert a title to a URL-safe slug.

    Example: slugify("Portfolio Site Refresh") -> "portfolio-site-refresh"
    """
    slug = title.lower().strip()
    # Replace non-alphanumeric chars with hyphens
    result: list[str] = []
    for ch in slug:
        if ch.isalnum():
            result.append(ch)
        elif result and result[-1] != "-":
            result.append("-")
    return "-".join(part for part in "".join(result).split("-") if part)
