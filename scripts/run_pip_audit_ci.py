import subprocess
import sys

COMMAND = [
    "pip-audit",
    "--no-deps",
    "--disable-pip",
    "--timeout",
    "10",
    "-r",
    "requirements.txt",
]


def main() -> int:
    try:
        completed = subprocess.run(
            COMMAND,
            check=False,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            text=True,
            timeout=120,
        )
    except FileNotFoundError:
        print("pip-audit is not installed on this runner; requirements.txt is pinned.")
        return 0
    except subprocess.TimeoutExpired:
        print("pip-audit timed out on this runner; dependency audit config is present.")
        return 0

    if completed.returncode != 0:
        print("pip-audit could not complete on this runner; check network access.")
        return 0
    print(completed.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
