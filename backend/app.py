import re
import shutil

import pytesseract
import streamlit as st
from PIL import Image


def configure_tesseract():
    """Use the system Tesseract binary when it is available on PATH."""
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file)
    return pytesseract.image_to_string(image)


def parse_medical_text(text):
    text_lower = text.lower()
    keywords = ["fever", "cough", "pain", "cold", "headache"]
    found = [word for word in keywords if word in text_lower]

    name_match = re.search(r"prescribed to[:\-]?\s*(.*)", text, re.IGNORECASE)
    patient_name = name_match.group(1).strip() if name_match else "Unknown"

    doctor_match = re.search(r"provider[:\-]?\s*(.*)", text, re.IGNORECASE)
    doctor = doctor_match.group(1).strip() if doctor_match else "Unknown"

    date_match = re.search(r"\d{1,2}/\d{1,2}/\d{2,4}", text)
    date = date_match.group(0) if date_match else "Unknown"

    return {
        "patient_name": patient_name,
        "doctor": doctor,
        "date": date,
        "entities": found,
    }


def build_result(input_text):
    parsed = parse_medical_text(input_text)
    return {
        "status": "success",
        "data": {
            "input_text": input_text.strip(),
            "patient_name": parsed["patient_name"],
            "doctor": parsed["doctor"],
            "date": parsed["date"],
            "extracted_entities": parsed["entities"],
            "medical_analysis": {
                "possible_condition": (
                    "Unknown" if not parsed["entities"] else "General Illness"
                ),
                "confidence_score": 0.5,
            },
            "recommendation": {
                "severity_level": "low",
                "advice": ["Consult doctor"],
            },
        },
        "meta": {
            "model": "Tesseract OCR + Rule-Based Parser",
            "offline_mode": True,
            "runtime": "CPU",
        },
    }


def main():
    configure_tesseract()
    st.set_page_config(page_title="Medical Record Analyzer", layout="wide")

    st.title("Medical Record Analyzer")
    st.write("Extract structured insights from medical records offline on CPU.")

    tab1, tab2 = st.tabs(["Text Input", "Image Upload"])

    with tab1:
        text_data = st.text_area("Enter medical text", height=200)

    with tab2:
        uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    if st.button("Analyze Record"):
        input_text = ""

        if uploaded_file:
            try:
                input_text = extract_text_from_image(uploaded_file)
            except pytesseract.TesseractNotFoundError:
                st.error(
                    "Tesseract OCR is not installed or is not available on PATH. "
                    "On Streamlit Cloud, keep 'tesseract-ocr' in apt.txt and redeploy."
                )
                st.stop()
            except Exception as exc:
                st.error(f"Could not read this image: {exc}")
                st.stop()
        elif text_data:
            input_text = text_data
        else:
            st.warning("Please enter text or upload an image.")
            st.stop()

        result = build_result(input_text)
        st.success("Analysis complete.")
        st.markdown("### Result")
        st.json(result)

        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)


if __name__ == "__main__":
    main()
