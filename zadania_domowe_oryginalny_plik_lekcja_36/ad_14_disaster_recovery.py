import time
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class DisasterRecoveryPlan:
    """Implementuje disaster recovery plan między dwoma regionami AWS."""

    def __init__(
        self,
        primary_region: str = "eu-central-1",
        backup_region: str = "us-east-1",
    ) -> None:
        self.primary_region = primary_region
        self.backup_region = backup_region

        self.route53 = boto3.client("route53")
        self.s3_primary = boto3.client("s3", region_name=primary_region)
        self.rds_primary = boto3.client("rds", region_name=primary_region)
        self.rds_backup = boto3.client("rds", region_name=backup_region)

    def create_health_check(
        self,
        endpoint_ip_or_domain: str,
        port: int = 80,
        resource_path: str = "/health",
        request_interval: int = 30,
        failure_threshold: int = 3,
    ) -> str:
        """Tworzy health check w Route53 monitorujący endpoint primary regionu."""
        response = self.route53.create_health_check(
            CallerReference=f"dr-healthcheck-{int(time.time())}",
            HealthCheckConfig={
                "IPAddress": None,
                "FullyQualifiedDomainName": endpoint_ip_or_domain,
                "Port": port,
                "Type": "HTTP",
                "ResourcePath": resource_path,
                "RequestInterval": request_interval,
                "FailureThreshold": failure_threshold,
            },
        )

        health_check_id = response["HealthCheck"]["Id"]

        print(f"[OK] Utworzono health check: {health_check_id}")
        print(f"[INFO] Monitoruje: {endpoint_ip_or_domain}:{port}{resource_path}")
        print(f"[INFO] Interwał: {request_interval}s | Próg awarii: {failure_threshold}")

        return health_check_id

    def setup_failover_routing(
        self,
        hosted_zone_id: str,
        domain: str,
        primary_endpoint: str,
        backup_endpoint: str,
        health_check_id: str,
    ) -> None:
        """Konfiguruje Route53 failover routing z health checkiem na primary."""
        changes = [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": domain,
                    "Type": "CNAME",
                    "SetIdentifier": "primary",
                    "Failover": "PRIMARY",
                    "TTL": 60,
                    "ResourceRecords": [{"Value": primary_endpoint}],
                    "HealthCheckId": health_check_id,
                },
            },
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": domain,
                    "Type": "CNAME",
                    "SetIdentifier": "backup",
                    "Failover": "SECONDARY",
                    "TTL": 60,
                    "ResourceRecords": [{"Value": backup_endpoint}],
                },
            },
        ]

        self.route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={"Changes": changes},
        )

        print(f"[OK] Failover routing skonfigurowany dla: {domain}")
        print(f"[INFO] Primary: {primary_endpoint} | Backup: {backup_endpoint}")

    def replicate_s3_bucket(
        self,
        source_bucket: str,
        destination_bucket: str,
    ) -> int:
        """Kopiuje wszystkie obiekty z bucketa primary do bucketa backup w innym regionie."""
        s3_destination = boto3.client("s3", region_name=self.backup_region)

        paginator = self.s3_primary.get_paginator("list_objects_v2")
        copied = 0

        for page in paginator.paginate(Bucket=source_bucket):
            for obj in page.get("Contents", []):
                key = obj["Key"]

                copy_source = {"Bucket": source_bucket, "Key": key}

                s3_destination.copy_object(
                    CopySource=copy_source,
                    Bucket=destination_bucket,
                    Key=key,
                )

                copied += 1

        print(f"[OK] Zreplikowano {copied} obiektów: {source_bucket} -> {destination_bucket}")

        return copied

    def copy_rds_snapshot_to_backup_region(
        self,
        source_db_identifier: str,
        snapshot_identifier: str,
    ) -> str:
        """Tworzy snapshot RDS w primary regionie i kopiuje go do backup regionu."""
        print(f"[RUN] Tworzenie snapshotu w {self.primary_region}: {snapshot_identifier}")

        self.rds_primary.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier,
            DBInstanceIdentifier=source_db_identifier,
        )

        waiter = self.rds_primary.get_waiter("db_snapshot_available")
        waiter.wait(DBSnapshotIdentifier=snapshot_identifier)

        source_snapshot_arn = (
            f"arn:aws:rds:{self.primary_region}:"
            f"{boto3.client('sts').get_caller_identity()['Account']}:"
            f"snapshot:{snapshot_identifier}"
        )

        print(f"[RUN] Kopiowanie snapshotu do {self.backup_region}...")

        self.rds_backup.copy_db_snapshot(
            SourceDBSnapshotIdentifier=source_snapshot_arn,
            TargetDBSnapshotIdentifier=f"{snapshot_identifier}-copy",
            SourceRegion=self.primary_region,
        )

        waiter = self.rds_backup.get_waiter("db_snapshot_available")
        waiter.wait(DBSnapshotIdentifier=f"{snapshot_identifier}-copy")

        print(f"[OK] Snapshot skopiowany do regionu backup: {snapshot_identifier}-copy")

        return f"{snapshot_identifier}-copy"

    def simulate_regional_failure(
        self,
        health_check_id: str,
        domain: str,
        poll_interval: int = 15,
        max_checks: int = 40,
    ) -> dict:
        """
        Symuluje awarię przez oczekiwanie na zmianę statusu health checka na Failed,
        a następnie mierzy czas do momentu, gdy Route53 przełączy ruch na backup.
        """
        import dns.resolver

        print("=== SYMULACJA AWARII PRIMARY REGION ===")
        print("[INFO] Wyłącz ręcznie usługę w primary region (np. zatrzymaj ALB/instancje),")
        print("[INFO] następnie skrypt zmierzy czas do przełączenia na backup region.\n")

        failover_start = datetime.now(timezone.utc)
        checks_done = 0

        resolver = dns.resolver.Resolver()
        resolver.cache = None

        while checks_done < max_checks:
            try:
                answer = resolver.resolve(domain, "CNAME")
                resolved_target = str(answer[0].target).rstrip(".")

                print(f"[CHECK] Rozwiązano na: {resolved_target}")

                if "backup" in resolved_target.lower() or self.backup_region in resolved_target:
                    failover_end = datetime.now(timezone.utc)
                    downtime = (failover_end - failover_start).total_seconds()

                    print(f"\n[OK] Przełączenie na backup wykryte po {downtime:.1f}s")

                    return {
                        "failover_seconds": downtime,
                        "resolved_to": resolved_target,
                    }

            except dns.exception.DNSException as exc:
                print(f"[WARNING] Błąd zapytania DNS: {exc}")

            checks_done += 1
            time.sleep(poll_interval)

        raise TimeoutError("Nie wykryto przełączenia na backup region w czasie obserwacji.")


if __name__ == "__main__":
    dr_plan = DisasterRecoveryPlan(
        primary_region="eu-central-1",
        backup_region="us-east-1",
    )

    try:
        health_check_id = dr_plan.create_health_check(
            endpoint_ip_or_domain="primary-alb.eu-central-1.elb.amazonaws.com",
            port=80,
            resource_path="/health",
        )

        dr_plan.setup_failover_routing(
            hosted_zone_id="Z1234567890ABC",
            domain="app.yourdomain.com",
            primary_endpoint="primary-alb.eu-central-1.elb.amazonaws.com",
            backup_endpoint="backup-alb.us-east-1.elb.amazonaws.com",
            health_check_id=health_check_id,
        )

        dr_plan.replicate_s3_bucket(
            source_bucket="lesson36-primary-bucket",
            destination_bucket="lesson36-backup-bucket",
        )

        dr_plan.copy_rds_snapshot_to_backup_region(
            source_db_identifier="lesson36-postgres-db",
            snapshot_identifier="lesson36-dr-snapshot",
        )

        report = dr_plan.simulate_regional_failure(
            health_check_id=health_check_id,
            domain="app.yourdomain.com",
        )

        print(f"\n[RAPORT KOŃCOWY] {report}")

    except (ClientError, BotoCoreError, TimeoutError) as exc:
        print(f"[ERROR] {exc}")