import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class RDSInstanceCreator:
    """Tworzy instancję RDS PostgreSQL wraz z manualnym snapshotem."""

    def __init__(self, region: str = "eu-central-1") -> None:
        self.rds = boto3.client("rds", region_name=region)

    def create_postgres_instance(
        self,
        db_instance_identifier: str,
        master_username: str,
        master_password: str,
        allocated_storage: int = 20,
        backup_retention_days: int = 3,
    ) -> dict:
        """Tworzy instancję RDS PostgreSQL (db.t3.micro) z backup retention."""
        print(f"[RUN] Tworzenie instancji RDS: {db_instance_identifier}")

        response = self.rds.create_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            DBInstanceClass="db.t3.micro",
            Engine="postgres",
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            AllocatedStorage=allocated_storage,
            BackupRetentionPeriod=backup_retention_days,
            PubliclyAccessible=False,
            StorageType="gp3",
            Tags=[
                {"Key": "Project", "Value": "lesson36-homework"},
            ],
        )

        print(f"[OK] Żądanie utworzenia instancji wysłane.")
        return response["DBInstance"]

    def wait_until_available(
        self,
        db_instance_identifier: str,
        poll_interval: int = 30,
        timeout_minutes: int = 15,
    ) -> None:
        """Czeka aż instancja RDS osiągnie status 'available'."""
        print(f"[WAIT] Oczekiwanie na dostępność instancji {db_instance_identifier}...")

        deadline = time.time() + timeout_minutes * 60

        while time.time() < deadline:
            response = self.rds.describe_db_instances(
                DBInstanceIdentifier=db_instance_identifier,
            )

            status = response["DBInstances"][0]["DBInstanceStatus"]
            print(f"[STATUS] {status}")

            if status == "available":
                print("[OK] Instancja jest dostępna.")
                return

            time.sleep(poll_interval)

        raise TimeoutError(
            f"Instancja {db_instance_identifier} nie osiągnęła statusu "
            f"'available' w ciągu {timeout_minutes} minut."
        )

    def create_manual_snapshot(
        self,
        db_instance_identifier: str,
        snapshot_identifier: str,
    ) -> str:
        """Tworzy manualny snapshot instancji RDS."""
        print(f"[RUN] Tworzenie snapshotu: {snapshot_identifier}")

        self.rds.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier,
            DBInstanceIdentifier=db_instance_identifier,
        )

        waiter = self.rds.get_waiter("db_snapshot_available")
        waiter.wait(DBSnapshotIdentifier=snapshot_identifier)

        print(f"[OK] Snapshot utworzony: {snapshot_identifier}")
        return snapshot_identifier

    def provision(
        self,
        db_instance_identifier: str,
        master_username: str,
        master_password: str,
    ) -> None:
        """Pełny proces: utworzenie instancji, oczekiwanie, snapshot."""
        print("=== RDS INSTANCE PROVISIONING ===")

        self.create_postgres_instance(
            db_instance_identifier,
            master_username,
            master_password,
        )

        self.wait_until_available(db_instance_identifier)

        snapshot_id = f"{db_instance_identifier}-initial-snapshot"
        self.create_manual_snapshot(db_instance_identifier, snapshot_id)

        print("\n[SUCCESS] Provisioning zakończony.")
        print(f"Instancja: {db_instance_identifier}")
        print(f"Snapshot: {snapshot_id}")


if __name__ == "__main__":
    creator = RDSInstanceCreator(region="eu-central-1")

    try:
        creator.provision(
            db_instance_identifier="lesson36-postgres-db",
            master_username="admin_user",
            master_password="ZmienToHaslo123!",
        )

    except (ClientError, BotoCoreError, TimeoutError) as exc:
        print(f"[ERROR] {exc}")