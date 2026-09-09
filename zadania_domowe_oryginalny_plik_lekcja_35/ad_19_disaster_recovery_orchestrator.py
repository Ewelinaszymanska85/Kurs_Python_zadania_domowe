from datetime import datetime
import json
import logging
from pathlib import Path
from uuid import uuid4


LOG_FILE = "disaster_recovery.log"
SNAPSHOT_FILE = "snapshots.json"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


class DisasterRecoveryOrchestrator:
    """Symuluje proces disaster recovery dla EC2 i RDS."""

    def __init__(self, backup_region: str = "eu-west-1") -> None:
        self.backup_region = backup_region
        self.snapshot_path = Path(SNAPSHOT_FILE)

    def _load_snapshots(self) -> list[dict]:
        if not self.snapshot_path.exists():
            return []

        with self.snapshot_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_snapshots(self, snapshots: list[dict]) -> None:
        with self.snapshot_path.open("w", encoding="utf-8") as file:
            json.dump(
                snapshots,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def _update_status(self, snapshot_id: str, status: str) -> None:
        snapshots = self._load_snapshots()

        for snapshot in snapshots:
            if snapshot["snapshot_id"] == snapshot_id:
                snapshot["status"] = status
                break

        self._save_snapshots(snapshots)

    def create_snapshot(
        self,
        resource_type: str,
        resource_id: str,
    ) -> str:
        snapshot_id = f"snap-{uuid4().hex[:10]}"

        snapshot = {
            "snapshot_id": snapshot_id,
            "resource_type": resource_type.upper(),
            "resource_id": resource_id,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "status": "CREATED",
        }

        snapshots = self._load_snapshots()
        snapshots.append(snapshot)
        self._save_snapshots(snapshots)

        logging.info(
            "Utworzono snapshot %s dla %s %s",
            snapshot_id,
            resource_type,
            resource_id,
        )

        print(f"[OK] Utworzono snapshot: {snapshot_id}")
        return snapshot_id

    def store_backup_s3(self, snapshot_id: str) -> None:
        self._update_status(snapshot_id, "BACKED_UP")

        logging.info(
            "Snapshot %s zapisany w S3 w regionie %s",
            snapshot_id,
            self.backup_region,
        )

        print(
            f"[BACKUP] {snapshot_id} -> "
            f"S3 region: {self.backup_region}"
        )

    def restore_from_backup(self, snapshot_id: str) -> bool:
        snapshots = self._load_snapshots()

        snapshot = next(
            (
                item
                for item in snapshots
                if item["snapshot_id"] == snapshot_id
            ),
            None,
        )

        if snapshot is None:
            logging.error(
                "Nie znaleziono snapshotu %s",
                snapshot_id,
            )
            print(f"[ERROR] Snapshot nie istnieje: {snapshot_id}")
            return False

        self._update_status(snapshot_id, "RESTORED")

        logging.info(
            "Odtworzono zas├│b %s z snapshotu %s",
            snapshot["resource_id"],
            snapshot_id,
        )

        print(
            f"[RESTORE] {snapshot['resource_type']} "
            f"{snapshot['resource_id']} "
            f"z {snapshot_id}"
        )

        return True

    def test_recovery(self) -> None:
        print("=== DISASTER RECOVERY TEST ===")

        ec2_snapshot = self.create_snapshot(
            "EC2",
            "i-demo123456",
        )

        rds_snapshot = self.create_snapshot(
            "RDS",
            "database-production",
        )

        for snapshot_id in (ec2_snapshot, rds_snapshot):
            self.store_backup_s3(snapshot_id)
            self.restore_from_backup(snapshot_id)

        logging.info("Test disaster recovery zako┼äczony pomy┼Ťlnie.")
        print("\n[OK] Disaster recovery test zako┼äczony.")


if __name__ == "__main__":
    orchestrator = DisasterRecoveryOrchestrator(
        backup_region="eu-west-1"
    )
    orchestrator.test_recovery()
