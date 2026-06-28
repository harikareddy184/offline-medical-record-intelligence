# MedicalExtract AI

MedicalExtract AI is a CPU-first, offline Streamlit app that extracts structured
data from medical record text and prescription images.

## Problem

Medical records are often stored as paper documents or scanned images. They are
hard to search and risky to send to cloud services. This project processes the
record locally and returns clean JSON that can be saved or copied into another
system.

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
streamlit run backend/app.py
```

## Streamlit Cloud Deployment

The repository includes `packages.txt` with `tesseract-ocr`, so Streamlit Cloud
installs the OCR binary during deployment. The app detects the binary from
`PATH`, which works on Linux cloud hosts and local machines.

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
python -m compileall backend
ruff format --check .
black --check .
ruff check .
mypy backend scripts --ignore-missing-imports
pytest -q
bandit -r backend scripts -ll
pip-audit --no-deps --disable-pip --timeout 10 -r requirements.txt
pre-commit run --all-files
```

## License

This project is licensed under GPL-3.0-or-later, a strong copyleft Free and Open
Source Software license.
