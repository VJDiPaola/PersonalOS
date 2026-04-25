# PersonalOS Architecture

## Overview

PersonalOS is a markdown-first personal operating system built on three layers:

1. **Source** (`entities/`) — canonical records authored by humans
2. **Views** (`views/`) — generated human-readable dashboards and reports
3. **Exports** (`exports/`) — generated machine-readable JSON and AI context files

Schemas (`schema/`) define the contracts that bind all three layers together. The CLI (`personalos`) is the single tool that validates, generates, and manages the system.

## Directory Layout

```text
PersonalOS/
  schema/             # JSON Schema contracts
  entities/           # Canonical markdown records (source of truth)
    projects/
    tasks/
    tools/
    contacts/
    applications/
    decisions/
    reviews/
  views/              # Generated human-readable output
    dashboard.md
    graph.mmd
  exports/            # Generated machine-readable output
    context/
    json/
  cli/                # CLI source code
    personalos/
  tests/              # Validation, smoke, and golden tests
    fixtures/
    golden/
  docs/               # Documentation
```

## Entity Identity Model

Every entity has a shared set of identity fields:

- `id` — globally unique, prefixed ULID (e.g. `prj_01JYV4R2D3J7M7X9Q0N2K8A6P1`)
- `type` — entity kind (`project`, `task`, `tool`, `contact`, `application`, `decision`, `review`)
- `slug` — URL-safe, human-readable identifier derived from the title
- `title` — display name
- `status` — lifecycle state (varies by entity type)
- `created_at` — ISO 8601 date
- `updated_at` — ISO 8601 date
- `tags` — freeform labels for filtering and grouping

### ID Prefix Map

| Type        | Prefix     |
|-------------|------------|
| project     | `prj_`     |
| task        | `tsk_`     |
| tool        | `tool_`    |
| contact     | `contact_` |
| application | `app_`     |
| decision    | `dec_`     |
| review      | `rev_`     |

Prefixes are customizable via `personalos.toml`.

### Relationships

Entities reference each other by stable ID:

- `project_id` — links a task to its parent project
- `tool_ids` — links an entity to the tools it uses
- `contact_ids` — links an entity to related people
- `related_entity_ids` — generic cross-references

Freeform string references should be avoided where a stable ID can be used.

## Lifecycle States

### Projects

```text
idea → active → building → deploy_ready → shipped → reviewed → archived
```

### Tasks

```text
todo → in_progress → blocked → done → archived
```

### Applications

```text
draft → applied → interviewing → offer → accepted → rejected → withdrawn
```

### Decisions

```text
open → decided → revisited → archived
```

Explicit lifecycle states are always preferred over boolean flags.

## Source vs Generated Content

- **Source** content lives in `entities/`. It is authored and edited by humans.
- **Generated** content lives in `views/` and `exports/`. It is produced by `personalos generate` commands and should not be hand-edited.
- Generated content is committed to the repo so it is visible without running the CLI, but CI enforces that it stays in sync with source.

## CLI Role

The `personalos` CLI is the single entry point for all operations:

- **Validation** — check entities against schemas
- **Scaffolding** — create new entities from schema-driven templates
- **Generation** — produce dashboards, AI context exports, and relationship graphs
- **Diagnostics** — detect setup issues and stale generated output

See [docs/quickstart.md](quickstart.md) for usage.
