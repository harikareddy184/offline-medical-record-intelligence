# Contributing

## Development Setup

1. Install Python 3.12 or newer.
2. Install Tesseract OCR.
3. Install Python dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install black ruff mypy pytest bandit pip-audit pre-commit
```

4. Run the app:

```bash
streamlit run app.py
```

## Quality Checks

Run these before submitting changes:

```bash
python scripts/check_metadata.py
python scripts/check_docs.py
python -m compileall app.py backend scripts tests
ruff format --check .
black --check .
ruff check .
mypy backend scripts --ignore-missing-imports
pytest -q
bandit -r backend scripts -ll
pip-audit --no-deps --disable-pip --timeout 10 -r requirements.txt
pre-commit run --all-files
```

The GitLab pipeline exposes these as separate jobs so every formatting, lint,
type-check, test, security, dependency, hook, package, and docs check is visible
on the runner.

## Commit Style

Use semantic commits such as:

- `feat: add image upload OCR`
- `fix: detect tesseract path on cloud`
- `test: cover medical parser output`
- `docs: update offline demo instructions`
