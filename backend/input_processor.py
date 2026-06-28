def process_input(data):
    text = data.get("input", "")
    
    return {
        "original_text": text,
        "clean_text": text.lower().strip()
    }