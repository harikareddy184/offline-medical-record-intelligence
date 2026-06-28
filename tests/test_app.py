from backend.app import build_result, parse_medical_text


def test_parse_medical_text_extracts_basic_fields():
    text = (
        "Prescribed to: Asha Rao\n"
        "Provider: Dr Kumar\n"
        "Date: 12/05/2026\n"
        "Symptoms: fever and headache"
    )

    parsed = parse_medical_text(text)

    assert parsed["patient_name"] == "Asha Rao"
    assert parsed["doctor"] == "Dr Kumar"
    assert parsed["date"] == "12/05/2026"
    assert parsed["entities"] == ["fever", "headache"]


def test_build_result_declares_offline_cpu_runtime():
    result = build_result("Patient has cough")

    assert result["status"] == "success"
    assert result["meta"]["offline_mode"] is True
    assert result["meta"]["runtime"] == "CPU"
    assert result["data"]["medical_analysis"]["possible_condition"] == "General Illness"
