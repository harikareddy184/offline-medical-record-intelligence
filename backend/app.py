import streamlit as st
import pytesseract
from PIL import Image
import json
import re
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Medical Record Analyzer", layout="wide")

# ---------------- OCR FUNCTION ----------------
def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file)
    text = pytesseract.image_to_string(image)
    return text

# ---------------- SIMPLE PARSER ----------------
def parse_medical_text(text):
    text_lower = text.lower()

    # Extract simple entities
    keywords = ["fever", "cough", "pain", "cold", "headache"]
    found = [word for word in keywords if word in text_lower]

    # Try extracting name (very basic)
    name_match = re.search(r"prescribed to[:\-]?\s*(.*)", text, re.IGNORECASE)
    patient_name = name_match.group(1).strip() if name_match else "Unknown"

    # Try extracting doctor
    doctor_match = re.search(r"provider[:\-]?\s*(.*)", text, re.IGNORECASE)
    doctor = doctor_match.group(1).strip() if doctor_match else "Unknown"

    # Try extracting date
    date_match = re.search(r"\d{1,2}/\d{1,2}/\d{2,4}", text)
    date = date_match.group(0) if date_match else "Unknown"

    return {
        "patient_name": patient_name,
        "doctor": doctor,
        "date": date,
        "entities": found
    }

# ---------------- UI ----------------
st.title("📋 Medical Record Analyzer")
st.write("Extract structured insights from medical records (offline)")

tab1, tab2 = st.tabs(["📝 Text Input", "📁 Image Upload"])

text_data = ""
uploaded_file = None

# -------- TEXT TAB --------
with tab1:
    text_data = st.text_area("Enter medical text", height=200)

# -------- IMAGE TAB --------
with tab2:
    uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

# -------- BUTTON --------
if st.button("✨ Analyze Record"):

    input_text = ""

    # IMAGE → OCR
    if uploaded_file:
        input_text = extract_text_from_image(uploaded_file)

    # TEXT INPUT
    elif text_data:
        input_text = text_data

    else:
        st.warning("Please enter text or upload image")
        st.stop()

    # -------- PARSE --------
    parsed = parse_medical_text(input_text)

    # -------- FINAL JSON --------
    result = {
        "status": "success",
        "data": {
            "input_text": input_text.strip(),
            "patient_name": parsed["patient_name"],
            "doctor": parsed["doctor"],
            "date": parsed["date"],
            "extracted_entities": parsed["entities"],
            "medical_analysis": {
                "possible_condition": "Unknown" if not parsed["entities"] else "General Illness",
                "confidence_score": 0.5
            },
            "recommendation": {
                "severity_level": "low",
                "advice": ["Consult doctor"]
            }
        },
        "meta": {
            "model": "OCR-Rule-Based-v1",
            "offline_mode": True
        }
    }

    # -------- OUTPUT --------
    st.success("✅ Analysis Complete!")
    st.markdown("### 📊 Result")

    st.json(result)

    # -------- SHOW IMAGE --------
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)