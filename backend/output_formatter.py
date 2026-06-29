def _value(source, key, default):
    if not isinstance(source, dict):
        return default
    value = source.get(key, default)
    return default if value in (None, "") else value


def format_output(processed, result):
    clean_text = _value(processed, "clean_text", "")
    predicted_condition = _value(result, "predicted_condition", "Unknown")
    confidence_score = _value(result, "confidence_score", 0.0)

    return {
        "status": "success",
        "data": {
            "summary": clean_text[:160],
            "word_count": _value(result, "word_count", len(clean_text.split())),
            "prediction": {
                "condition": predicted_condition,
                "confidence_score": confidence_score,
            },
        },
        "meta": {
            "model": "Tesseract OCR + Offline Rule-Based Medical Parser",
            "offline_mode": True,
            "runtime": "CPU",
            "disclaimer": (
                "Educational support only. Not a substitute for professional "
                "medical advice."
            ),
        },
    }
