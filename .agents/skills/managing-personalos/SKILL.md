---
name: managing-personalos
description: "Builds and maintains the PersonalOS public starter repo: architecture docs, schema contracts, CLI scaffolding, example entities, generated sample views, and public-safe AI-operable project structure. Use when asked to scaffold, extend, document, validate, or polish the PersonalOS starter without introducing private real-world data."
---

# Managing PersonalOS

Operational workflow for the `PersonalOS` public starter repository.

This skill is for building a reusable template, not for managing a live private dashboard.

## Core Rule

Keep the repo public-safe and starter-friendly.

Always optimize for:

- clarity
- reusability
- determinism
- sample data quality
- clean onboarding

Never optimize for preserving private history or personal operating detail.

## What To Build

Prefer work in these areas:

- `docs/`
- `schema/`
- `entities/`
- `views/`
- `exports/`
- `cli/`
- `tests/`

If the repo is still early, start with:

1. architecture docs
2. schema contracts
3. CLI scaffolding
4. example entities
5. generated sample views
6. tests

## Public-Safe Data Rules

Only use:

- synthetic names
- generic project examples
- fake contacts and applications
- neutral sample links

Never add:

- real names unless already explicitly intended for public use
- private strategy notes
- financial runway details
- secrets or `.env` contents
- personal emails or job-search material copied from a private repo

## README Standard

Treat `README.md` as a product landing page.

It should explain:

- what PersonalOS is
- who it helps
- how the system works
- how to get started quickly
- where to find architecture and schema docs

Do not turn the README into a personal dashboard dump.

## Architecture Standards

Prefer this separation:

- `schema/` for contracts
- `entities/` for source records
- `views/` for generated human-readable outputs
- `exports/` for generated AI and JSON outputs

Do not blur source and generated data without a strong reason.

## Entity Standards

When defining starter entities, prefer fields like:

- `id`
- `type`
- `slug`
- `title`
- `status`
- `created_at`
- `updated_at`
- `tags`

Use stable IDs for relationships such as:

- `project_id`
- `contact_ids`
- `related_entity_ids`

Avoid freeform string references where a stable ID should exist.

## Lifecycle Standards

For projects, prefer explicit states:

- `idea`
- `active`
- `building`
- `deploy_ready`
- `shipped`
- `reviewed`
- `archived`

Prefer explicit date fields over boolean lifecycle side flags.

## CLI Direction

Prefer one CLI over many shell scripts.

Recommended command surface:

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

If choosing an implementation language, prefer Python for:

- Windows compatibility
- schema tooling
- testability
- packaging

## Example Content Guidance

Starter content should be believable and useful.

Good examples:

- `portfolio-site-refresh`
- `local-habit-tracker`
- `ship landing page copy`
- `review activation funnel`
- `Should this project stay solo or become a product?`

Bad examples:

- content copied directly from a private personal OS
- half-sanitized real applications
- vague filler records with no practical value

## Testing Expectations

As the starter grows, maintain:

- schema validation tests
- CLI smoke tests
- generator golden tests
- public export tests

If a feature changes generated output, update or add fixtures so the behavior stays legible and deterministic.

## Decision Filter

When deciding between two implementations, prefer the one that makes the repo:

- easier for a new user to understand
- safer to publish
- easier for Codex to operate on
- less dependent on hidden context

That is the standard for PersonalOS.
