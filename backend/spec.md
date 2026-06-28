# Spec Kit

## Project Idea

MedicalExtract AI is a CPU-first, offline web app that converts unstructured
medical record text and scanned prescription images into structured JSON.

## Problem

Paper prescriptions and scanned medical records are hard to search, organize,
and reuse. Cloud OCR or remote AI APIs can expose private health data and fail
when the network is unavailable.

## Inputs

- Typed medical text
- PNG, JPG, or JPEG medical record images

## Output

The app returns structured JSON containing:

- Raw extracted text
- Patient name
- Doctor or provider
- Date
- Extracted symptoms or entities
- Basic medical analysis
- Recommendation metadata

## CPU Runtime

- OCR engine: Tesseract OCR
- Parser: local rule-based Python parser
- Runtime: CPU only
- GPU/CUDA: not required

## Offline Mode

Core processing runs locally with no external API calls. After dependencies are
installed, the app can process text and images with Wi-Fi turned off.

## System Flow

Input -> OCR or text capture -> local parser -> structured JSON -> display
