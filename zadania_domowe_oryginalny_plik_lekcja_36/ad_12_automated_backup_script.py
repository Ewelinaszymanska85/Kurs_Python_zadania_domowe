import logging
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

import boto3
import schedule
from botocore.exceptions import BotoCoreError, ClientError


LOG_FILE = "rds_backup.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


class AutomatedRDSBackup:
    """Automatyzuje tworzenie i rotację snapshotów RDS z powiadomieniem email."""

    def __init__(
        self,
        db_instance_identifier: str,
        retention_days: int = 7,
        region: str = "eu-central-1",
    ) -> None:
        self.db_instance_identifier = db_instance_identifier
        self.retention_days = retention_days
        self.rds = boto3.client("rds", region_name=region)

    def create_daily_snapshot(self) -> str:
        """Tworzy snapshot RDS z automatyczną nazwą zawierającą datę."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_id = f"{self.db_instance_identifier}-auto-{timestamp}"

        logging.info("Tworzenie snapshotu: %s", snapshot_id)

        self.rds.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_id,
            DBInstanceIdentifier=self.db_instance_identifier,
        )

        waiter = self.rds.get_waiter("db_snapshot_available")
        waiter.wait(DBSnapshotIdentifier=snapshot_id)

        logging.info("Snapshot utworzony pomyslnie: %s", snapshot_id)

        return snapshot_id

    def delete_old_snapshots(self) -> list[str]:
        """Usuwa manualne snapshoty starsze niż retention_days."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=self.retention_days)

        response = self.rds.describe_db_snapshots(
            DBInstanceIdentifier=self.db_instance_identifier,
            SnapshotType="manual",
        )

        deleted = []

        for snapshot in response.get("DBSnapshots", []):
            snapshot_id = snapshot["DBSnapshotIdentifier"]
            created_at = snapshot["SnapshotCreateTime"]

            if created_at < cutoff:
                self.rds.delete_db_snapshot(DBSnapshotIdentifier=snapshot_id)
                deleted.append(snapshot_id)
                logging.info("Usunieto stary snapshot: %s (utworzony %s)", snapshot_id, created_at)

        return deleted

    def send_email_notification(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        recipient: str,
        snapshot_id: str,
        deleted_snapshots: list[str],
    ) -> None:
        """Wysyła email z podsumowaniem operacji backupu."""
        body_lines = [
            f"Backup RDS zakonczony dla: {self.db_instance_identifier}",
            f"Nowy snapshot: {snapshot_id}",
            f"Usuniete stare snapshoty ({len(deleted_snapshots)}):",
        ]
        body_lines.extend(f"  - {s}" for s in deleted_snapshots) or body_lines.append("  brak")

        message = MIMEText("\n".join(body_lines))
        message["Subject"] = f"[RDS Backup] {self.db_instance_identifier} - {datetime.now():%Y-%m-%d}"
        message["From"] = smtp_user
        message["To"] = recipient

        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(message)

            logging.info("Email z powiadomieniem wyslany do: %s", recipient)

        except smtplib.SMTPException as exc:
            logging.error("Nie udalo sie wyslac emaila: %s", exc)

    def run_backup_job(
        self,
        smtp_config: dict,
    ) -> None:
        """Pełny przebieg: snapshot, rotacja, powiadomienie."""
        logging.info("=== START ZADANIA BACKUP ===")

        try:
            snapshot_id = self.create_daily_snapshot()
            deleted = self.delete_old_snapshots()

            self.send_email_notification(
                snapshot_id=snapshot_id,
                deleted_snapshots=deleted,
                **smtp_config,
            )

            logging.info("=== ZADANIE BACKUP ZAKONCZONE SUKCESEM ===")

        except (ClientError, BotoCoreError) as exc:
            logging.error("Blad podczas zadania backup: %s", exc)


if __name__ == "__main__":
    backup = AutomatedRDSBackup(
        db_instance_identifier="lesson36-postgres-db",
        retention_days=7,
    )

    smtp_config = {
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_user": "twoj_email@gmail.com",
        "smtp_password": "haslo_aplikacji",
        "recipient": "admin@example.com",
    }

    schedule.every().day.at("02:00").do(backup.run_backup_job, smtp_config=smtp_config)

    print("=== SCHEDULER URUCHOMIONY - backup codziennie o 2:00 ===")
    print(f"Logi zapisywane do: {LOG_FILE}")

    while True:
        schedule.run_pending()
        import time
        time.sleep(60)