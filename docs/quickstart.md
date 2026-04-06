# PersonalOS Quickstart

## Goal

Get from fresh clone to a validated, generated starter workspace in under 10 minutes.

## 1. Install

From the repo root:

```bash
python -m pip install -e .[dev]
```

If you do not need the test dependencies, `python -m pip install -e .` is enough for normal CLI use.

## 2. Validate The Sample Workspace

```bash
python -m personalos validate
```

Expected result:

- the repo validates 11 sample entities
- relationships resolve cleanly
- the sample content passes public-safety checks

## 3. Generate The Sample Outputs

```bash
python -m personalos generate all
```

This writes:

- [`../views/dashboard.example.md`](../views/dashboard.example.md)
- [`../exports/context/workspace-context.md`](../exports/context/workspace-context.md)
- [`../exports/json/workspace-context.json`](../exports/json/workspace-context.json)

## 4. Run The Test Suite

```bash
pytest
```

The tests verify:

- valid starter records pass
- invalid fixtures fail for the right reasons
- generated outputs still match the committed examples

## 5. Make Your First Change

The current starter does not yet ship `personalos new project` or `personalos new task`, so the fastest path is:

1. copy one of the sample markdown files in `entities/`
2. give it a new `id`, `slug`, `title`, and `summary`
3. update any relationship fields like `project_id`
4. run `python -m personalos validate`
5. run `python -m personalos generate all`

## Optional: Scaffold A Blank Workspace

If you want to create the directory structure somewhere else first:

```bash
python -m personalos init --path C:\\path\\to\\workspace
```

That command creates the standard folders so you can start populating them with your own schema files and entities.
