from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ENTITY_DIRECTORIES = {
    "project": "projects",
    "task": "tasks",
    "decision": "decisions",
}

SCHEMA_FILES = {
    "project": "project.schema.json",
    "task": "task.schema.json",
    "decision": "decision.schema.json",
}

PRIVATE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "email address",
        re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    ),
    (
        "secret-like token",
        re.compile(r"\b(?:sk|ghp)_[A-Za-z0-9]{20,}\b"),
    ),
    (
        "private finance term",
        re.compile(r"\b(?:runway|salary|compensation|social security|ssn)\b", re.IGNORECASE),
    ),
)


class WorkspaceError(RuntimeError):
    """Raised when the workspace is missing required structure or valid content."""


@dataclass(frozen=True)
class EntityRecord:
    path: Path
    entity_type: str
    metadata: dict[str, Any]
    body: str

    @property
    def id(self) -> str:
        return str(self.metadata["id"])

    @property
    def slug(self) -> str:
        return str(self.metadata["slug"])

    @property
    def title(self) -> str:
        return str(self.metadata["title"])

    @property
    def status(self) -> str:
        return str(self.metadata["status"])


@dataclass(frozen=True)
class ValidationIssue:
    path: Path | None
    message: str

    def render(self, root: Path) -> str:
        if self.path is None:
            return self.message
        return f"{self.path.relative_to(root)}: {self.message}"


@dataclass(frozen=True)
class ValidationResult:
    root: Path
    records: tuple[EntityRecord, ...]
    issues: tuple[ValidationIssue, ...]

    @property
    def is_valid(self) -> bool:
        return not self.issues

    @property
    def counts(self) -> dict[str, int]:
        counts: dict[str, int] = {entity_type: 0 for entity_type in ENTITY_DIRECTORIES}
        for record in self.records:
            counts[record.entity_type] += 1
        return counts


@dataclass(frozen=True)
class WorkspaceData:
    root: Path
    projects: tuple[EntityRecord, ...]
    tasks: tuple[EntityRecord, ...]
    decisions: tuple[EntityRecord, ...]

    @property
    def all_records(self) -> tuple[EntityRecord, ...]:
        return self.projects + self.tasks + self.decisions


def scaffold_workspace(path: Path) -> list[Path]:
    created: list[Path] = []
    for relative in (
        Path("schema"),
        Path("entities/projects"),
        Path("entities/tasks"),
        Path("entities/decisions"),
        Path("views"),
        Path("exports/context"),
        Path("exports/json"),
        Path("docs"),
        Path("tests/fixtures"),
        Path("tests/golden"),
    ):
        target = path / relative
        target.mkdir(parents=True, exist_ok=True)
        created.append(target)
        if not any(target.iterdir()):
            (target / ".gitkeep").write_text("", encoding="utf-8")
    return created


def validate_workspace(root: Path) -> ValidationResult:
    root = root.resolve()
    issues: list[ValidationIssue] = []
    records: list[EntityRecord] = []

    try:
        schemas, registry = load_schemas(root / "schema")
    except WorkspaceError as exc:
        return ValidationResult(root=root, records=tuple(), issues=(ValidationIssue(None, str(exc)),))

    for entity_type, folder_name in ENTITY_DIRECTORIES.items():
        entity_dir = root / "entities" / folder_name
        if not entity_dir.exists():
            issues.append(ValidationIssue(entity_dir, "missing required entity directory"))
            continue

        for path in sorted(entity_dir.glob("*.md")):
            try:
                record = parse_entity_file(path, entity_type)
            except WorkspaceError as exc:
                issues.append(ValidationIssue(path, str(exc)))
                continue

            schema = schemas[entity_type]
            validator = Draft202012Validator(
                schema,
                registry=registry,
                format_checker=FormatChecker(),
            )
            errors = sorted(validator.iter_errors(record.metadata), key=lambda error: list(error.path))
            for error in errors:
                location = ".".join(str(part) for part in error.absolute_path)
                message = error.message if not location else f"{location}: {error.message}"
                issues.append(ValidationIssue(path, message))

            if record.metadata.get("type") != entity_type:
                issues.append(ValidationIssue(path, f"type must be '{entity_type}'"))

            records.append(record)

    issues.extend(check_uniqueness(records))
    issues.extend(check_relationships(records))
    issues.extend(check_public_safety(records))

    return ValidationResult(root=root, records=tuple(records), issues=tuple(issues))


def load_workspace(root: Path) -> WorkspaceData:
    result = validate_workspace(root)
    if not result.is_valid:
        rendered = "\n".join(f"- {issue.render(result.root)}" for issue in result.issues)
        raise WorkspaceError(f"Workspace validation failed:\n{rendered}")

    by_type: dict[str, list[EntityRecord]] = defaultdict(list)
    for record in result.records:
        by_type[record.entity_type].append(record)

    return WorkspaceData(
        root=result.root,
        projects=tuple(sorted(by_type["project"], key=sort_key)),
        tasks=tuple(sorted(by_type["task"], key=sort_key)),
        decisions=tuple(sorted(by_type["decision"], key=sort_key)),
    )


def render_dashboard(workspace: WorkspaceData) -> str:
    project_by_id = {record.id: record for record in workspace.projects}
    tasks_by_project: dict[str, list[EntityRecord]] = defaultdict(list)
    decisions_by_project: dict[str, list[EntityRecord]] = defaultdict(list)

    for task in workspace.tasks:
        tasks_by_project[str(task.metadata["project_id"])].append(task)
    for decision in workspace.decisions:
        decisions_by_project[str(decision.metadata["project_id"])].append(decision)

    lines = [
        "# PersonalOS Starter Dashboard",
        "",
        "This dashboard is generated from the canonical markdown records in `entities/`.",
        "",
        "## Snapshot",
        "",
        f"- Projects: {len(workspace.projects)} total ({summarize_statuses(workspace.projects)})",
        f"- Tasks: {len(workspace.tasks)} total ({summarize_statuses(workspace.tasks)})",
        f"- Decisions: {len(workspace.decisions)} total ({summarize_statuses(workspace.decisions)})",
        "",
        "## Projects",
        "",
    ]

    for project in workspace.projects:
        linked_tasks = tasks_by_project.get(project.id, [])
        linked_decisions = decisions_by_project.get(project.id, [])
        lines.extend(
            [
                f"### {project.title}",
                "",
                f"- Status: `{project.status}`",
                f"- Priority: `{project.metadata['priority']}`",
                f"- Summary: {project.metadata['summary']}",
                f"- Tags: {', '.join(project.metadata['tags'])}",
                f"- Open tasks: {count_open_tasks(linked_tasks)}",
                f"- Decisions: {len(linked_decisions)} recorded",
            ]
        )
        open_tasks = [task for task in linked_tasks if task.status not in {"done", "archived"}]
        if open_tasks:
            lines.append("- Next tasks:")
            for task in open_tasks:
                due_text = f" (due {task.metadata['due_on']})" if task.metadata.get("due_on") else ""
                lines.append(f"  - [{task.status}] {task.title}{due_text}")
        if linked_decisions:
            latest = linked_decisions[-1]
            lines.append(f"- Latest decision: {latest.title} ({latest.status})")
        lines.extend(["", project.body, ""])

    lines.extend(["## Tasks To Move This Week", ""])
    for task in workspace.tasks:
        if task.status in {"done", "archived"}:
            continue
        project = project_by_id[str(task.metadata["project_id"])]
        due_text = f", due {task.metadata['due_on']}" if task.metadata.get("due_on") else ""
        lines.extend(
            [
                f"- [{task.status}] {task.title} ({project.title}{due_text})",
                f"  - {task.metadata['summary']}",
            ]
        )

    completed_tasks = [task for task in workspace.tasks if task.status == "done"]
    if completed_tasks:
        lines.extend(["", "## Completed Recently", ""])
        for task in completed_tasks:
            project = project_by_id[str(task.metadata["project_id"])]
            lines.extend(
                [
                    f"- {task.title} ({project.title})",
                    f"  - {task.metadata['summary']}",
                ]
            )

    lines.extend(["", "## Decision Log", ""])
    for decision in workspace.decisions:
        project = project_by_id[str(decision.metadata["project_id"])]
        task_refs = ", ".join(decision.metadata.get("related_task_ids", [])) or "none"
        lines.extend(
            [
                f"- [{decision.status}] {decision.title} ({project.title}, {decision.metadata['decision_date']})",
                f"  - Outcome: {decision.metadata['outcome']}",
                f"  - Related task IDs: {task_refs}",
                f"  - {decision.metadata['summary']}",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_context_markdown(workspace: WorkspaceData) -> str:
    lines = [
        "# PersonalOS Workspace Context",
        "",
        "Use this file as public-safe assistant context for the starter workspace.",
        "",
        "## Workspace Summary",
        "",
        f"- Projects: {len(workspace.projects)}",
        f"- Tasks: {len(workspace.tasks)}",
        f"- Decisions: {len(workspace.decisions)}",
        "",
        "## Active Projects",
        "",
    ]

    for project in workspace.projects:
        lines.extend(
            [
                f"### {project.title}",
                "",
                f"- ID: `{project.id}`",
                f"- Status: `{project.status}`",
                f"- Summary: {project.metadata['summary']}",
                f"- Tags: {', '.join(project.metadata['tags'])}",
                f"- Body: {project.body}",
                "",
            ]
        )

    lines.extend(["## Open Tasks", ""])
    for task in workspace.tasks:
        if task.status in {"done", "archived"}:
            continue
        lines.extend(
            [
                f"- `{task.id}` {task.title} [{task.status}]",
                f"  - Project ID: `{task.metadata['project_id']}`",
                f"  - Summary: {task.metadata['summary']}",
            ]
        )

    lines.extend(["", "## Decision Notes", ""])
    for decision in workspace.decisions:
        lines.extend(
            [
                f"- `{decision.id}` {decision.title} [{decision.status}]",
                f"  - Outcome: {decision.metadata['outcome']}",
                f"  - Summary: {decision.metadata['summary']}",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_context_json(workspace: WorkspaceData) -> str:
    payload = {
        "workspace": {
            "name": "PersonalOS starter workspace",
            "description": "Public-safe sample workspace for the PersonalOS template repository.",
            "entity_counts": {
                "projects": len(workspace.projects),
                "tasks": len(workspace.tasks),
                "decisions": len(workspace.decisions),
            },
        },
        "projects": [serialize_record(record, workspace.root) for record in workspace.projects],
        "tasks": [serialize_record(record, workspace.root) for record in workspace.tasks],
        "decisions": [serialize_record(record, workspace.root) for record in workspace.decisions],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def write_dashboard(root: Path, output_path: Path | None = None) -> Path:
    workspace = load_workspace(root)
    target = output_path or workspace.root / "views" / "dashboard.example.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_dashboard(workspace), encoding="utf-8")
    return target


def write_contexts(
    root: Path,
    markdown_output: Path | None = None,
    json_output: Path | None = None,
) -> tuple[Path, Path]:
    workspace = load_workspace(root)
    markdown_target = markdown_output or workspace.root / "exports" / "context" / "workspace-context.md"
    json_target = json_output or workspace.root / "exports" / "json" / "workspace-context.json"
    markdown_target.parent.mkdir(parents=True, exist_ok=True)
    json_target.parent.mkdir(parents=True, exist_ok=True)
    markdown_target.write_text(render_context_markdown(workspace), encoding="utf-8")
    json_target.write_text(render_context_json(workspace), encoding="utf-8")
    return markdown_target, json_target


def load_schemas(schema_dir: Path) -> tuple[dict[str, dict[str, Any]], Registry]:
    if not schema_dir.exists():
        raise WorkspaceError("schema/ is missing; run this command from the workspace root")

    registry = Registry()
    loaded: dict[str, dict[str, Any]] = {}
    for schema_path in sorted(schema_dir.glob("*.schema.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema_id = schema.get("$id")
        if not schema_id:
            raise WorkspaceError(f"{schema_path.name} is missing a $id field")
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))
        loaded[schema_path.name] = schema

    schemas: dict[str, dict[str, Any]] = {}
    for entity_type, file_name in SCHEMA_FILES.items():
        if file_name not in loaded:
            raise WorkspaceError(f"schema/{file_name} is missing")
        schemas[entity_type] = loaded[file_name]
    return schemas, registry


def parse_entity_file(path: Path, expected_type: str) -> EntityRecord:
    raw_text = path.read_text(encoding="utf-8")
    normalized = raw_text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise WorkspaceError("file must start with YAML frontmatter")

    try:
        _, remainder = normalized.split("---\n", 1)
        frontmatter, body = remainder.split("\n---\n", 1)
    except ValueError as exc:
        raise WorkspaceError("file must contain opening and closing frontmatter markers") from exc

    loaded = yaml.safe_load(frontmatter) or {}
    if not isinstance(loaded, dict):
        raise WorkspaceError("frontmatter must deserialize to a mapping")

    metadata = normalize_value(loaded)
    body_text = body.strip()
    return EntityRecord(path=path, entity_type=expected_type, metadata=metadata, body=body_text)


def normalize_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, list):
        return [normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): normalize_value(item) for key, item in value.items()}
    return value


def check_uniqueness(records: list[EntityRecord]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seen_ids: dict[str, Path] = {}
    seen_slugs: dict[str, Path] = {}
    for record in records:
        if record.id in seen_ids:
            issues.append(ValidationIssue(record.path, f"duplicate id already used in {seen_ids[record.id].name}"))
        else:
            seen_ids[record.id] = record.path
        if record.slug in seen_slugs:
            issues.append(ValidationIssue(record.path, f"duplicate slug already used in {seen_slugs[record.slug].name}"))
        else:
            seen_slugs[record.slug] = record.path
    return issues


def check_relationships(records: list[EntityRecord]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    projects = {record.id for record in records if record.entity_type == "project"}
    tasks = {record.id for record in records if record.entity_type == "task"}

    for record in records:
        if record.entity_type == "task":
            project_id = str(record.metadata.get("project_id", ""))
            if project_id not in projects:
                issues.append(ValidationIssue(record.path, f"project_id references unknown project '{project_id}'"))
        if record.entity_type == "decision":
            project_id = str(record.metadata.get("project_id", ""))
            if project_id not in projects:
                issues.append(ValidationIssue(record.path, f"project_id references unknown project '{project_id}'"))
            for task_id in record.metadata.get("related_task_ids", []):
                if task_id not in tasks:
                    issues.append(ValidationIssue(record.path, f"related_task_ids references unknown task '{task_id}'"))
    return issues


def check_public_safety(records: list[EntityRecord]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for record in records:
        haystack = yaml.safe_dump(record.metadata, sort_keys=True) + "\n" + record.body
        for label, pattern in PRIVATE_PATTERNS:
            if pattern.search(haystack):
                issues.append(ValidationIssue(record.path, f"contains a {label}; starter entities must stay public-safe"))
    return issues


def summarize_statuses(records: tuple[EntityRecord, ...]) -> str:
    counts: dict[str, int] = defaultdict(int)
    for record in records:
        counts[record.status] += 1
    return ", ".join(f"{count} {status}" for status, count in sorted(counts.items()))


def count_open_tasks(tasks: list[EntityRecord]) -> int:
    return sum(1 for task in tasks if task.status not in {"done", "archived"})


def serialize_record(record: EntityRecord, root: Path) -> dict[str, Any]:
    return {
        **record.metadata,
        "body": record.body,
        "path": record.path.relative_to(root).as_posix(),
    }


def sort_key(record: EntityRecord) -> tuple[str, str]:
    return (str(record.metadata.get("created_at", "")), record.slug)
