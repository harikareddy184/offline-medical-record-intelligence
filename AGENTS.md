# Agents Guide

## Project Context

This repository contains an offline, CPU-first medical record intelligence app.
Agents should preserve the local-first design and avoid adding cloud calls for
core medical parsing.

## Development Rules

- Keep patient data local and avoid committing examples with real personal data.
- Prefer deterministic rule-based parsing unless a task explicitly asks for a
  model change.
- Run focused checks before committing CI, parser, or documentation updates.
- Keep GitLab CI compatible with the Windows PowerShell shell runner tagged
  `medical analyzer`.

## Useful Checks

```bash
python -m compileall app.py backend scripts tests
python scripts/check_frontend_pwa.py
pytest -q
ruff check .
mypy backend scripts --ignore-missing-imports
bandit -r backend scripts -ll
```
