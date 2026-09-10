import time
from datetime import datetime, timezone


LOG_FILE = "/data/app.log"


def write_log_entry() -> None:
    """Dopisuje wpis z aktualnym czasem do pliku logu."""
    timestamp = datetime.now(timezone.utc).isoformat()

    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp} - Aplikacja dziala\n")

    print(f"[LOG] Zapisano wpis: {timestamp}")


if __name__ == "__main__":
    print("=== START APLIKACJI ===")

    while True:
        write_log_entry()
        time.sleep(5)