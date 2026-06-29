from backend.app import build_result, parse_medical_text
from backend.output_formatter import format_output


def test_parse_medical_text_extracts_prescription_fields():
    text = (
        "Patient Name: Asha Rao\n"
        "Age: 34\n"
        "Gender: Female\n"
        "Doctor: Dr Kumar\n"
        "Date: 12/05/2026\n"
        "Tab Paracetamol 500mg 1-0-1 for 3 days\n"
        "Symptoms: fever and headache"
    )

    parsed = parse_medical_text(text)

    assert parsed["record_type"] == "prescription"
    assert parsed["patient"]["name"] == "Asha Rao"
    assert parsed["patient"]["age"] == "34"
    assert parsed["provider"]["doctor"] == "Dr Kumar"
    assert parsed["date"] == "12/05/2026"
    assert parsed["entities"] == ["fever", "headache"]
    assert parsed["patient_summary"]["identified_patient"] == "Asha Rao"
    assert "Name: Asha Rao" in parsed["patient_summary"]["known_details"]
    assert parsed["medicines"][0]["name"] == "Paracetamol"
    assert parsed["medicines"][0]["dosage"] == "500mg"
    assert parsed["medicines"][0]["frequency"] == "morning and night"
    assert parsed["condition_summary"]["detected_conditions"] == ["Fever", "Headache"]
    assert "keep the patient hydrated" in parsed["condition_summary"]["care_guidance"]


def test_build_result_returns_disease_json_for_question():
    result = build_result("What is diabetes and what are symptoms of diabetes?")

    assert result["status"] == "success"
    assert result["data"]["record_type"] == "disease_question"
    assert result["data"]["medical_analysis"]["possible_condition"] == "Diabetes"
    assert result["data"]["disease_information"][0]["name"] == "Diabetes"
    assert result["data"]["medical_analysis"]["condition_summary"][
        "plain_language_summary"
    ].startswith("Diabetes was detected")
    assert "care_plan" in result["data"]["recommendation"]
    assert result["meta"]["offline_mode"] is True
    assert result["meta"]["runtime"] == "CPU"


def test_build_result_declares_offline_cpu_runtime():
    result = build_result("Patient has cough")

    assert result["status"] == "success"
    assert result["meta"]["offline_mode"] is True
    assert result["meta"]["runtime"] == "CPU"
    assert result["data"]["medical_analysis"]["possible_condition"] == "Cough"


def test_format_output_returns_consistent_json_contract():
    formatted = format_output(
        {"clean_text": "Patient has fever and headache."},
        {
            "word_count": 5,
            "predicted_condition": "Fever",
            "confidence_score": 0.9,
        },
    )

    assert formatted["status"] == "success"
    assert formatted["data"]["summary"] == "Patient has fever and headache."
    assert formatted["data"]["word_count"] == 5
    assert formatted["data"]["prediction"]["condition"] == "Fever"
    assert formatted["meta"]["offline_mode"] is True
    assert formatted["meta"]["runtime"] == "CPU"
