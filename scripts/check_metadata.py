from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8").lower()


def require_file(path):
    file_path = ROOT / path
    if not file_path.exists():
        raise SystemExit(f"Missing required file: {path}")
    return file_path


def require_text(path, required_terms):
    content = read(path)
    missing = [term for term in required_terms if term not in content]
    if missing:
        raise SystemExit(f"{path} is missing required terms: {', '.join(missing)}")


def main():
    for path in [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "work_division.md",
        "backend/spec.md",
        "apt.txt",
        "packages.txt",
        ".pre-commit-config.yaml",
        ".gitlab-ci.yml",
    ]:
        require_file(path)

    require_text("README.md", ["offline", "cpu", "tesseract", "gpl"])
    require_text("LICENSE", ["gnu general public license", "version 3"])
    require_text("apt.txt", ["tesseract-ocr"])
    require_text("packages.txt", ["tesseract-ocr"])
    require_text("backend/spec.md", ["input", "output", "offline", "cpu"])


if __name__ == "__main__":
    main()
