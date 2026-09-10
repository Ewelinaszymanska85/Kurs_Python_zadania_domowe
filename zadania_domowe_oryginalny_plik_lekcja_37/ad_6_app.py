import os
import time

import psycopg2


def wait_for_database(max_retries: int = 10, delay_seconds: int = 3) -> psycopg2.extensions.connection:
    """Próbuje połączyć się z bazą danych, ponawiając próby aż do skutku."""
    for attempt in range(1, max_retries + 1):
        try:
            connection = psycopg2.connect(
                host=os.environ["DB_HOST"],
                port=os.environ.get("DB_PORT", "5432"),
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
            )
            print(f"[OK] Połączono z bazą danych (próba {attempt})")
            return connection

        except psycopg2.OperationalError as exc:
            print(f"[RETRY] Baza niedostępna (próba {attempt}/{max_retries}): {exc}")
            time.sleep(delay_seconds)

    raise ConnectionError("Nie udało się połączyć z bazą danych.")


if __name__ == "__main__":
    connection = wait_for_database()

    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    print(f"[INFO] Wersja bazy danych: {db_version[0]}")

    cursor.close()
    connection.close()