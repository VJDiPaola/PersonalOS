"""PersonalOS CLI — main entry point."""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path
from typing import Optional

import typer

from . import __version__
from .config import ENTITY_SUBDIRS, ENTITY_TYPES, find_root, load_config
from .entities import (
    entities_by_type,
    entities_dir,
    entity_index,
    exports_dir,
    load_all_entities,
    schema_dir,
    views_dir,
)
from .ids import generate_id, slugify
from .validator import check_structure, validate_entities

app = typer.Typer(
    name="personalos",
    help="A markdown-first personal operating system CLI.",
    no_args_is_help=True,
)
generate_app = typer.Typer(help="Generate views and exports.")
app.add_typer(generate_app, name="generate")


# ---------------------------------------------------------------------------
# personalos init
# ---------------------------------------------------------------------------
@app.command()
def init() -> None:
    """Scaffold the PersonalOS directory structure."""
    root = find_root()
    config = load_config(root)
    dirs_to_create = [
        entities_dir(root, config),
        *[entities_dir(root, config) / sub for sub in ENTITY_SUBDIRS.values()],
        views_dir(root, config),
        exports_dir(root, config),
        exports_dir(root, config) / "context",
        exports_dir(root, config) / "context" / "per-project",
        exports_dir(root, config) / "json",
    ]
    created = 0
    for d in dirs_to_create:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            gitkeep = d / ".gitkeep"
            if not any(d.iterdir()):
                gitkeep.touch()
            created += 1
    typer.echo(f"Initialized {created} directories.")


# ---------------------------------------------------------------------------
# personalos validate
# ---------------------------------------------------------------------------
@app.command()
def validate() -> None:
    """Validate all entities against their JSON schemas."""
    root = find_root()
    errors = validate_entities(root)
    if not errors:
        typer.echo("All entities are valid.")
        raise typer.Exit(0)
    for err in errors:
        path = err["file"]
        field = f" [{err['field']}]" if err["field"] else ""
        typer.echo(f"  ERROR {path}{field}: {err['message']}", err=True)
    typer.echo(f"\n{len(errors)} validation error(s) found.", err=True)
    raise typer.Exit(1)


# ---------------------------------------------------------------------------
# personalos check
# ---------------------------------------------------------------------------
@app.command()
def check() -> None:
    """Run validation and structural checks."""
    root = find_root()
    schema_errors = validate_entities(root)
    struct_errors = check_structure(root)
    all_errors = schema_errors + struct_errors
    if not all_errors:
        typer.echo("All checks passed.")
        raise typer.Exit(0)
    for err in all_errors:
        path = err["file"]
        field = f" [{err['field']}]" if err["field"] else ""
        typer.echo(f"  ERROR {path}{field}: {err['message']}", err=True)
    typer.echo(f"\n{len(all_errors)} error(s) found.", err=True)
    raise typer.Exit(1)


# ---------------------------------------------------------------------------
# personalos new <type> <title>
# ---------------------------------------------------------------------------
@app.command("new")
def new_entity(
    entity_type: str = typer.Argument(..., help="Entity type (project, task, tool, etc.)"),
    title: str = typer.Argument(..., help="Entity title."),
) -> None:
    """Create a new entity from a schema-driven template."""
    if entity_type not in ENTITY_TYPES:
        typer.echo(f"Unknown entity type: '{entity_type}'. Choose from: {', '.join(ENTITY_TYPES)}", err=True)
        raise typer.Exit(1)

    root = find_root()
    config = load_config(root)
    ent_id = generate_id(entity_type)
    slug = slugify(title)
    today = datetime.date.today().isoformat()

    # Build frontmatter from schema
    s_dir = schema_dir(root, config)
    schema_file = s_dir / f"{entity_type}.schema.json"
    extra_fields: dict[str, str] = {}
    if schema_file.exists():
        with open(schema_file, "r", encoding="utf-8") as f:
            schema = json.load(f)
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        base_fields = {"id", "type", "slug", "title", "status", "created_at", "updated_at", "tags"}
        for field_name, field_schema in props.items():
            if field_name in base_fields:
                continue
            if field_name in required:
                extra_fields[field_name] = _default_for_schema(field_schema)

    # Determine default status
    s_file = s_dir / f"{entity_type}.schema.json"
    default_status = "active"
    if s_file.exists():
        with open(s_file, "r", encoding="utf-8") as f:
            s = json.load(f)
        status_enum = s.get("properties", {}).get("status", {}).get("enum", [])
        if status_enum:
            default_status = status_enum[0]

    lines = [
        "---",
        f"id: {ent_id}",
        f"type: {entity_type}",
        f"slug: {slug}",
        f"title: {title}",
        f"status: {default_status}",
    ]
    for k, v in extra_fields.items():
        lines.append(f"{k}: {v}")
    lines += [
        f"created_at: {today}",
        f"updated_at: {today}",
        "tags: []",
        "---",
        "",
        f"# {title}",
        "",
        "Notes go here.",
        "",
    ]

    subdir = entities_dir(root, config) / ENTITY_SUBDIRS[entity_type]
    subdir.mkdir(parents=True, exist_ok=True)
    filepath = subdir / f"{slug}.md"
    filepath.write_text("\n".join(lines), encoding="utf-8")
    typer.echo(f"Created {filepath.relative_to(root)}")


def _default_for_schema(field_schema: dict) -> str:
    """Generate a placeholder default value for a schema field."""
    field_type = field_schema.get("type", "string")
    if field_type == "array":
        return "[]"
    if "enum" in field_schema:
        return field_schema["enum"][0]
    return '""'


# ---------------------------------------------------------------------------
# personalos generate dashboard
# ---------------------------------------------------------------------------
@generate_app.command("dashboard")
def generate_dashboard() -> None:
    """Generate the human-readable dashboard."""
    from .generators import generate_dashboard as _gen

    root = find_root()
    output = _gen(root)
    out_dir = views_dir(root)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "dashboard.md"
    out_file.write_text(output, encoding="utf-8")
    typer.echo(f"Generated {out_file.relative_to(root)}")


# ---------------------------------------------------------------------------
# personalos generate contexts
# ---------------------------------------------------------------------------
@generate_app.command("contexts")
def generate_contexts() -> None:
    """Generate AI context exports."""
    from .generators import generate_ai_contexts as _gen

    root = find_root()
    _gen(root)
    typer.echo("Generated AI context exports.")


# ---------------------------------------------------------------------------
# personalos generate graph
# ---------------------------------------------------------------------------
@generate_app.command("graph")
def generate_graph_cmd() -> None:
    """Generate a Mermaid relationship graph."""
    from .generators import generate_graph as _gen

    root = find_root()
    output = _gen(root)
    out_dir = views_dir(root)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "graph.mmd"
    out_file.write_text(output, encoding="utf-8")
    typer.echo(f"Generated {out_file.relative_to(root)}")


# ---------------------------------------------------------------------------
# personalos generate all
# ---------------------------------------------------------------------------
@generate_app.command("all")
def generate_all() -> None:
    """Run all generators."""
    from .generators import generate_ai_contexts, generate_dashboard, generate_graph, generate_json_export

    root = find_root()
    config = load_config(root)

    # Dashboard
    v_dir = views_dir(root, config)
    v_dir.mkdir(parents=True, exist_ok=True)
    (v_dir / "dashboard.md").write_text(generate_dashboard(root), encoding="utf-8")

    # Graph
    (v_dir / "graph.mmd").write_text(generate_graph(root), encoding="utf-8")

    # AI contexts
    generate_ai_contexts(root)

    # JSON export
    generate_json_export(root)

    typer.echo("Generated all views and exports.")


# ---------------------------------------------------------------------------
# personalos review create
# ---------------------------------------------------------------------------
@app.command("review")
def review_create() -> None:
    """Create a new weekly review entity."""
    root = find_root()
    config = load_config(root)
    today = datetime.date.today()
    iso_cal = today.isocalendar()
    period = f"{iso_cal[0]}-W{iso_cal[1]:02d}"
    title = f"Weekly Review {period}"
    slug = slugify(title)
    ent_id = generate_id("review")

    lines = [
        "---",
        f"id: {ent_id}",
        "type: review",
        f"slug: {slug}",
        f"title: {title}",
        "status: draft",
        f"period: {period}",
        "highlights: []",
        "lowlights: []",
        "next_actions: []",
        f"created_at: {today.isoformat()}",
        f"updated_at: {today.isoformat()}",
        "tags: [review]",
        "---",
        "",
        f"# {title}",
        "",
        "## Highlights",
        "",
        "- ",
        "",
        "## Lowlights",
        "",
        "- ",
        "",
        "## Next Actions",
        "",
        "- ",
        "",
    ]

    subdir = entities_dir(root, config) / ENTITY_SUBDIRS["review"]
    subdir.mkdir(parents=True, exist_ok=True)
    filepath = subdir / f"{slug}.md"
    filepath.write_text("\n".join(lines), encoding="utf-8")
    typer.echo(f"Created {filepath.relative_to(root)}")


# ---------------------------------------------------------------------------
# personalos archive
# ---------------------------------------------------------------------------
@app.command()
def archive(
    dry_run: bool = typer.Option(True, "--dry-run/--execute", help="List entities eligible for archival."),
) -> None:
    """List (or archive) entities eligible for archival."""
    root = find_root()
    entities = load_all_entities(root)
    archivable_statuses = {"shipped", "reviewed", "done", "decided", "accepted", "rejected", "withdrawn", "published", "retired"}
    eligible = [e for e in entities if e.get("status") in archivable_statuses]

    if not eligible:
        typer.echo("No entities eligible for archival.")
        raise typer.Exit(0)

    typer.echo(f"Found {len(eligible)} entity(ies) eligible for archival:")
    for e in eligible:
        typer.echo(f"  [{e.get('type')}] {e.get('title')} ({e.get('status')})")

    if dry_run:
        typer.echo("\nRun with --execute to archive these entities.")


# ---------------------------------------------------------------------------
# personalos doctor
# ---------------------------------------------------------------------------
@app.command()
def doctor() -> None:
    """Diagnose common setup issues."""
    root = find_root()
    config = load_config(root)
    issues: list[str] = []

    # Python version
    if sys.version_info < (3, 10):
        issues.append(f"Python 3.10+ required, found {sys.version}")

    # Required directories
    for name, path_fn in [
        ("schema", lambda: schema_dir(root, config)),
        ("entities", lambda: entities_dir(root, config)),
    ]:
        if not path_fn().exists():
            issues.append(f"Missing directory: {name}/")

    # Schema files
    s_dir = schema_dir(root, config)
    if s_dir.exists():
        schema_files = list(s_dir.glob("*.schema.json"))
        if not schema_files:
            issues.append("No schema files found in schema/")
        for sf in schema_files:
            try:
                with open(sf, "r", encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError as exc:
                issues.append(f"Invalid JSON in {sf.name}: {exc}")

    # Dependencies
    missing_deps: list[str] = []
    for pkg in ["typer", "pydantic", "yaml", "frontmatter", "jsonschema", "ulid"]:
        try:
            __import__(pkg)
        except ImportError:
            missing_deps.append(pkg)
    if missing_deps:
        issues.append(f"Missing Python packages: {', '.join(missing_deps)}")

    if not issues:
        typer.echo("Everything looks good.")
        typer.echo(f"  Python: {sys.version.split()[0]}")
        typer.echo(f"  Root: {root}")
        typer.echo(f"  Config: personalos.toml {'found' if (root / 'personalos.toml').exists() else 'using defaults'}")
        raise typer.Exit(0)

    typer.echo(f"Found {len(issues)} issue(s):")
    for issue in issues:
        typer.echo(f"  - {issue}")
    raise typer.Exit(1)


# ---------------------------------------------------------------------------
# personalos diff
# ---------------------------------------------------------------------------
@app.command("diff")
def diff_cmd() -> None:
    """Show what would change if generators were re-run."""
    import difflib

    from .generators import generate_ai_contexts, generate_dashboard, generate_graph, generate_json_export

    root = find_root()
    config = load_config(root)
    changes_found = False

    # Check dashboard
    v_dir = views_dir(root, config)
    dashboard_path = v_dir / "dashboard.md"
    new_dashboard = generate_dashboard(root)
    if dashboard_path.exists():
        old = dashboard_path.read_text(encoding="utf-8")
        if old != new_dashboard:
            changes_found = True
            typer.echo("--- views/dashboard.md")
            for line in difflib.unified_diff(
                old.splitlines(), new_dashboard.splitlines(),
                fromfile="views/dashboard.md (current)",
                tofile="views/dashboard.md (generated)",
                lineterm="",
            ):
                typer.echo(line)
    else:
        changes_found = True
        typer.echo("+ views/dashboard.md (new file)")

    # Check graph
    graph_path = v_dir / "graph.mmd"
    new_graph = generate_graph(root)
    if graph_path.exists():
        old = graph_path.read_text(encoding="utf-8")
        if old != new_graph:
            changes_found = True
            typer.echo("\n--- views/graph.mmd")
            for line in difflib.unified_diff(
                old.splitlines(), new_graph.splitlines(),
                fromfile="views/graph.mmd (current)",
                tofile="views/graph.mmd (generated)",
                lineterm="",
            ):
                typer.echo(line)
    else:
        changes_found = True
        typer.echo("+ views/graph.mmd (new file)")

    if not changes_found:
        typer.echo("No changes detected. Generated output is up to date.")


# ---------------------------------------------------------------------------
# personalos version
# ---------------------------------------------------------------------------
@app.command()
def version() -> None:
    """Show the PersonalOS CLI version."""
    typer.echo(f"personalos {__version__}")


if __name__ == "__main__":
    app()
