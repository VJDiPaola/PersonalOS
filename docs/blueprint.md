# PersonalOS Blueprint

## Purpose

This document captures the product direction for PersonalOS beyond the currently shipped starter slice.

The repo now includes a working vertical slice for:

- `projects`
- `tasks`
- `decisions`

The blueprint below describes the standard future additions should meet.

## Current Product Bar

The starter should always feel:

- cloneable
- deterministic
- public-safe
- easy to understand in the first 10 minutes
- useful even before a user customizes it

If a proposed change makes the repo feel more like someone else's sanitized private workspace, it misses the point.

## Design Principles

### 1. Schema First

Entity rules should be defined once and reused across:

- validation
- documentation
- generation
- fixtures

### 2. Source vs Views vs Exports

- `entities/` holds canonical records
- `views/` holds generated human-facing outputs
- `exports/` holds generated assistant and JSON context

### 3. Stable Identity

Every entity should keep a stable `id`, readable `slug`, and explicit lifecycle state.

### 4. Cross-Platform By Default

The starter should remain comfortable on Windows, macOS, and Linux, with Python as the current implementation path.

## Current Structure

```text
PersonalOS/
  README.md
  CONTRIBUTING.md
  LICENSE
  docs/
    blueprint.md
    architecture.md
    schema.md
    quickstart.md
  schema/
    base.schema.json
    project.schema.json
    task.schema.json
    decision.schema.json
  entities/
    projects/
    tasks/
    decisions/
  views/
    dashboard.example.md
  exports/
    context/
    json/
  cli/
    personalos/
  tests/
    fixtures/
    golden/
```

## Recommended Next Additions

Once the shipped slice feels stable, the most natural next areas are:

1. `tool`
2. `review`
3. `contact`
4. `application`

Each addition should arrive with:

- a schema
- believable sample records
- generator updates
- tests
- doc updates

## CLI Direction

Shipped today:

- `personalos init`
- `personalos validate`
- `personalos generate dashboard`
- `personalos generate contexts`
- `personalos generate all`

Likely next commands:

- `personalos new project`
- `personalos new task`
- `personalos review create`
- `personalos archive --dry-run`

## Public Starter Content Rules

Include:

- fake sample projects
- fake sample tasks
- fake sample decisions
- useful generated examples

Never include:

- real contacts
- real job applications
- internal-only links
- secrets or `.env` values
- private finance or strategy notes
