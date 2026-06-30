from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8").lower()


def require_terms(path, terms):
    content = read(path)
    missing = [term for term in terms if term not in content]
    if missing:
        raise SystemExit(f"{path} is missing required terms: {', '.join(missing)}")


def main():
    require_terms(
        "README.md",
        [
            "medicalextract ai",
            "cpu",
            "offline",
            "tesseract",
            "structured json",
            "agpl",
        ],
    )
    require_terms(
        "CONTRIBUTING.md",
        ["quality checks", "semantic commits", "pre-commit", "pytest"],
    )
    require_terms("CHANGELOG.md", ["changelog", "gitlab ci", "audit"])
    require_terms(
        "ISSUES.md",
        ["assignee", "estimate", "due date", "2026-06-28"],
    )
    require_terms(
        "work_division.md",
        ["backend", "frontend", "sama harika reddy", "offline"],
    )
    require_terms(
        "backend/spec.md",
        ["input", "output", "cpu", "offline", "json"],
    )


if __name__ == "__main__":
    main()
