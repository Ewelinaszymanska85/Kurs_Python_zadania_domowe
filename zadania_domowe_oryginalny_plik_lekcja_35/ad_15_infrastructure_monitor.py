import csv
import time
from datetime import datetime
from pathlib import Path

import requests


class InfrastructureMonitor:
    """Monitoruje stan infrastruktury i zapisuje historię do CSV."""

    def __init__(
        self,
        cpu_threshold: float = 80.0,
        disk_threshold: float = 85.0,
        report_file: str = "infrastructure_report.csv",
    ) -> None:
        self.cpu_threshold = cpu_threshold
        self.disk_threshold = disk_threshold
        self.report_file = Path(report_file)

    def check_cpu(self, usage: float) -> str:
        return (
            "ALERT"
            if usage >= self.cpu_threshold
            else "OK"
        )

    def check_disk(self, usage: float) -> str:
        return (
            "ALERT"
            if usage >= self.disk_threshold
            else "OK"
        )

    @staticmethod
    def check_http(url: str) -> tuple[str, int | None]:
        try:
            response = requests.get(
                url,
                timeout=5,
            )

            status = (
                "OK"
                if response.status_code == 200
                else "ALERT"
            )

            return status, response.status_code

        except requests.RequestException:
            return "ERROR", None

    def save_report(
        self,
        cpu: float,
        disk: float,
        http_status: str,
    ) -> None:
        exists = self.report_file.exists()

        with self.report_file.open(
            "a",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            if not exists:
                writer.writerow(
                    [
                        "timestamp",
                        "cpu_usage",
                        "disk_usage",
                        "http_status",
                    ]
                )

            writer.writerow(
                [
                    datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    cpu,
                    disk,
                    http_status,
                ]
            )

    def run_check(
        self,
        cpu: float,
        disk: float,
        url: str,
    ) -> None:
        cpu_status = self.check_cpu(cpu)
        disk_status = self.check_disk(disk)
        http_status, http_code = self.check_http(url)

        print(f"[{cpu_status}] CPU: {cpu:.1f}%")
        print(f"[{disk_status}] EBS: {disk:.1f}%")
        print(
            f"[{http_status}] HTTP: "
            f"{http_code or 'brak odpowiedzi'}"
        )

        self.save_report(
            cpu,
            disk,
            http_status,
        )

    def monitor(
        self,
        url: str,
        interval: int = 1,
        iterations: int = 3,
    ) -> None:
        print("=== INFRASTRUCTURE MONITOR ===")

        for number in range(1, iterations + 1):
            print(f"\n--- Pomiar {number}/{iterations} ---")

            # Symulacja danych CloudWatch.
            cpu = 55.0 + number * 10
            disk = 70.0 + number * 5

            self.run_check(
                cpu,
                disk,
                url,
            )

            if number < iterations:
                time.sleep(interval)


if __name__ == "__main__":
    monitor = InfrastructureMonitor()

    monitor.monitor(
        url="https://example.com",
        interval=1,
        iterations=3,
    )