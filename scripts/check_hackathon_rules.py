import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def read(path):
    return (ROOT / path).read_text(encoding="utf-8").lower()


def fail(message):
    raise SystemExit(message)


def check_cpu_first():
    readme = read("README.md")
    app = read("backend/app.py")
    forbidden_terms = ["cuda", "gpu runtime", "torch.cuda", "tensorflow-gpu"]
    found = [term for term in forbidden_terms if term in app]
    if found:
        fail(f"CPU-first check failed. Forbidden GPU terms found: {', '.join(found)}")
    required_terms = ["cpu", "tesseract", "offline"]
    missing = [term for term in required_terms if term not in readme]
    if missing:
        fail(f"CPU-first check failed. README missing: {', '.join(missing)}")


def check_offline_first():
    source_files = list((ROOT / "backend").rglob("*.py")) + [ROOT / "app.py"]
    forbidden_terms = [
        "openai",
        "requests.",
        "httpx.",
        "urllib.request",
        "api_key",
    ]
    violations = []
    for path in source_files:
        content = path.read_text(encoding="utf-8").lower()
        for term in forbidden_terms:
            if term in content:
                violations.append(f"{path.relative_to(ROOT)}:{term}")
    if violations:
        fail("Offline-first check failed: " + ", ".join(violations))


def check_strong_copyleft_license():
    license_text = read("LICENSE")
    if (
        "gnu affero general public license" not in license_text
        or "version 3" not in license_text
    ):
        fail("License check failed. LICENSE must be AGPL-3.0 strong copyleft.")


def check_system_packages():
    apt_text = read("apt.txt")
    packages_text = read("packages.txt")
    if "tesseract-ocr" not in apt_text or "tesseract-ocr" not in packages_text:
        fail(
            "System package check failed. "
            "tesseract-ocr must be in apt.txt and packages.txt."
        )


def check_real_parser_output():
    from backend.app import build_result

    result = build_result(
        "Patient Name: Asha Rao\n"
        "Age: 34\n"
        "Doctor: Dr Kumar\n"
        "Tab Paracetamol 500mg 1-0-1 for 3 days\n"
        "Symptoms: fever"
    )
    data = result["data"]
    if result["status"] != "success":
        fail("Parser output check failed. Status was not success.")
    if data["patient"]["name"] != "Asha Rao":
        fail("Parser output check failed. Patient name was not extracted.")
    if not data["medicines"]:
        fail("Parser output check failed. Medicine list was empty.")
    if data["medical_analysis"]["possible_condition"] != "Fever":
        fail("Parser output check failed. Fever condition was not detected.")


def main():
    checks = {
        "cpu_first": check_cpu_first,
        "offline_first": check_offline_first,
        "strong_copyleft_license": check_strong_copyleft_license,
        "system_packages": check_system_packages,
        "real_parser_output": check_real_parser_output,
    }

    for name, check in checks.items():
        check()
        print(f"{name}: passed")


if __name__ == "__main__":
    main()
