# PersonalOS Architecture

## Overview

PersonalOS is a markdown-first starter organized around one core rule: canonical records live in `entities/`, and every human-facing or AI-facing view is generated from those records.

The current shipped slice covers:

- `projects`
- `tasks`
- `decisions`

## Source Of Truth

```text
schema/   -> machine-readable contracts
entities/ -> canonical markdown records with YAML frontmatter
views/    -> generated human-readable outputs
exports/  -> generated markdown and JSON assistant context
cli/      -> validation and generation commands
tests/    -> fixtures and golden parity checks
```

This separation is deliberate:

- editing happens in `entities/`
- validation is driven by `schema/`
- `views/` and `exports/` can always be regenerated

## Data Flow

1. A builder adds or edits markdown records in `entities/`.
2. `personalos validate` parses each file, validates frontmatter against JSON Schema, checks cross-entity references, and rejects obviously private content.
3. `personalos generate dashboard` renders a deterministic markdown dashboard for people.
4. `personalos generate contexts` renders deterministic markdown and JSON exports for AI workflows or downstream automation.
5. Tests assert that sample data still validates and generated outputs still match the committed examples.

## Entity Model

Every shipped entity shares a base contract:

- `id`
- `type`
- `slug`
- `title`
- `status`
- `created_at`
- `updated_at`
- `tags`
- `summary`

Specialized fields extend the base:

- projects add `priority` and `horizon`
- tasks add `project_id`, `priority`, `energy`, and optional `due_on`
- decisions add `project_id`, `decision_date`, `outcome`, and `related_task_ids`

## Validation Model

Validation happens in layers:

1. Frontmatter shape and field constraints via JSON Schema.
2. Relationship checks such as `task.project_id` and `decision.related_task_ids`.
3. Public-safety checks that reject email addresses, secret-like tokens, and obvious private finance language inside starter entities.

This layered approach keeps the repo understandable for humans while still giving automation a reliable contract.

## Generation Model

The current generator writes three committed outputs:

- [`views/dashboard.example.md`](../views/dashboard.example.md)
- [`exports/context/workspace-context.md`](../exports/context/workspace-context.md)
- [`exports/json/workspace-context.json`](../exports/json/workspace-context.json)

These outputs are intentionally deterministic:

- no machine-local absolute paths
- no generation timestamps
- stable sorting by entity metadata

That makes them safe for version control and easy to test.

## Extending The Starter

When adding a new entity type later, keep the pattern consistent:

1. add a schema in `schema/`
2. add a canonical subdirectory in `entities/`
3. update validation and generation rules in `cli/personalos/`
4. add believable sample records
5. update the golden outputs and tests

If a proposed change blurs source data and generated artifacts, the default answer should be no.
