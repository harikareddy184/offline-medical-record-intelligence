import re
import shutil
from pathlib import Path

import pytesseract
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps

DISEASE_KNOWLEDGE = {
    "fever": {
        "overview": (
            "Fever is a higher than normal body temperature, usually caused by "
            "infection or inflammation."
        ),
        "common_symptoms": ["high temperature", "chills", "body pain", "tiredness"],
        "self_care": ["drink fluids", "rest", "monitor temperature"],
        "care_guidance": [
            "keep the patient hydrated",
            "use fever medicine only as prescribed",
            "recheck temperature regularly",
        ],
        "prevention": ["wash hands often", "avoid close contact during infections"],
        "seek_help_if": [
            "fever is very high",
            "breathing is difficult",
            "symptoms last more than 3 days",
        ],
    },
    "cough": {
        "overview": (
            "Cough is a reflex that clears the throat or lungs and can happen "
            "with colds, allergy, asthma, or infection."
        ),
        "common_symptoms": ["throat irritation", "mucus", "chest discomfort"],
        "self_care": ["drink warm fluids", "avoid smoke and dust", "rest"],
        "care_guidance": [
            "stay away from smoke, dust, and strong smells",
            "drink warm fluids if comfortable",
            "take prescribed cough or allergy medicine only as directed",
        ],
        "prevention": ["cover coughs", "wash hands often", "avoid known allergens"],
        "seek_help_if": [
            "cough lasts more than 2 weeks",
            "blood appears",
            "breathing is difficult",
        ],
    },
    "cold": {
        "overview": "Common cold is a mild viral infection of the nose and throat.",
        "common_symptoms": ["runny nose", "sneezing", "sore throat", "mild cough"],
        "self_care": ["rest", "drink fluids", "use steam inhalation if comfortable"],
        "care_guidance": [
            "rest and drink enough fluids",
            "use prescribed symptom medicines only as directed",
            "avoid unnecessary antibiotics unless a doctor prescribes them",
        ],
        "prevention": ["wash hands often", "avoid sharing cups or towels"],
        "seek_help_if": [
            "high fever occurs",
            "symptoms worsen",
            "breathing becomes difficult",
        ],
    },
    "headache": {
        "overview": (
            "Headache is pain in the head or face and may be caused by stress, "
            "dehydration, fever, migraine, or other conditions."
        ),
        "common_symptoms": ["head pain", "light sensitivity", "nausea"],
        "self_care": ["drink water", "rest in a quiet place", "avoid skipped meals"],
        "care_guidance": [
            "drink water and eat on time",
            "rest away from bright light and loud noise",
            "take pain medicine only as prescribed",
        ],
        "prevention": ["sleep regularly", "manage stress", "avoid known triggers"],
        "seek_help_if": [
            "pain is sudden and severe",
            "vision changes",
            "weakness or confusion occurs",
        ],
    },
    "diabetes": {
        "overview": (
            "Diabetes is a long-term condition where blood sugar stays higher "
            "than normal."
        ),
        "common_symptoms": [
            "frequent urination",
            "increased thirst",
            "tiredness",
            "slow wound healing",
        ],
        "self_care": [
            "follow diet plan",
            "take medicines as prescribed",
            "monitor blood sugar",
        ],
        "care_guidance": [
            "follow the diet and medicine plan from the doctor",
            "check blood sugar as advised",
            "keep regular follow-up visits",
        ],
        "prevention": [
            "choose balanced meals",
            "stay physically active as advised",
            "maintain a healthy weight",
        ],
        "seek_help_if": [
            "blood sugar is very high or low",
            "vomiting occurs",
            "confusion or fainting occurs",
        ],
    },
    "hypertension": {
        "overview": (
            "Hypertension means high blood pressure, which can increase risk "
            "to the heart, brain, and kidneys."
        ),
        "common_symptoms": ["often no symptoms", "headache", "dizziness"],
        "self_care": [
            "reduce salt",
            "take medicines regularly",
            "check blood pressure",
        ],
        "care_guidance": [
            "take blood pressure medicine at the same time each day",
            "reduce salt if advised",
            "record blood pressure readings for follow-up",
        ],
        "prevention": [
            "limit salt",
            "stay active as advised",
            "avoid tobacco and excess alcohol",
        ],
        "seek_help_if": [
            "chest pain occurs",
            "severe headache occurs",
            "blood pressure is very high",
        ],
    },
}

MEDICINE_KNOWLEDGE = {
    "paracetamol": {
        "use": "Used for fever and mild to moderate pain.",
        "simple_explanation": "Helps reduce fever and body pain.",
        "common_cautions": [
            "do not exceed the prescribed dose",
            "avoid combining with other paracetamol products",
        ],
    },
    "acetaminophen": {
        "use": "Used for fever and mild to moderate pain.",
        "simple_explanation": (
            "Another name for paracetamol; helps reduce fever and pain."
        ),
        "common_cautions": [
            "do not exceed the prescribed dose",
            "avoid combining with other acetaminophen products",
        ],
    },
    "ibuprofen": {
        "use": "Used for pain, fever, and inflammation.",
        "simple_explanation": "Helps with swelling, pain, and fever.",
        "common_cautions": [
            "take with food if advised",
            "avoid if a doctor told you to avoid NSAIDs",
        ],
    },
    "amoxicillin": {
        "use": "Antibiotic used for some bacterial infections.",
        "simple_explanation": "Helps fight certain bacterial infections.",
        "common_cautions": [
            "complete the full course",
            "do not use for viral cold unless prescribed",
        ],
    },
    "azithromycin": {
        "use": "Antibiotic used for some bacterial infections.",
        "simple_explanation": "Helps fight certain bacterial infections.",
        "common_cautions": ["take exactly as prescribed", "do not skip doses"],
    },
    "cetirizine": {
        "use": "Used for allergy symptoms such as sneezing, runny nose, or itching.",
        "simple_explanation": "Helps reduce allergy symptoms.",
        "common_cautions": ["may cause sleepiness", "avoid driving if drowsy"],
    },
    "metformin": {
        "use": "Used to help control blood sugar in type 2 diabetes.",
        "simple_explanation": "Helps the body manage sugar levels.",
        "common_cautions": [
            "take with meals if advised",
            "follow blood sugar monitoring advice",
        ],
    },
    "amlodipine": {
        "use": "Used to treat high blood pressure.",
        "simple_explanation": "Helps relax blood vessels and lower blood pressure.",
        "common_cautions": [
            "take regularly",
            "do not stop suddenly without medical advice",
        ],
    },
}

FREQUENCY_PATTERNS = [
    (r"\b1-0-1\b", "morning and night"),
    (r"\b1-1-1\b", "morning, afternoon, and night"),
    (r"\b1-0-0\b", "morning only"),
    (r"\b0-0-1\b", "night only"),
    (r"\bod\b", "once daily"),
    (r"\bbd\b|\bbid\b", "twice daily"),
    (r"\btds\b|\btid\b", "three times daily"),
    (r"\bhs\b", "at bedtime"),
    (r"\bsos\b|\bprn\b", "only when needed"),
]


def configure_tesseract():
    """Use the system Tesseract binary when it is available on PATH."""
    common_paths = [
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    ]
    tesseract_path = shutil.which("tesseract")
    if not tesseract_path:
        tesseract_path = next(
            (path for path in common_paths if Path(path).exists()),
            None,
        )
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file)
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    image = ImageEnhance.Sharpness(image).enhance(1.8)
    return pytesseract.image_to_string(image, config="--psm 6")


def clean_lines(text):
    return [line.strip(" :-\t") for line in text.splitlines() if line.strip()]


def first_match(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip(" :-\t")
    return "Unknown"


def detect_record_type(text):
    text_lower = text.lower()
    if any(
        word in text_lower
        for word in ["tablet", "tab", "capsule", "cap", "syrup", "rx", "prescription"]
    ):
        return "prescription"
    if any(
        word in text_lower
        for word in ["what is", "tell me about", "disease", "symptoms of"]
    ):
        return "disease_question"
    return "medical_text"


def extract_patient_details(text):
    return {
        "name": first_match(
            text,
            [
                (
                    r"(?:patient\s*name|patient|name|prescribed\s*to)\s*"
                    r"[:\-]\s*([A-Za-z .]+)"
                ),
                r"(?:mr|mrs|ms|miss)\.?\s+([A-Za-z .]+)",
            ],
        ),
        "age": first_match(text, [r"(?:age)\s*[:\-]?\s*(\d{1,3})\b"]),
        "gender": first_match(
            text, [r"(?:sex|gender)\s*[:\-]?\s*(male|female|other|m|f)\b"]
        ),
    }


def extract_provider_details(text):
    return {
        "doctor": first_match(
            text,
            [
                r"(?:provider|doctor|dr\.?)\s*[:\-]?\s*([A-Za-z .]+)",
                r"(Dr\.?\s+[A-Za-z .]+)",
            ],
        ),
        "date": first_match(
            text,
            [
                r"(?:date)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
                r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
            ],
        ),
    }


def extract_conditions(text):
    text_lower = text.lower()
    return [name for name in DISEASE_KNOWLEDGE if re.search(rf"\b{name}\b", text_lower)]


def extract_frequency(line):
    line_lower = line.lower()
    for pattern, meaning in FREQUENCY_PATTERNS:
        if re.search(pattern, line_lower):
            return meaning
    return "not clearly mentioned"


def extract_duration(line):
    match = re.search(
        r"\b(?:for\s*)?(\d+\s*(?:day|days|week|weeks|month|months))\b",
        line,
        re.IGNORECASE,
    )
    return match.group(1) if match else "not clearly mentioned"


def extract_dosage(line):
    match = re.search(r"\b(\d+(?:\.\d+)?\s*(?:mg|ml|mcg|g))\b", line, re.IGNORECASE)
    return match.group(1) if match else "not clearly mentioned"


def extract_medicines(text):
    medicines = []
    seen = set()
    lines = clean_lines(text)
    medicine_names = "|".join(re.escape(name) for name in MEDICINE_KNOWLEDGE)
    fallback_pattern = re.compile(
        r"\b(?:tab|tablet|cap|capsule|syrup)\.?\s+([A-Za-z][A-Za-z0-9-]+)",
        re.IGNORECASE,
    )

    for line in lines:
        known_matches = re.findall(rf"\b({medicine_names})\b", line, re.IGNORECASE)
        fallback_matches = fallback_pattern.findall(line)
        for raw_name in [*known_matches, *fallback_matches]:
            normalized = raw_name.lower()
            if normalized in seen:
                continue
            seen.add(normalized)
            info = MEDICINE_KNOWLEDGE.get(normalized, {})
            medicines.append(
                {
                    "name": raw_name.title(),
                    "dosage": extract_dosage(line),
                    "frequency": extract_frequency(line),
                    "duration": extract_duration(line),
                    "purpose": info.get(
                        "use",
                        "Purpose is not available in the offline medicine database.",
                    ),
                    "simple_explanation": info.get(
                        "simple_explanation",
                        (
                            "Medicine detected from the prescription text. "
                            "Confirm details with a doctor or pharmacist."
                        ),
                    ),
                    "common_cautions": info.get(
                        "common_cautions",
                        [
                            "use only as prescribed",
                            "confirm unclear OCR text with a doctor or pharmacist",
                        ],
                    ),
                    "source_line": line,
                }
            )
    return medicines


def build_disease_info(conditions):
    disease_info = []
    for condition in conditions:
        info = DISEASE_KNOWLEDGE[condition]
        disease_info.append(
            {
                "name": condition.title(),
                "overview": info["overview"],
                "common_symptoms": info["common_symptoms"],
                "simple_self_care": info["self_care"],
                "care_guidance": info["care_guidance"],
                "prevention_tips": info["prevention"],
                "when_to_seek_medical_help": info["seek_help_if"],
            }
        )
    return disease_info


def build_patient_summary(patient, provider, record_type):
    known_details = []
    for label, value in [
        ("Name", patient["name"]),
        ("Age", patient["age"]),
        ("Gender", patient["gender"]),
        ("Doctor", provider["doctor"]),
        ("Date", provider["date"]),
    ]:
        if value != "Unknown":
            known_details.append(f"{label}: {value}")

    if not known_details:
        known_details.append("No clear patient identity details found in the text.")

    return {
        "record_type": record_type,
        "identified_patient": patient["name"],
        "known_details": known_details,
        "missing_details": [
            label
            for label, value in [
                ("name", patient["name"]),
                ("age", patient["age"]),
                ("gender", patient["gender"]),
                ("doctor", provider["doctor"]),
                ("date", provider["date"]),
            ]
            if value == "Unknown"
        ],
    }


def build_condition_summary(disease_info):
    if not disease_info:
        return {
            "plain_language_summary": (
                "No supported disease name was clearly detected. Review the OCR text "
                "or enter symptoms such as fever, cough, cold, headache, diabetes, "
                "or hypertension."
            ),
            "detected_conditions": [],
            "care_guidance": [
                "confirm the readable text with the original document",
                "consult a qualified clinician for diagnosis and treatment",
            ],
            "urgent_warning_signs": [
                "breathing difficulty",
                "chest pain",
                "confusion or fainting",
                "severe or rapidly worsening symptoms",
            ],
        }

    primary = disease_info[0]
    return {
        "plain_language_summary": (
            f"{primary['name']} was detected. {primary['overview']} "
            "The guidance below is general education, not a confirmed diagnosis."
        ),
        "detected_conditions": [condition["name"] for condition in disease_info],
        "common_symptoms": primary["common_symptoms"],
        "care_guidance": primary["care_guidance"],
        "prevention_tips": primary["prevention_tips"],
        "urgent_warning_signs": primary["when_to_seek_medical_help"],
    }


def build_medicine_summary(medicines):
    if not medicines:
        return {
            "plain_language_summary": "No medicine name was clearly detected.",
            "instructions": [
                "check the prescription image or typed text for medicine names",
                "ask a doctor or pharmacist before taking unclear medicines",
            ],
        }

    return {
        "plain_language_summary": (
            f"{len(medicines)} medicine item(s) were detected. Verify each dose, "
            "timing, and duration against the original prescription."
        ),
        "instructions": [
            (
                f"{medicine['name']}: {medicine['simple_explanation']} "
                f"Dose: {medicine['dosage']}; timing: {medicine['frequency']}; "
                f"duration: {medicine['duration']}."
            )
            for medicine in medicines
        ],
    }


def parse_medical_text(text):
    conditions = extract_conditions(text)
    medicines = extract_medicines(text)
    provider = extract_provider_details(text)
    patient = extract_patient_details(text)
    record_type = detect_record_type(text)
    disease_info = build_disease_info(conditions)

    return {
        "record_type": record_type,
        "patient": patient,
        "provider": provider,
        "date": provider["date"],
        "entities": conditions,
        "medicines": medicines,
        "disease_info": disease_info,
        "patient_summary": build_patient_summary(patient, provider, record_type),
        "condition_summary": build_condition_summary(disease_info),
        "medicine_summary": build_medicine_summary(medicines),
    }


def confidence_score(parsed):
    score = 0.35
    if parsed["patient"]["name"] != "Unknown":
        score += 0.15
    if parsed["provider"]["doctor"] != "Unknown":
        score += 0.15
    if parsed["medicines"]:
        score += 0.2
    if parsed["disease_info"]:
        score += 0.15
    return min(round(score, 2), 0.95)


def build_result(input_text):
    parsed = parse_medical_text(input_text)
    confidence = confidence_score(parsed)
    possible_condition = (
        parsed["disease_info"][0]["name"] if parsed["disease_info"] else "Unknown"
    )
    return {
        "status": "success",
        "data": {
            "record_type": parsed["record_type"],
            "input_text": input_text.strip(),
            "patient": parsed["patient"],
            "provider": parsed["provider"],
            "date": parsed["date"],
            "patient_summary": parsed["patient_summary"],
            "extracted_entities": parsed["entities"],
            "medicines": parsed["medicines"],
            "disease_information": parsed["disease_info"],
            "medical_analysis": {
                "possible_condition": possible_condition,
                "confidence_score": confidence,
                "condition_summary": parsed["condition_summary"],
                "medicine_summary": parsed["medicine_summary"],
                "explanation_for_everyone": (
                    "This JSON is generated offline from typed text or OCR. "
                    "Use it to understand the record, not as a final diagnosis."
                ),
            },
            "recommendation": {
                "severity_level": "unknown" if not parsed["disease_info"] else "review",
                "care_plan": parsed["condition_summary"]["care_guidance"],
                "urgent_warning_signs": parsed["condition_summary"][
                    "urgent_warning_signs"
                ],
                "advice": [
                    "Check OCR text against the original prescription.",
                    "Follow the doctor's prescription exactly.",
                    (
                        "Ask a doctor or pharmacist if medicine name, dose, "
                        "or timing is unclear."
                    ),
                ],
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


def main():
    configure_tesseract()
    st.set_page_config(page_title="Medical Record Analyzer", layout="wide")

    st.title("Medical Record Analyzer")
    st.write("Extract structured insights from medical records offline on CPU.")

    tab1, tab2 = st.tabs(["Text Input", "Image Upload"])

    with tab1:
        text_data = st.text_area(
            "Enter a disease question, symptoms, or prescription text",
            height=200,
            placeholder="Example: What is fever? Or paste prescription text here.",
        )

    with tab2:
        uploaded_file = st.file_uploader(
            "Upload prescription image", type=["png", "jpg", "jpeg"]
        )

    if st.button("Analyze Record"):
        input_text = ""

        if uploaded_file:
            try:
                input_text = extract_text_from_image(uploaded_file)
            except pytesseract.TesseractNotFoundError:
                st.error(
                    "Tesseract OCR is not installed or is not available on PATH. "
                    "On Streamlit Cloud, keep 'tesseract-ocr' in packages.txt "
                    "and redeploy."
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

        if not input_text.strip():
            st.warning("No readable text was found. Try a clearer prescription image.")
            st.stop()

        result = build_result(input_text)
        st.success("Analysis complete.")
        st.markdown("### Result")
        st.json(result)

        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)


if __name__ == "__main__":
    main()
