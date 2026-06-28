def run_inference(processed):
    text = processed.get("input", "").lower()

    if "fever" in text and "cough" in text:
        return {
            "condition": "Flu",
            "confidence": 0.92,
            "severity": "mild",
            "advice": [
                "Take rest",
                "Drink fluids",
                "Monitor temperature"
            ]
        }

    return {
        "condition": "Unknown",
        "confidence": 0.50,
        "severity": "low",
        "advice": ["Consult doctor"]
    }