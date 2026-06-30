# User Manual

## Overview

MedicalExtract AI is an offline-first medical record intelligence app. It helps
users turn typed medical text or prescription images into structured JSON using
local CPU processing.

## Start The App

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start Streamlit:

```bash
streamlit run app.py
```

## Analyze A Record

1. Open the Streamlit URL shown in the terminal.
2. Upload a PNG, JPG, or JPEG medical record image, or use the browser PWA text
   interface from `frontend/index.html`.
3. Review the extracted patient details, medicines, condition summary, and JSON.
4. Compare all extracted text with the original record before using it.

## Offline Use

The core parser runs locally. OCR requires Tesseract to be installed on the
machine. The browser PWA can continue working after first load for text-based
analysis.

## Safety Notice

The output is educational support only. It is not a diagnosis and is not a
substitute for professional medical advice.
