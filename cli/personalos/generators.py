"""PersonalOS generators — dashboard, AI context, JSON export, graph."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import load_config
from .entities import (
    entities_by_type,
    entity_index,
    exports_dir,
    load_all_entities,
)


# ---------------------------------------------------------------------------
# Dashboard generator
# ---------------------------------------------------------------------------

def generate_dashboard(root: Path) -> str:
    """Generate a markdown dashboard from all entities."""
    entities = load_all_entities(root)
    by_type = entities_by_type(entities)
    index = entity_index(entities)
    lines: list[str] = ["# PersonalOS Dashboard", ""]

    # Projects
    projects = by_type.get("project", [])
    if projects:
        lines.append("## Projects")
        lines.append("")
        for status in ["active", "building", "idea", "deploy_ready", "shipped", "reviewed"]:
            group = [p for p in projects if p.get("status") == status]
            if group:
                lines.append(f"### {status.replace('_', ' ').title()}")
                lines.append("")
                for p in group:
                    priority = p.get("priority", "")
                    lines.append(f"- **{p['title']}** ({priority})")
                    # Show linked tasks
                    tasks = by_type.get("task", [])
                    linked = [t for t in tasks if t.get("project_id") == p.get("id")]
                    for t in linked:
                        lines.append(f"  - [{t.get('status', '?')}] {t['title']}")
                lines.append("")

    # Standalone tasks (no project_id)
    tasks = by_type.get("task", [])
    standalone = [t for t in tasks if not t.get("project_id")]
    if standalone:
        lines.append("## Standalone Tasks")
        lines.append("")
        for t in standalone:
            lines.append(f"- [{t.get('status', '?')}] **{t['title']}** ({t.get('priority', '')})")
        lines.append("")

    # Decisions
    decisions = by_type.get("decision", [])
    if decisions:
        lines.append("## Decisions")
        lines.append("")
        for d in decisions:
            status = d.get("status", "?")
            lines.append(f"- [{status}] **{d['title']}**")
            if d.get("question"):
                lines.append(f"  > {d['question']}")
            if d.get("outcome"):
                lines.append(f"  Outcome: {d['outcome']}")
        lines.append("")

    # Tools
    tools = by_type.get("tool", [])
    if tools:
        lines.append("## Tools")
        lines.append("")
        for t in tools:
            status = t.get("status", "?")
            cat = f" ({t['category']})" if t.get("category") else ""
            lines.append(f"- **{t['title']}**{cat} — {status}")
        lines.append("")

    # Contacts
    contacts = by_type.get("contact", [])
    if contacts:
        lines.append("## Contacts")
        lines.append("")
        for c in contacts:
            role = f" — {c['role']}" if c.get("role") else ""
            org = f" @ {c['organization']}" if c.get("organization") else ""
            lines.append(f"- **{c['title']}**{role}{org}")
        lines.append("")

    # Applications
    applications = by_type.get("application", [])
    if applications:
        lines.append("## Applications")
        lines.append("")
        for a in applications:
            status = a.get("status", "?")
            lines.append(f"- [{status}] **{a['title']}** — {a.get('company', '?')} ({a.get('role_title', '?')})")
        lines.append("")

    # Reviews
    reviews = by_type.get("review", [])
    if reviews:
        lines.append("## Recent Reviews")
        lines.append("")
        for r in sorted(reviews, key=lambda x: x.get("period", ""), reverse=True)[:3]:
            lines.append(f"- **{r['title']}** ({r.get('status', '?')})")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# AI context exporter
# ---------------------------------------------------------------------------

def generate_ai_contexts(root: Path) -> None:
    """Generate AI context exports (full + per-project)."""
    config = load_config(root)
    entities = load_all_entities(root, config)
    by_type = entities_by_type(entities)
    index = entity_index(entities)

    exp_dir = exports_dir(root, config)
    ctx_dir = exp_dir / "context"
    ctx_dir.mkdir(parents=True, exist_ok=True)
    per_project_dir = ctx_dir / "per-project"
    per_project_dir.mkdir(parents=True, exist_ok=True)

    # Full context
    full_context = {
        "entity_count": len(entities),
        "entities": {
            etype: [_clean(e) for e in elist]
            for etype, elist in by_type.items()
        },
    }
    (ctx_dir / "full-context.json").write_text(
        json.dumps(full_context, indent=2, default=str), encoding="utf-8"
    )

    # Per-project context
    projects = by_type.get("project", [])
    tasks = by_type.get("task", [])
    for project in projects:
        pid = project.get("id", "")
        slug = project.get("slug", pid)
        linked_tasks = [t for t in tasks if t.get("project_id") == pid]
        linked_tool_ids = project.get("tool_ids", [])
        linked_tools = [index[tid] for tid in linked_tool_ids if tid in index]

        project_context = {
            "project": _clean(project),
            "tasks": [_clean(t) for t in linked_tasks],
            "tools": [_clean(t) for t in linked_tools],
        }
        (per_project_dir / f"{slug}.json").write_text(
            json.dumps(project_context, indent=2, default=str), encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# JSON entity exporter
# ---------------------------------------------------------------------------

def generate_json_export(root: Path) -> None:
    """Generate one JSON file per entity."""
    config = load_config(root)
    entities = load_all_entities(root, config)
    json_dir = exports_dir(root, config) / "json"
    json_dir.mkdir(parents=True, exist_ok=True)

    for entity in entities:
        slug = entity.get("slug", entity.get("id", "unknown"))
        etype = entity.get("type", "unknown")
        data = _clean(entity)
        filename = f"{etype}-{slug}.json"
        (json_dir / filename).write_text(
            json.dumps(data, indent=2, default=str), encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# Relationship graph generator (Mermaid)
# ---------------------------------------------------------------------------

def generate_graph(root: Path) -> str:
    """Generate a Mermaid flowchart of entity relationships."""
    entities = load_all_entities(root)
    index = entity_index(entities)

    lines: list[str] = ["graph LR"]

    # Define nodes
    for entity in entities:
        eid = entity.get("id", "")
        title = entity.get("title", "?")
        etype = entity.get("type", "?")
        node_id = _mermaid_id(eid)
        shape = _mermaid_shape(etype)
        lines.append(f"    {node_id}{shape[0]}\"{etype}: {title}\"{shape[1]}")

    lines.append("")

    # Define edges
    ref_fields = {
        "project_id": "belongs to",
        "tool_ids": "uses",
        "contact_ids": "involves",
        "related_entity_ids": "related to",
    }
    for entity in entities:
        src = _mermaid_id(entity.get("id", ""))
        for field, label in ref_fields.items():
            value = entity.get(field)
            if value is None:
                continue
            refs = [value] if isinstance(value, str) else value
            for ref_id in refs:
                if ref_id in index:
                    dst = _mermaid_id(ref_id)
                    lines.append(f"    {src} -->|{label}| {dst}")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean(entity: dict[str, Any]) -> dict[str, Any]:
    """Remove internal keys (prefixed with _) from an entity dict."""
    return {k: v for k, v in entity.items() if not k.startswith("_")}


def _mermaid_id(entity_id: str) -> str:
    """Convert an entity ID to a valid Mermaid node ID."""
    return entity_id.replace("_", "x")


def _mermaid_shape(entity_type: str) -> tuple[str, str]:
    """Return Mermaid shape delimiters based on entity type."""
    shapes: dict[str, tuple[str, str]] = {
        "project": ("[", "]"),
        "task": ("(", ")"),
        "tool": ("{{", "}}"),
        "contact": ("([", "])"),
        "decision": ("{", "}"),
        "review": ("[[", "]]"),
        "application": ("(", ")"),
    }
    return shapes.get(entity_type, ("[", "]"))
