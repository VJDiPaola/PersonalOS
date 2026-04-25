# PersonalOS Schema Reference

## Overview

Entity schemas are defined as JSON Schema files in `schema/`. A shared base (`_base.schema.json`) defines identity and metadata fields. Each entity type extends the base with its own fields.

## Shared Base Fields

Every entity includes these fields (defined in `schema/_base.schema.json`):

- **`id`** (string, required) — prefixed ULID, e.g. `prj_01JYV4R2D3J7M7X9Q0N2K8A6P1`
- **`type`** (string, required) — one of: `project`, `task`, `tool`, `contact`, `application`, `decision`, `review`
- **`slug`** (string, required) — URL-safe identifier, lowercase, hyphen-separated
- **`title`** (string, required) — human-readable display name
- **`status`** (string, required) — lifecycle state (enum varies by type)
- **`created_at`** (string, required) — ISO 8601 date (`YYYY-MM-DD`)
- **`updated_at`** (string, required) — ISO 8601 date (`YYYY-MM-DD`)
- **`tags`** (array of strings, optional) — freeform labels

## ID Format

IDs use a type prefix followed by a ULID:

```text
<prefix><ulid>

prj_01JYV4R2D3J7M7X9Q0N2K8A6P1
tsk_01JYV5A1B2C3D4E5F6G7H8J9K0
```

Prefixes: `prj_`, `tsk_`, `tool_`, `contact_`, `app_`, `dec_`, `rev_`

## Per-Entity Fields

### Project (`schema/project.schema.json`)

- **`status`** — enum: `idea`, `active`, `building`, `deploy_ready`, `shipped`, `reviewed`, `archived`
- **`priority`** — enum: `low`, `medium`, `high`, `critical`
- **`tool_ids`** — array of tool entity IDs
- **`contact_ids`** — array of contact entity IDs
- **`related_entity_ids`** — array of any entity IDs

### Task (`schema/task.schema.json`)

- **`status`** — enum: `todo`, `in_progress`, `blocked`, `done`, `archived`
- **`priority`** — enum: `low`, `medium`, `high`, `critical`
- **`project_id`** — ID of the parent project (optional)
- **`due_date`** — ISO 8601 date (optional)
- **`assignee`** — string (optional)

### Tool (`schema/tool.schema.json`)

- **`status`** — enum: `active`, `evaluating`, `retired`
- **`url`** — URL string (optional)
- **`category`** — string (optional), e.g. `design`, `engineering`, `communication`

### Contact (`schema/contact.schema.json`)

- **`status`** — enum: `active`, `inactive`
- **`role`** — string (optional), e.g. `designer`, `engineer`
- **`organization`** — string (optional)
- **`email`** — string (optional)

### Application (`schema/application.schema.json`)

- **`status`** — enum: `draft`, `applied`, `interviewing`, `offer`, `accepted`, `rejected`, `withdrawn`
- **`company`** — string (required)
- **`role_title`** — string (required)
- **`applied_date`** — ISO 8601 date (optional)
- **`url`** — URL string (optional)

### Decision (`schema/decision.schema.json`)

- **`status`** — enum: `open`, `decided`, `revisited`, `archived`
- **`question`** — string (required), the decision question
- **`outcome`** — string (optional), the chosen answer
- **`decided_date`** — ISO 8601 date (optional)
- **`related_entity_ids`** — array of any entity IDs

### Review (`schema/review.schema.json`)

- **`status`** — enum: `draft`, `published`, `archived`
- **`period`** — string (required), e.g. `2026-W14`
- **`highlights`** — array of strings (optional)
- **`lowlights`** — array of strings (optional)
- **`next_actions`** — array of strings (optional)

## Entity File Format

Entities are markdown files with YAML frontmatter:

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
tool_ids: [tool_01JYV6X1A2B3C4D5E6F7G8H9J0]
---

Free-form notes, context, and documentation go here.
```

The frontmatter is validated against the JSON schema for the entity's `type`. The body content below the frontmatter is freeform markdown.
