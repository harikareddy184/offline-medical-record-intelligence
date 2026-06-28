MedicalExtract AI

Project Overview

MedicalExtract AI is an offline, CPU-first AI application that extracts structured information from medical documents such as prescriptions, lab reports, and discharge summaries. The application uses OCR and local AI models to convert unstructured medical records into structured JSON, which is stored in a local SQLite database.

Problem Statement

Medical records are often stored as paper documents or scanned PDFs, making them difficult to search, organize, and manage. This project provides a privacy-friendly solution by processing documents completely offline without sending any data to cloud services.

Objectives

* Extract information from medical documents.
* Convert unstructured text into structured JSON.
* Store extracted information locally in SQLite.
* Work completely offline.
* Run AI inference using only CPU.

Features

* Upload medical documents (Image/PDF)
* OCR text extraction using Tesseract
* Local AI processing using Ollama
* Structured JSON generation
* SQLite database storage
* Search and retrieve saved medical records
* 100% Offline
* CPU-First AI

Technology Stack

* Python
* FastAPI
* Streamlit
* Tesseract OCR
* Ollama
* SQLite

Workflow

1. Upload Medical Document
2. Extract Text using OCR
3. Process Text using Local AI
4. Generate Structured JSON
5. Store Data in SQLite
6. Search and Retrieve Records

Expected JSON Output

{
  "patient_name": "",
  "doctor_name": "",
  "date": "",
  "medicines": [],
  "diagnosis": ""
}

Future Enhancements

* Support laboratory reports
* Support medical bills
* Support discharge summaries
* Export data to CSV and JSON
* Multi-language support

License

This project will be released under the GNU General Public License v3.0 (GPL-3.0).