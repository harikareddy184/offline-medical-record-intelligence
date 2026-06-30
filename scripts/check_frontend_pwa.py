from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    required_files = [
        "frontend/index.html",
        "frontend/manifest.webmanifest",
        "frontend/sw.js",
        "frontend/app.js",
        "frontend/style.css",
    ]
    missing = [path for path in required_files if not (ROOT / path).exists()]
    if missing:
        raise SystemExit(f"Missing PWA files: {', '.join(missing)}")
    print("PWA files present")


if __name__ == "__main__":
    main()
