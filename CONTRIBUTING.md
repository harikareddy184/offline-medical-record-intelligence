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
streamlit run backend/app.py
```

## Quality Checks

Run these before submitting changes:

```bash
python scripts/check_metadata.py
python -m compileall backend
ruff format --check .
ruff check .
black --check .
mypy backend scripts --ignore-missing-imports
pytest -q
bandit -r backend scripts -ll
pip-audit -r requirements.txt
pre-commit run --all-files
```

## Commit Style

Use semantic commits such as:

- `feat: add image upload OCR`
- `fix: detect tesseract path on cloud`
- `test: cover medical parser output`
- `docs: update offline demo instructions`
