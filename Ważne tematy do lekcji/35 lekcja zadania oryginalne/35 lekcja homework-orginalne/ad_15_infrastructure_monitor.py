import csv
import time
from datetime import datetime
from pathlib import Path

import boto3
import requests
import schedule
from botocore.exceptions import BotoCoreError, ClientError


class InfrastructureMonitor:
    """Monitoruje stan infrastruktury AWS i zapisuje historię do CSV."""

    def __init__(
        self,
        region: str = "eu-central-1",
        disk_threshold: float = 85.0,
        report_file: str = "infrastructure_report.csv",
    ) -> None:
        self.ec2 = boto3.client("ec2", region_name=region)
        self.disk_threshold = disk_threshold
        self.report_file = Path(report_file)

    def check_ec2_instances(self) -> tuple[str, int, int]:
        """Sprawdza stan instancji EC2. Zwraca (status, running, total)."""
        try:
            response = self.ec2.describe_instances()

            states = [
                instance["State"]["Name"]
                for reservation in response.get("Reservations", [])
                for instance in reservation.get("Instances", [])
                if instance["State"]["Name"] != "terminated"
            ]

            running = sum(1 for state in states if state == "running")
            total = len(states)
            status = "OK" if running == total or total == 0 else "ALERT"

            return status, running, total

        except (ClientError, BotoCoreError) as exc:
            print(f"[ERROR] Nie udało się pobrać instancji EC2: {exc}")
            return "ERROR", 0, 0

    def check_ebs_volumes(self) -> tuple[str, float]:
        """Sprawdza wolumeny EBS pod kątem stanu innych niż 'in-use'/'available'."""
        try:
            response = self.ec2.describe_volumes()
            volumes = response.get("Volumes", [])

            if not volumes:
                return "OK", 0.0

            problematic = [
                volume
                for volume in volumes
                if volume["State"] not in ("in-use", "available")
            ]

            ratio = len(problematic) / len(volumes) * 100
            status = "ALERT" if ratio >= self.disk_threshold else "OK"

            return status, ratio

        except (ClientError, BotoCoreError) as exc:
            print(f"[ERROR] Nie udało się pobrać wolumenów EBS: {exc}")
            return "ERROR", 0.0

    @staticmethod
    def check_http(url: str) -> tuple[str, int | None]:
        try:
            response = requests.get(url, timeout=5)
            status = "OK" if response.status_code == 200 else "ALERT"
            return status, response.status_code

        except requests.RequestException:
            return "ERROR", None

    def save_report(
        self,
        ec2_status: str,
        volume_status: str,
        http_status: str,
    ) -> None:
        exists = self.report_file.exists()

        with self.report_file.open("a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not exists:
                writer.writerow(
                    ["timestamp", "ec2_status", "volume_status", "http_status"]
                )

            writer.writerow(
                [
                    datetime.now().isoformat(timespec="seconds"),
                    ec2_status,
                    volume_status,
                    http_status,
                ]
            )

    def run_check(self, url: str) -> None:
        ec2_status, running, total = self.check_ec2_instances()
        volume_status, problem_ratio = self.check_ebs_volumes()
        http_status, http_code = self.check_http(url)

        print(f"[{ec2_status}] EC2: {running}/{total} running")
        print(f"[{volume_status}] EBS: {problem_ratio:.1f}% problematycznych wolumenów")
        print(f"[{http_status}] HTTP: {http_code or 'brak odpowiedzi'}")

        if "ALERT" in (ec2_status, volume_status, http_status) or "ERROR" in (
            ec2_status,
            volume_status,
            http_status,
        ):
            print("[!] WYKRYTO PROBLEM W INFRASTRUKTURZE")

        self.save_report(ec2_status, volume_status, http_status)

    def monitor(self, url: str, interval_minutes: int = 5) -> None:
        print("=== INFRASTRUCTURE MONITOR ===")

        schedule.every(interval_minutes).minutes.do(self.run_check, url=url)

        self.run_check(url)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    monitor = InfrastructureMonitor()

    try:
        monitor.monitor(url="https://example.com", interval_minutes=5)
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring zatrzymany przez użytkownika.")