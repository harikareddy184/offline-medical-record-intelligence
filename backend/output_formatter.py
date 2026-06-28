def format_output(processed, result):

    return {
        "status": "success",
        "data": {
            "input_text": processed.get("input", ""),
            "extracted_entities": processed.get("entities", []),

            "medical_analysis": {
                "possible_condition": result.get("condition"),
                "confidence_score": result.get("confidence")
            },

            "recommendation": {
                "severity_level": result.get("severity"),
                "advice": result.get("advice")
            }
        },
        "meta": {
            "model": "CPU-Rule-Based-v1",
            "offline_mode": True
        }
    }
       
   