# PersonalOS Schema Guide

## Base Contract

Every shipped entity type inherits the same base fields.

| Field | Required | Purpose |
| --- | --- | --- |
| `id` | yes | Stable identifier for cross-entity references |
| `type` | yes | Entity kind: `project`, `task`, or `decision` |
| `slug` | yes | Human-readable, URL-safe identifier |
| `title` | yes | Short display title |
| `status` | yes | Explicit lifecycle state |
| `created_at` | yes | Creation date in `YYYY-MM-DD` form |
| `updated_at` | yes | Last meaningful update date |
| `tags` | yes | Searchable, low-cardinality labels |
| `summary` | yes | One-sentence explanation of why the record exists |

The base contract is defined in [`schema/base.schema.json`](../schema/base.schema.json).

## Project Schema

Defined in [`schema/project.schema.json`](../schema/project.schema.json).

Additional required fields:

- `priority`: `low`, `medium`, `high`
- `horizon`: `now`, `next`, `later`

Allowed statuses:

- `idea`
- `active`
- `building`
- `deploy_ready`
- `shipped`
- `reviewed`
- `archived`

## Task Schema

Defined in [`schema/task.schema.json`](../schema/task.schema.json).

Additional required fields:

- `project_id`
- `priority`
- `energy`

Optional fields:

- `due_on`

Allowed statuses:

- `backlog`
- `ready`
- `in_progress`
- `blocked`
- `done`
- `archived`

## Decision Schema

Defined in [`schema/decision.schema.json`](../schema/decision.schema.json).

Additional required fields:

- `project_id`
- `decision_date`
- `outcome`
- `related_task_ids`

Allowed statuses:

- `proposed`
- `decided`
- `rejected`
- `archived`

Allowed outcomes:

- `commit`
- `hold`
- `revisit`

## Relationship Rules

The starter enforces a few opinionated integrity checks:

- every `task.project_id` must point to a real project
- every `decision.project_id` must point to a real project
- every value in `decision.related_task_ids` must point to a real task
- IDs and slugs must be unique across shipped records

## Public-Safety Rules

Because this repo is a public starter, entity validation rejects obviously private content such as:

- email addresses
- secret-like tokens
- finance-heavy private terms like `salary`, `runway`, or `ssn`

That check is intentionally conservative for sample data. If you clone this starter for private personal use, you can relax those rules later.
