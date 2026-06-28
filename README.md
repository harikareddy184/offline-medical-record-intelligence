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
- Enter medical text directly
- Parse patient name, provider, date, and common symptoms
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

The repository includes `apt.txt` with `tesseract-ocr`, so Streamlit Cloud
installs the OCR binary during deployment. The app detects the binary from
`PATH`, which works on Linux cloud hosts and local machines.

## Expected JSON Output

```json
{
  "status": "success",
  "data": {
    "input_text": "Prescribed to: Asha Rao",
    "patient_name": "Asha Rao",
    "doctor": "Unknown",
    "date": "Unknown",
    "extracted_entities": ["fever"],
    "medical_analysis": {
      "possible_condition": "General Illness",
      "confidence_score": 0.5
    },
    "recommendation": {
      "severity_level": "low",
      "advice": ["Consult doctor"]
    }
  },
  "meta": {
    "model": "Tesseract OCR + Rule-Based Parser",
    "offline_mode": true,
    "runtime": "CPU"
  }
}
```

## Audit Checks

GitLab CI runs real checks for metadata, compilation, formatting, linting,
typing, tests, security scanning, dependency auditing, and pre-commit hooks.

## License

This project is licensed under GPL-3.0-or-later, a strong copyleft Free and Open
Source Software license.
