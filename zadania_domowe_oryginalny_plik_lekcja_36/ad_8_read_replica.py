import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def create_read_replica(
    source_db_identifier: str,
    replica_identifier: str,
    region: str = "eu-central-1",
    poll_interval: int = 30,
    timeout_minutes: int = 20,
) -> str:
    """Tworzy Read Replica dla istniejącej bazy RDS i czeka aż będzie dostępna."""
    rds = boto3.client("rds", region_name=region)

    print(f"[RUN] Tworzenie Read Replica: {replica_identifier}")
    print(f"[INFO] Baza źródłowa: {source_db_identifier}")

    rds.create_db_instance_read_replica(
        DBInstanceIdentifier=replica_identifier,
        SourceDBInstanceIdentifier=source_db_identifier,
    )

    print(f"[WAIT] Oczekiwanie na dostępność repliki...")

    deadline = time.time() + timeout_minutes * 60

    while time.time() < deadline:
        response = rds.describe_db_instances(
            DBInstanceIdentifier=replica_identifier,
        )

        instance = response["DBInstances"][0]
        status = instance["DBInstanceStatus"]

        print(f"[STATUS] {status}")

        if status == "available":
            endpoint = instance["Endpoint"]["Address"]
            port = instance["Endpoint"]["Port"]

            print(f"[OK] Replica dostępna.")
            print(f"[ENDPOINT] {endpoint}:{port}")

            return endpoint

        time.sleep(poll_interval)

    raise TimeoutError(
        f"Replica {replica_identifier} nie osiągnęła statusu 'available' "
        f"w ciągu {timeout_minutes} minut."
    )


if __name__ == "__main__":
    try:
        create_read_replica(
            source_db_identifier="lesson36-postgres-db",
            replica_identifier="lesson36-postgres-db-replica",
        )

    except (ClientError, BotoCoreError, TimeoutError) as exc:
        print(f"[ERROR] {exc}")