# MedicalExtract AI

MedicalExtract AI is a CPU-first, offline Streamlit app that extracts structured
data from medical record text and prescription images.

## Overview

The app is designed for local review of medical documents when privacy and
connectivity matter. It uses Tesseract OCR for images and deterministic Python
rules for medical entity extraction, so the core workflow does not send patient
text, prescriptions, or images to cloud APIs.

Use MedicalExtract AI to:

- Convert typed record text into a structured JSON summary
- Review prescription images with local OCR
- Identify common symptoms, medicine instructions, and missing patient fields
- Produce explainable output that can be checked against the original record

## Problem

Medical records are often stored as paper documents or scanned images. They are
hard to search and risky to send to cloud services. This project processes the
record locally and returns clean JSON that can be saved or copied into another
system.

## Quick Start

1. Install Python 3.12 or newer.
2. Install Tesseract OCR.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Start the app with `streamlit run app.py`.
5. Open the local Streamlit URL and upload a synthetic sample or paste text.

On Debian or Ubuntu, Tesseract can be installed with:

```bash
sudo apt-get install tesseract-ocr
```

## Features

- Upload PNG, JPG, or JPEG medical record images
- Extract text with Tesseract OCR
- Ask about a disease or paste symptoms directly
- Parse patient name, age, gender, provider, date, and common symptoms
- Extract common medicines, dosage, timing, duration, purpose, and simple cautions
- Explain detected conditions in plain language with care guidance and warning signs
- Return structured JSON
- Run on CPU with no GPU or CUDA
- Work offline after dependencies are installed

## Repository Layout

- `app.py` starts the Streamlit interface.
- `backend/app.py` contains the offline parser and JSON response builder.
- `backend/inference.py` connects uploaded images to OCR and parsing.
- `frontend/` contains the static offline browser workflow and PWA assets.
- `scripts/` contains metadata, documentation, and PWA validation checks.
- `tests/` contains focused parser and output contract tests.
- `.gitlab-ci.yml` defines local-runner-friendly compliance and quality jobs.
- `.specify/` and `specs/` hold the spec-driven development templates and
  feature specification.

## Model and Runtime

- OCR model/runtime: Tesseract OCR
- Structured extraction: local rule-based Python parser
- Hardware target: CPU
- Cloud calls: none for the core workflow

## Run Locally

Install Tesseract OCR first. On Debian or Ubuntu:

```bash
sudo apt-get install tesseract-ocr
```

Install Python dependencies and start the app:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The older command, `streamlit run backend/app.py`, also works.

## Privacy and Safety

This project is educational support software. It is not a diagnostic device and
does not replace professional medical advice. Always compare OCR and parser
output with the original document before using it.

Development rules:

- Keep real patient records, names, phone numbers, addresses, images, and
  credentials out of the repository.
- Use synthetic examples in tests, issues, specs, and documentation.
- Preserve offline-first behavior for core medical parsing.
- Prefer deterministic rules unless a task explicitly asks for a model change.

## Streamlit Cloud Deployment

The repository includes `packages.txt` with `tesseract-ocr`, so Streamlit Cloud
installs the OCR binary during deployment. The app detects the binary from
`PATH`, which works on Linux cloud hosts and local machines.

## Phase 2 Submission

This project is submitted as a web application.

- GitLab Pages deployment: created by the `pages` job in `.gitlab-ci.yml`
- GitLab Environment: `production`, created under Operate -> Environments
- Environment URL: provided by GitLab through `$CI_PAGES_URL`
- Public reviewer app: open the `production` environment URL in GitLab
- Offline support: the deployed browser app includes a service worker and web
  manifest, so the text analysis workflow works after the first load without
  network access

The full local Streamlit app supports text input and image OCR. The public
GitLab Pages app provides the core offline text-analysis workflow directly in
the browser, with no API server or cloud calls. This project does not produce a
CLI package, release binary, mobile APK, or mobile release asset.

## Expected JSON Output

```json
{
  "status": "success",
  "data": {
    "record_type": "prescription",
    "input_text": "Prescribed to: Asha Rao",
    "patient": {
      "name": "Asha Rao",
      "age": "Unknown",
      "gender": "Unknown"
    },
    "provider": {
      "doctor": "Unknown",
      "date": "Unknown"
    },
    "date": "Unknown",
    "patient_summary": {
      "record_type": "prescription",
      "identified_patient": "Asha Rao",
      "known_details": ["Name: Asha Rao"],
      "missing_details": ["age", "gender", "doctor", "date"]
    },
    "extracted_entities": ["fever"],
    "medicines": [
      {
        "name": "Paracetamol",
        "dosage": "500mg",
        "frequency": "morning and night",
        "duration": "3 days",
        "purpose": "Used for fever and mild to moderate pain.",
        "simple_explanation": "Helps reduce fever and body pain.",
        "common_cautions": ["do not exceed the prescribed dose"]
      }
    ],
    "disease_information": [
      {
        "name": "Fever",
        "overview": "Fever is a higher than normal body temperature.",
        "common_symptoms": ["high temperature", "chills"],
        "simple_self_care": ["drink fluids", "rest"],
        "care_guidance": ["keep the patient hydrated"],
        "prevention_tips": ["wash hands often"],
        "when_to_seek_medical_help": ["fever is very high"]
      }
    ],
    "medical_analysis": {
      "possible_condition": "Fever",
      "confidence_score": 0.85,
      "condition_summary": {
        "plain_language_summary": "Fever was detected. Fever is a higher than normal body temperature.",
        "detected_conditions": ["Fever"],
        "common_symptoms": ["high temperature", "chills"],
        "care_guidance": ["keep the patient hydrated"],
        "prevention_tips": ["wash hands often"],
        "urgent_warning_signs": ["fever is very high"]
      },
      "medicine_summary": {
        "plain_language_summary": "1 medicine item(s) were detected.",
        "instructions": ["Paracetamol: Helps reduce fever and body pain. Dose: 500mg; timing: morning and night; duration: 3 days."]
      },
      "explanation_for_everyone": "This JSON is generated offline from typed text or OCR."
    },
    "recommendation": {
      "severity_level": "review",
      "care_plan": ["keep the patient hydrated"],
      "urgent_warning_signs": ["fever is very high"],
      "advice": ["Check OCR text against the original prescription."]
    }
  },
  "meta": {
    "model": "Tesseract OCR + Offline Rule-Based Medical Parser",
    "offline_mode": true,
    "runtime": "CPU",
    "disclaimer": "Educational support only. Not a substitute for professional medical advice."
  }
}
```

## Audit Checks

GitLab CI runs separate local-runner-friendly jobs for metadata, compilation,
Ruff formatting, Black formatting, Ruff linting, mypy type checking, pytest,
Bandit security scanning, pip-audit dependency scanning, pre-commit hooks,
Streamlit import validation, and documentation quality checks.

Run the same audit locally:

```bash
python scripts/check_metadata.py
python scripts/check_docs.py
python -m compileall app.py backend scripts tests
ruff format --check .
black --check .
ruff check .
mypy backend scripts --ignore-missing-imports
pytest -q
coverage run -m pytest
coverage report --fail-under=1
coverage xml
bandit -r backend scripts -ll
pip-audit --no-deps --disable-pip --timeout 10 -r requirements.txt
pre-commit run --all-files
```

## Development Workflow

Before opening a merge request:

1. Keep the change scoped to the parser, UI, docs, or CI behavior being updated.
2. Add or update tests when parser behavior or JSON contracts change.
3. Run the focused checks listed above.
4. Update `CHANGELOG.md`, specs, or user docs when behavior changes.
5. Confirm no real patient data or secrets are included.

## License

This project is licensed under AGPL-3.0-or-later, a strong copyleft Free and Open
Source Software license for software that may be accessed over a network.
