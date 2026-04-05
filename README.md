# PersonalOS

A markdown-first personal operating system. Track projects, tasks, decisions, reviews, and more — all in version-controlled markdown with YAML frontmatter.

## What This Is

PersonalOS is a public starter template for building your own markdown-based personal dashboard. It provides:

- **JSON schemas** for 7 entity types (projects, tasks, tools, contacts, applications, decisions, reviews)
- **A CLI** (`personalos`) for validation, scaffolding, and generation
- **Generated dashboards** — human-readable markdown views
- **AI context exports** — structured JSON for feeding to LLMs
- **Relationship graphs** — Mermaid diagrams of entity connections
- **Tests and CI** — schema validation, golden tests, and staleness checks

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/PersonalOS.git
cd PersonalOS
pip install -e .
```

### Create an entity

```bash
personalos new project "My Project"
```

### Validate everything

```bash
personalos validate
```

### Generate dashboard, exports, and graph

```bash
personalos generate all
```

## Architecture

```text
schema/         → JSON Schema contracts (shared base + per-entity)
entities/       → Canonical markdown records (source of truth)
views/          → Generated dashboard and relationship graph
exports/        → Generated AI context and JSON exports
cli/            → CLI source (Python + Typer)
tests/          → Schema, CLI, and golden tests
docs/           → Architecture, schema reference, quickstart
```

Source lives in `entities/`. Generated output lives in `views/` and `exports/`. Schemas in `schema/` define the contracts.

## Entity Types

| Type | Prefix | Lifecycle States |
|------|--------|------------------|
| Project | `prj_` | idea → active → building → deploy_ready → shipped → reviewed → archived |
| Task | `tsk_` | todo → in_progress → blocked → done → archived |
| Tool | `tool_` | active → evaluating → retired |
| Contact | `contact_` | active → inactive |
| Application | `app_` | draft → applied → interviewing → offer → accepted → rejected → withdrawn |
| Decision | `dec_` | open → decided → revisited → archived |
| Review | `rev_` | draft → published → archived |

## CLI Commands

```text
personalos init              Scaffold directory structure
personalos new <type> "…"    Create entity from schema template
personalos validate          Check entities against schemas
personalos check             Validate + structural checks
personalos generate all      Generate dashboard, graph, exports
personalos generate dashboard
personalos generate contexts
personalos generate graph
personalos review            Create a weekly review
personalos archive --dry-run List archivable entities
personalos doctor            Diagnose setup issues
personalos diff              Preview generator changes
```

## Configuration

Customize via `personalos.toml`:

```toml
[id_prefixes]
project = "prj_"
task = "tsk_"

[directories]
entities = "entities"
views = "views"
exports = "exports"
```

## Documentation

- [Architecture](docs/architecture.md) — system design and separation of concerns
- [Schema Reference](docs/schema.md) — field definitions for all entity types
- [Quickstart](docs/quickstart.md) — step-by-step setup guide
- [Blueprint](docs/blueprint.md) — original design goals and principles
- [Contributing](CONTRIBUTING.md) — how to add entities and run tests

## License

MIT
