from __future__ import annotations

import argparse
from pathlib import Path

from personalos.workspace import (
    ValidationIssue,
    WorkspaceError,
    scaffold_workspace,
    validate_workspace,
    write_contexts,
    write_dashboard,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="personalos",
        description="Validate and generate a public-safe PersonalOS starter workspace.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Workspace root. Defaults to the current working directory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create the standard PersonalOS directory structure.")
    init_parser.add_argument(
        "--path",
        default=".",
        help="Directory to scaffold. Defaults to the current working directory.",
    )

    subparsers.add_parser("validate", help="Validate entities, schemas, relationships, and public-safe content.")

    generate_parser = subparsers.add_parser("generate", help="Generate checked-in sample outputs.")
    generate_subparsers = generate_parser.add_subparsers(dest="generate_command", required=True)

    dashboard_parser = generate_subparsers.add_parser("dashboard", help="Generate the dashboard markdown view.")
    dashboard_parser.add_argument(
        "--output",
        default=None,
        help="Optional output path for the generated dashboard.",
    )

    contexts_parser = generate_subparsers.add_parser("contexts", help="Generate assistant-ready markdown and JSON exports.")
    contexts_parser.add_argument(
        "--context-output",
        default=None,
        help="Optional output path for the markdown context file.",
    )
    contexts_parser.add_argument(
        "--json-output",
        default=None,
        help="Optional output path for the JSON context file.",
    )

    generate_subparsers.add_parser("all", help="Generate the dashboard and both context exports.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        created = scaffold_workspace(Path(args.path).resolve())
        print(f"Scaffolded {len(created)} PersonalOS directories in {Path(args.path).resolve()}.")
        return 0

    root = Path(args.root).resolve()

    try:
        if args.command == "validate":
            result = validate_workspace(root)
            if not result.is_valid:
                print("Validation failed:")
                for issue in result.issues:
                    print(f"- {_render_issue(issue, root)}")
                return 1
            counts_text = ", ".join(f"{entity_type}={count}" for entity_type, count in result.counts.items())
            print(f"Validated PersonalOS workspace: {len(result.records)} entities ({counts_text}).")
            return 0

        if args.command == "generate":
            if args.generate_command == "dashboard":
                output = write_dashboard(root, Path(args.output).resolve() if args.output else None)
                print(f"Wrote dashboard to {output}.")
                return 0
            if args.generate_command == "contexts":
                markdown_output, json_output = write_contexts(
                    root,
                    Path(args.context_output).resolve() if args.context_output else None,
                    Path(args.json_output).resolve() if args.json_output else None,
                )
                print(f"Wrote markdown context to {markdown_output}.")
                print(f"Wrote JSON context to {json_output}.")
                return 0
            if args.generate_command == "all":
                dashboard_output = write_dashboard(root)
                markdown_output, json_output = write_contexts(root)
                print(f"Wrote dashboard to {dashboard_output}.")
                print(f"Wrote markdown context to {markdown_output}.")
                print(f"Wrote JSON context to {json_output}.")
                return 0
    except WorkspaceError as exc:
        print(str(exc))
        return 1

    parser.print_help()
    return 1


def _render_issue(issue: ValidationIssue, root: Path) -> str:
    return issue.render(root)
