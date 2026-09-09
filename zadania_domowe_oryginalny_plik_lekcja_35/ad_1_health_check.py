import time

import requests


SERVICES = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "Python", "url": "https://www.python.org"},
]


def check_service(name: str, url: str, timeout: int = 5) -> dict:
    """Sprawdza dostępność serwisu i mierzy czas odpowiedzi."""
    start_time = time.perf_counter()

    try:
        response = requests.get(url, timeout=timeout)
        response_time = time.perf_counter() - start_time

        return {
            "name": name,
            "url": url,
            "status_code": response.status_code,
            "response_time": round(response_time, 3),
            "available": response.status_code == 200,
        }

    except requests.Timeout:
        return {
            "name": name,
            "url": url,
            "error": "Przekroczono czas oczekiwania.",
            "available": False,
        }

    except requests.RequestException as exc:
        return {
            "name": name,
            "url": url,
            "error": str(exc),
            "available": False,
        }


def run_health_check() -> None:
    """Uruchamia health check dla wszystkich skonfigurowanych serwisów."""
    print("=== HEALTH CHECK ===")

    for service in SERVICES:
        result = check_service(
            service["name"],
            service["url"],
        )

        if result["available"]:
            print(
                f"[OK] {result['name']} | "
                f"HTTP {result['status_code']} | "
                f"{result['response_time']} s"
            )
        else:
            print(
                f"[ERROR] {result['name']} | "
                f"{result.get('error', 'Serwis zwrócił niepoprawny status')}"
            )


if __name__ == "__main__":
    run_health_check()