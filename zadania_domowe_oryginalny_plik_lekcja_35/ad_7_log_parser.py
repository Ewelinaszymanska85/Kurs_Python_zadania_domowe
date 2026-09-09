import re
from collections import Counter
from pathlib import Path


LOG_LEVELS = ("ERROR", "WARNING", "INFO")
LOG_PATTERN = re.compile(r"^\[.*?\]\s*(ERROR|WARNING|INFO)\b")


def parse_log_file(file_path: str) -> dict[str, int]:
    """Zlicza poziomy log├│w w podanym pliku."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Plik nie istnieje: {path}")

    if not path.is_file():
        raise ValueError(f"Podana ┼Ťcie┼╝ka nie jest plikiem: {path}")

    counter = Counter()

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            match = LOG_PATTERN.match(line.strip())
            if match:
                counter[match.group(1)] += 1

    result = {
        level: counter.get(level, 0)
        for level in LOG_LEVELS
    }

    return result


def print_report(result: dict[str, int]) -> None:
    """Wy┼Ťwietla czytelne podsumowanie log├│w."""
    print("=== LOG REPORT ===")

    total = sum(result.values())

    for level, count in result.items():
        print(f"{level:<8}: {count}")

    print(f"TOTAL   : {total}")


if __name__ == "__main__":
    try:
        report = parse_log_file("app.log")
        print_report(report)

    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"[ERROR] {exc}")
