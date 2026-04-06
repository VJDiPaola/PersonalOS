# PersonalOS

PersonalOS is a public-safe, markdown-first starter for people who want a version-controlled personal operating system without turning a repo into a private vault.

It ships a thin but real vertical slice: canonical markdown entities, schema-backed validation, deterministic generated views, and assistant-ready exports.

## What Works Today

- A Python CLI with `personalos validate`, `personalos generate dashboard`, `personalos generate contexts`, and `personalos generate all`
- Shipped entity coverage for `projects`, `tasks`, and `decisions`
- JSON Schema contracts plus relationship and public-safety validation
- Believable sample records you can inspect, copy, and extend
- Checked-in generated examples in [`views/dashboard.example.md`](views/dashboard.example.md), [`exports/context/workspace-context.md`](exports/context/workspace-context.md), and [`exports/json/workspace-context.json`](exports/json/workspace-context.json)
- Tests for validation failures, relationship integrity, and golden output parity

## Who It Is For

- Builders who want a cloneable starter instead of a vague “second brain” concept
- People who like storing structured source data in markdown
- Anyone who wants deterministic, AI-friendly exports without mixing source records and generated artifacts

## Five-Minute Start

```bash
python -m pip install -e .[dev]
python -m personalos validate
python -m personalos generate all
pytest
```

After that, inspect:

- [`entities/`](entities)
- [`views/dashboard.example.md`](views/dashboard.example.md)
- [`exports/context/workspace-context.md`](exports/context/workspace-context.md)
- [`docs/quickstart.md`](docs/quickstart.md)

## Example Output

```md
## Snapshot

- Projects: 3 total (1 active, 1 building, 1 deploy_ready)
- Tasks: 5 total (1 blocked, 1 done, 1 in_progress, 2 ready)
- Decisions: 3 total (2 decided, 1 proposed)
```

The full generated dashboard lives at [`views/dashboard.example.md`](views/dashboard.example.md).

## How It Works

```text
schema/   -> contracts for each entity type
entities/ -> canonical markdown records
views/    -> generated human-readable outputs
exports/  -> generated AI / JSON context
cli/      -> Python package and command-line entrypoint
tests/    -> fixtures, validation tests, and golden checks
docs/     -> architecture, schema, quickstart, and roadmap
```

The source of truth stays in `entities/`. Everything in `views/` and `exports/` is generated from those records.

## Current Scope

Shipped now:

- `project`
- `task`
- `decision`

Planned next:

- `tool`
- `contact`
- `application`
- `review`

The repo is intentionally proving one good end-to-end slice before expanding breadth.

## Docs

- [`docs/quickstart.md`](docs/quickstart.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/schema.md`](docs/schema.md)
- [`docs/blueprint.md`](docs/blueprint.md)

## Why This Repo Exists

The real operating system that inspired this starter stays private so it can remain useful and personal.

This public repo exists to share the architecture, tooling, and starter experience without shipping real contacts, private strategy, financial notes, or internal-only links.
