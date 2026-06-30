# Offline Medical Record Intelligence Specification

## Goal

Provide an offline, CPU-first workflow that converts medical record text and
prescription images into structured JSON for review.

## Functional Requirements

- Accept typed medical text and supported image uploads.
- Extract patient, provider, date, condition, medicine, dose, frequency, and
  duration fields when present.
- Return a stable JSON response with `status`, `data`, and `meta` sections.
- Include a medical disclaimer in every generated result.

## Non-Functional Requirements

- Core analysis must not require cloud APIs.
- Runtime must support CPU-only environments.
- Documentation must explain local setup, safety limits, and validation steps.
