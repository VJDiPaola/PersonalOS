# Contributing to PersonalOS

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/PersonalOS.git
cd PersonalOS
pip install -e .
pip install pytest pre-commit
pre-commit install
```

## Adding an Entity

```bash
personalos new project "Your Project Name"
```

Edit the generated file in `entities/`, then validate:

```bash
personalos validate
```

## Running Tests

```bash
pytest tests/ -v
```

## Updating Golden Files

If you intentionally changed generator output:

```bash
pytest tests/test_golden.py --update-goldens
```

## Regenerating Views and Exports

```bash
personalos generate all
```

Always commit the regenerated `views/` and `exports/` output alongside your entity changes.

## Public-Safe Data Rules

This is a public starter repo. **Never** add:

- Real personal contacts
- Real job applications
- Financial or strategy details
- Secrets or `.env` values

**Always** use synthetic, believable sample data.

## Code Quality

- Run `personalos check` before submitting a PR
- Ensure all tests pass
- Keep generated output in sync with source entities
