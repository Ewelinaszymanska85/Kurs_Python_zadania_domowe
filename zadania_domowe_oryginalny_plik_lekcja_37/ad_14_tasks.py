import time

from celery import Celery

celery_app = Celery(
    "ad_14_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
)


@celery_app.task(name="generate_report")
def generate_report(report_id: int) -> dict:
    """Symuluje długotrwałe generowanie raportu (np. 10 sekund)."""
    print(f"[WORKER] Rozpoczynam generowanie raportu #{report_id}")

    time.sleep(10)

    result = {
        "report_id": report_id,
        "status": "completed",
        "content": f"Raport #{report_id} - dane wygenerowane pomyslnie",
    }

    print(f"[WORKER] Zakonczono raport #{report_id}")

    return result