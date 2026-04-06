# Contributing

Thanks for helping improve PersonalOS.

## Contribution Standard

This repo should feel like a professional public starter, not a cleaned-up private vault.

Good changes make the repo:

- easier to understand
- easier to clone
- safer to publish
- more deterministic
- more reusable

## Guardrails

- never add real personal contacts or job applications
- never add secrets, tokens, or `.env` values
- never add private strategy notes or internal-only links
- prefer believable synthetic sample data over vague filler

## Typical Workflow

```bash
python -m pip install -e .[dev]
python -m personalos validate
python -m personalos generate all
pytest
```

If you change the sample entities or generator logic, update the committed outputs in:

- `views/`
- `exports/`
- `tests/golden/`

## Scope Guidance

The current starter intentionally ships a thin vertical slice:

- `projects`
- `tasks`
- `decisions`

Please prefer finishing that end-to-end experience before adding broader surface area.
