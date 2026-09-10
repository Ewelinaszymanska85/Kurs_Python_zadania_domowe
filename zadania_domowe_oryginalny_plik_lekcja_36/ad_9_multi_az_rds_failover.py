import time
from datetime import datetime, timezone

import boto3
import psycopg2
from botocore.exceptions import BotoCoreError, ClientError


class MultiAZFailoverTester:
    """Tworzy Multi-AZ RDS, testuje połączenie i mierzy downtime podczas failover."""

    def __init__(self, region: str = "eu-central-1") -> None:
        self.rds = boto3.client("rds", region_name=region)

    def create_multi_az_instance(
        self,
        db_instance_identifier: str,
        master_username: str,
        master_password: str,
        allocated_storage: int = 20,
    ) -> None:
        """Tworzy instancję RDS PostgreSQL z włączonym Multi-AZ."""
        print(f"[RUN] Tworzenie Multi-AZ instancji: {db_instance_identifier}")

        self.rds.create_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            DBInstanceClass="db.t3.micro",
            Engine="postgres",
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            AllocatedStorage=allocated_storage,
            MultiAZ=True,
            PubliclyAccessible=False,
        )

        waiter = self.rds.get_waiter("db_instance_available")
        waiter.wait(DBInstanceIdentifier=db_instance_identifier)

        print(f"[OK] Instancja Multi-AZ dostępna: {db_instance_identifier}")

    def get_endpoint(self, db_instance_identifier: str) -> tuple[str, int]:
        """Pobiera endpoint i port instancji RDS."""
        response = self.rds.describe_db_instances(
            DBInstanceIdentifier=db_instance_identifier,
        )

        instance = response["DBInstances"][0]
        endpoint = instance["Endpoint"]["Address"]
        port = instance["Endpoint"]["Port"]

        return endpoint, port

    def test_connection(
        self,
        endpoint: str,
        port: int,
        username: str,
        password: str,
        database: str = "postgres",
    ) -> bool:
        """Testuje połączenie do bazy PostgreSQL. Zwraca True/False."""
        try:
            connection = psycopg2.connect(
                host=endpoint,
                port=port,
                user=username,
                password=password,
                dbname=database,
                connect_timeout=3,
            )
            connection.close()
            return True

        except psycopg2.OperationalError:
            return False

    def trigger_failover(self, db_instance_identifier: str) -> None:
        """Wywołuje reboot z failover na instancji Multi-AZ."""
        print(f"[RUN] Wywołanie failover dla: {db_instance_identifier}")

        self.rds.reboot_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            ForceFailover=True,
        )

    def measure_failover_downtime(
        self,
        db_instance_identifier: str,
        username: str,
        password: str,
        check_interval: float = 1.0,
        max_checks: int = 300,
    ) -> dict:
        """Mierzy czas niedostępności bazy podczas failover."""
        endpoint, port = self.get_endpoint(db_instance_identifier)

        print("=== TEST FAILOVER - RAPORT DOWNTIME ===")
        print(f"[INFO] Endpoint: {endpoint}:{port}")

        self.trigger_failover(db_instance_identifier)

        downtime_start = None
        downtime_end = None
        checks_done = 0

        # Czekaj, aż baza faktycznie przestanie odpowiadać (start awarii).
        while checks_done < max_checks:
            is_up = self.test_connection(endpoint, port, username, password)
            checks_done += 1

            if not is_up:
                downtime_start = datetime.now(timezone.utc)
                print(f"[DOWN] Baza niedostępna od: {downtime_start.isoformat()}")
                break

            time.sleep(check_interval)

        if downtime_start is None:
            print("[WARNING] Nie wykryto przerwy w połączeniu w czasie obserwacji.")
            return {"downtime_seconds": 0.0, "detected": False}

        # Czekaj, aż baza znowu zacznie odpowiadać (koniec awarii).
        while checks_done < max_checks:
            is_up = self.test_connection(endpoint, port, username, password)
            checks_done += 1

            if is_up:
                downtime_end = datetime.now(timezone.utc)
                print(f"[UP] Baza znowu dostępna od: {downtime_end.isoformat()}")
                break

            time.sleep(check_interval)

        if downtime_end is None:
            raise TimeoutError("Baza nie wróciła do stanu 'available' w czasie obserwacji.")

        downtime_seconds = (downtime_end - downtime_start).total_seconds()

        print(f"\n[RAPORT] Czas niedostępności podczas failover: {downtime_seconds:.1f}s")

        return {
            "downtime_seconds": downtime_seconds,
            "detected": True,
            "started_at": downtime_start.isoformat(),
            "ended_at": downtime_end.isoformat(),
        }


if __name__ == "__main__":
    tester = MultiAZFailoverTester(region="eu-central-1")

    DB_IDENTIFIER = "lesson36-multiaz-db"
    MASTER_USERNAME = "admin_user"
    MASTER_PASSWORD = "ZmienToHaslo123!"

    CREATE_NEW_INSTANCE = False  # ustaw True tylko przy pierwszym uruchomieniu

    try:
        if CREATE_NEW_INSTANCE:
            tester.create_multi_az_instance(
                db_instance_identifier=DB_IDENTIFIER,
                master_username=MASTER_USERNAME,
                master_password=MASTER_PASSWORD,
            )

        report = tester.measure_failover_downtime(
            db_instance_identifier=DB_IDENTIFIER,
            username=MASTER_USERNAME,
            password=MASTER_PASSWORD,
        )

        print(f"\n[SUMMARY] {report}")

    except (ClientError, BotoCoreError, TimeoutError) as exc:
        print(f"[ERROR] {exc}")