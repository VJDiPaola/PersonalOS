# PersonalOS Blueprint

## Goal

Build a public starter repo for a markdown-first personal operating system that feels professional, cloneable, and extensible.

This repo is not meant to contain anyone's real private operating data.

It should provide:

- architecture
- schema contracts
- CLI scaffolding
- sample entities
- generated example views
- tests

## Product Positioning

PersonalOS should feel like a real starter product, not a dump of somebody else's private notes.

That means:

- clean docs
- believable example data
- deterministic generated outputs
- one obvious path to get started

## Design Principles

### 1. Schema First

Entity rules should be defined once and reused everywhere.

The schema layer should drive:

- validation
- templates
- docs
- generators

### 2. Source vs Views vs Exports

- `entities/` holds canonical records
- `views/` holds generated human-facing dashboards and reports
- `exports/` holds generated AI and JSON outputs

### 3. Stable Identity

Every entity should have:

- `id`
- `type`
- `slug`
- `title`
- `created_at`
- `updated_at`

### 4. Clean Lifecycle Modeling

Projects should use explicit lifecycle states:

- `idea`
- `active`
- `building`
- `deploy_ready`
- `shipped`
- `reviewed`
- `archived`

### 5. Cross-Platform by Default

The engine should work well on Windows, macOS, and Linux.

### 6. Starter Quality Matters

The first 10 minutes should be good enough that someone immediately understands:

- what the system does
- how to add a project
- how to generate a dashboard
- how to adapt it to their own life

## Target Structure

```text
PersonalOS/
  README.md
  docs/
    blueprint.md
    architecture.md
    schema.md
    quickstart.md
  schema/
    project.schema.json
    task.schema.json
    tool.schema.json
    contact.schema.json
    application.schema.json
    decision.schema.json
    review.schema.json
  entities/
    projects/
    tasks/
    tools/
    contacts/
    applications/
    decisions/
    reviews/
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

## Recommended CLI

```text
personalos init
personalos check
personalos validate
personalos generate all
personalos generate dashboard
personalos generate contexts
personalos new project "Project Name"
personalos new task "Task Name"
personalos review create
personalos archive --dry-run
```

## Suggested Implementation

Recommended stack:

- Python
- `typer`
- `pydantic`
- YAML frontmatter parsing
- golden-file tests

## Example Entity Contract

```yaml
---
id: prj_01JYV4R2D3J7M7X9Q0N2K8A6P1
type: project
slug: portfolio-site-refresh
title: Portfolio Site Refresh
status: building
priority: high
created_at: 2026-04-04
updated_at: 2026-04-04
tags: [portfolio, design, writing]
tool_ids: [tool_claude, tool_linear]
---
```

## Public Starter Content Rules

Include:

- fake sample projects
- fake sample tasks
- fake sample decisions
- clear example reviews
- screenshots or example outputs

Never include:

- real contacts
- real applications
- private strategy
- personal runway or financial data
- secrets or `.env` values

## Near-Term Build Plan

1. Add architecture and schema docs.
2. Define the first entity schemas.
3. Scaffold the CLI.
4. Add example entities.
5. Generate the first sample dashboard.
6. Add tests.

## Standard of Quality

PersonalOS should feel:

- useful
- legible
- opinionated
- safe to clone
- easy to extend

If it feels like a private vault that was merely cleaned up, it is not ready yet.
