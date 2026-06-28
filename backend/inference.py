def run_inference(data):
    text = data["clean_text"]

    # Simple offline logic
    word_count = len(text.split())

    if "fever" in text:
        condition = "Possible Fever"
    elif "cough" in text:
        condition = "Possible Cold"
    else:
        condition = "General Checkup"

    return {
        "word_count": word_count,
        "predicted_condition": condition
    }