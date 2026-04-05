# AGENTS.md - PersonalOS

This repo is a public starter/template for a markdown-first personal operating system.

It is not a live private dashboard. Treat it as a productized starter that other people should be able to clone, understand, and extend safely.

## Repository Purpose

PersonalOS should demonstrate a professional architecture for:

- projects
- tasks
- tools
- contacts
- applications
- decisions
- reviews
- generated dashboards
- generated AI context exports

The repo should remain public-safe, opinionated, and easy to clone.

## Public-Safe Content Rules

Never add:

- real personal contacts
- real job applications
- financial runway details
- private strategy notes
- secrets or `.env` values
- internal-only links

Always prefer:

- synthetic sample entities
- believable but fake example data
- generic screenshots or sample outputs
- reusable docs and tooling

## Current Stage

This repo is currently in blueprint/starter mode.

Until the engine is fully built, prioritize:

- architecture docs
- schema definitions
- CLI scaffolding
- example entities
- generated sample views
- tests

## Intended Structure

As the repo grows, keep to this shape:

```text
docs/
schema/
entities/
views/
exports/
cli/
tests/
.agents/skills/
```

## Source Of Truth

When implemented:

- `schema/` should define entity contracts
- `entities/` should hold canonical records
- `views/` should hold generated human-readable outputs
- `exports/` should hold generated AI/JSON outputs

Do not mix canonical source content with generated artifacts without a clear reason.

## Working Rules

- Prefer stable IDs over freeform references.
- Prefer explicit lifecycle states over boolean side flags.
- Prefer deterministic generation over hand-maintained dashboards.
- Prefer cross-platform tooling, especially Windows-friendly tooling.
- Prefer a single CLI over many one-off scripts.

## README Role

`README.md` should be a product landing page for the starter repo.

Do not turn it into a private dashboard dump.

It should explain:

- what PersonalOS is
- who it is for
- how it works
- how to get started
- where the architecture and schema docs live

## Documentation Priorities

If adding docs, prioritize:

1. `docs/architecture.md`
2. `docs/schema.md`
3. `docs/quickstart.md`
4. sample generated views and screenshots

## Skills

If agent workflows are added, keep them in `.agents/skills/`.

Skills in this repo should help Codex:

- scaffold the starter
- maintain schema/docs parity
- generate sample content
- keep public example data safe and coherent

## Quality Bar

A change is good if it makes the repo feel:

- easier to understand
- more reusable
- more deterministic
- more professional
- safer to publish

If a change makes the repo feel more like somebody's cleaned-up private vault, it is probably the wrong direction.
