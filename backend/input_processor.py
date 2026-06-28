def process_input(data):
    text = data.get("input", "")

    entities = []
    for word in ["fever", "cough", "cold", "headache"]:
        if word in text.lower():
            entities.append(word)

    return {
        "input": text,
        "entities": entities
    }