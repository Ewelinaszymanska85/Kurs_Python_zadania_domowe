from collections import Counter
from pathlib import Path


LOG_LEVELS = ("ERROR", "WARNING", "INFO")


def parse_log_file(file_path: str) -> dict[str, int]:
    """Zlicza poziomy logów w podanym pliku."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Plik nie istnieje: {path}")

    if not path.is_file():
        raise ValueError(f"Podana ścieżka nie jest plikiem: {path}")

    counter = Counter()

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            normalized = line.upper()

            for level in LOG_LEVELS:
                if level in normalized:
                    counter[level] += 1
                    break

    result = {
        level: counter.get(level, 0)
        for level in LOG_LEVELS
    }

    return result


def print_report(result: dict[str, int]) -> None:
    """Wyświetla czytelne podsumowanie logów."""
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