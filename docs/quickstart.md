# PersonalOS Quickstart

## Prerequisites

- Python 3.10+
- pip

## 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/PersonalOS.git
cd PersonalOS
```

## 2. Install the CLI

```bash
pip install -e .
```

This installs the `personalos` command globally.

## 3. Initialize (Optional)

If starting from scratch (not using the starter entities):

```bash
personalos init
```

This creates the `entities/`, `views/`, and `exports/` directories.

## 4. Create an Entity

```bash
personalos new project "My First Project"
```

This generates `entities/projects/my-first-project.md` with a pre-filled frontmatter template derived from the project schema.

## 5. Edit the Entity

Open the generated file and fill in the details. The frontmatter fields are documented in [docs/schema.md](schema.md).

## 6. Validate

```bash
personalos validate
```

Checks all entities against their JSON schemas and reports any errors.

## 7. Generate Views and Exports

```bash
personalos generate all
```

This produces:

- `views/dashboard.md` — a human-readable project dashboard
- `views/graph.mmd` — a Mermaid relationship diagram
- `exports/context/full-context.json` — full AI context export
- `exports/context/per-project/` — per-project AI context files
- `exports/json/` — individual JSON files per entity

## 8. Check Everything

```bash
personalos check
```

Runs validation plus structural checks (orphan IDs, missing directories).

## 9. Preview Changes

```bash
personalos diff
```

Shows what would change if generators were re-run, without writing files.

## 10. Diagnose Issues

```bash
personalos doctor
```

Reports Python version, missing dependencies, schema issues, and directory problems.

## Optional: Pre-Commit Hook

Install [pre-commit](https://pre-commit.com/) to auto-validate before each commit:

```bash
pip install pre-commit
pre-commit install
```

## Next Steps

- Read [docs/architecture.md](architecture.md) for the full system design
- Read [docs/schema.md](schema.md) for the complete field reference
- Browse `entities/` for example records
- Customize `personalos.toml` for your own ID prefixes and settings
