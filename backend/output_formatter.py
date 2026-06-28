def format_output(processed, result):
    return {
        "Summary": processed["clean_text"][:100],
        "Word Count": result["word_count"],
        "Prediction": result["predicted_condition"],
    }
