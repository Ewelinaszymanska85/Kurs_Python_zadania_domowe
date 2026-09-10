from datetime import datetime, timedelta, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class CostOptimizationStrategy:
    """Implementuje strategie optymalizacji kosztów AWS i generuje raport oszczędności."""

    ON_DEMAND_PRICES = {
        "t3.micro": 0.0104,
        "t3.small": 0.0208,
        "t3.medium": 0.0416,
        "m5.large": 0.096,
    }

    RESERVED_DISCOUNT = 0.40  # przybliżona zniżka dla 1-year Reserved Instance

    def __init__(self, region: str = "eu-central-1") -> None:
        self.region = region
        self.autoscaling = boto3.client("autoscaling", region_name=region)
        self.ec2 = boto3.client("ec2", region_name=region)
        self.cloudwatch = boto3.client("cloudwatch", region_name=region)

    def setup_scheduled_scaling(
        self,
        asg_name: str,
        scale_down_hour_utc: int = 22,
        scale_up_hour_utc: int = 6,
        night_capacity: int = 1,
        day_capacity: int = 3,
    ) -> None:
        """Konfiguruje scheduled scaling: mniej instancji w nocy, więcej w dzień."""
        self.autoscaling.put_scheduled_update_group_action(
            AutoScalingGroupName=asg_name,
            ScheduledActionName=f"{asg_name}-scale-down-night",
            Recurrence=f"0 {scale_down_hour_utc} * * *",
            DesiredCapacity=night_capacity,
            MinSize=night_capacity,
        )

        self.autoscaling.put_scheduled_update_group_action(
            AutoScalingGroupName=asg_name,
            ScheduledActionName=f"{asg_name}-scale-up-day",
            Recurrence=f"0 {scale_up_hour_utc} * * *",
            DesiredCapacity=day_capacity,
            MinSize=day_capacity,
        )

        print(f"[OK] Scheduled scaling: {night_capacity} instancji w nocy, {day_capacity} w dzień")

    def calculate_spot_savings(
        self,
        instance_type: str,
        hours_per_month: int,
        spot_discount: float = 0.65,
    ) -> dict:
        """Szacuje oszczędności z użycia Spot Instances zamiast On-Demand."""
        on_demand_price = self.ON_DEMAND_PRICES.get(instance_type, 0.0)
        spot_price = on_demand_price * (1 - spot_discount)

        on_demand_cost = on_demand_price * hours_per_month
        spot_cost = spot_price * hours_per_month
        savings = on_demand_cost - spot_cost

        return {
            "instance_type": instance_type,
            "on_demand_monthly_usd": round(on_demand_cost, 2),
            "spot_monthly_usd": round(spot_cost, 2),
            "monthly_savings_usd": round(savings, 2),
        }

    def calculate_reserved_instance_savings(
        self,
        instance_type: str,
        instance_count: int,
        hours_per_month: int = 720,
    ) -> dict:
        """Szacuje oszczędności z Reserved Instances dla instancji działających 24/7."""
        on_demand_price = self.ON_DEMAND_PRICES.get(instance_type, 0.0)

        on_demand_monthly = on_demand_price * hours_per_month * instance_count
        reserved_monthly = on_demand_monthly * (1 - self.RESERVED_DISCOUNT)
        savings = on_demand_monthly - reserved_monthly

        return {
            "instance_type": instance_type,
            "instance_count": instance_count,
            "on_demand_monthly_usd": round(on_demand_monthly, 2),
            "reserved_monthly_usd": round(reserved_monthly, 2),
            "monthly_savings_usd": round(savings, 2),
        }

    def apply_s3_lifecycle_policy(
        self,
        bucket_name: str,
        prefix: str = "releases/old/",
        transition_days: int = 30,
    ) -> None:
        """Konfiguruje S3 Lifecycle policy przenoszącą stare pliki do Glacier."""
        s3 = boto3.client("s3", region_name=self.region)

        s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration={
                "Rules": [
                    {
                        "ID": "move-old-releases-to-glacier",
                        "Status": "Enabled",
                        "Filter": {"Prefix": prefix},
                        "Transitions": [
                            {
                                "Days": transition_days,
                                "StorageClass": "GLACIER",
                            }
                        ],
                    }
                ]
            },
        )

        print(f"[OK] Lifecycle policy: pliki w '{prefix}' -> Glacier po {transition_days} dniach")

    def find_underutilized_instances(
        self,
        cpu_threshold: float = 10.0,
        lookback_hours: int = 24,
    ) -> list[dict]:
        """Znajduje instancje EC2 o niskim wykorzystaniu CPU - kandydatów do optymalizacji."""
        response = self.ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}],
        )

        underutilized = []
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=lookback_hours)

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance["InstanceId"]

                metrics = self.cloudwatch.get_metric_statistics(
                    Namespace="AWS/EC2",
                    MetricName="CPUUtilization",
                    Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,
                    Statistics=["Average"],
                )

                datapoints = metrics.get("Datapoints", [])

                if not datapoints:
                    continue

                avg_cpu = sum(d["Average"] for d in datapoints) / len(datapoints)

                if avg_cpu < cpu_threshold:
                    underutilized.append({
                        "instance_id": instance_id,
                        "instance_type": instance["InstanceType"],
                        "avg_cpu_percent": round(avg_cpu, 1),
                    })

        return underutilized

    def generate_optimization_report(
        self,
        report_file: str = "cost_optimization_report.md",
        reserved_candidates: list[dict] | None = None,
        spot_estimate: dict | None = None,
    ) -> None:
        """Generuje raport rekomendacji optymalizacji kosztów w formacie markdown."""
        lines = [
            "# Cost Optimization Report",
            "",
            f"Wygenerowano: {datetime.now():%Y-%m-%d %H:%M}",
            "",
            "## Niedowykorzystane instancje (kandydaci do Reserved Instance)",
            "",
        ]

        underutilized = self.find_underutilized_instances()

        if underutilized:
            for instance in underutilized:
                lines.append(
                    f"- `{instance['instance_id']}` ({instance['instance_type']}) "
                    f"- średnie CPU: {instance['avg_cpu_percent']}%"
                )
        else:
            lines.append("- Brak wykrytych niedowykorzystanych instancji.")

        lines.append("")
        lines.append("## Szacowane oszczędności - Reserved Instances")
        lines.append("")

        if reserved_candidates:
            total_ri_savings = 0.0
            for candidate in reserved_candidates:
                result = self.calculate_reserved_instance_savings(**candidate)
                total_ri_savings += result["monthly_savings_usd"]
                lines.append(
                    f"- {result['instance_count']}x {result['instance_type']}: "
                    f"oszczędność {result['monthly_savings_usd']} USD/mies."
                )
            lines.append(f"\n**Łączna oszczędność RI: {total_ri_savings:.2f} USD/mies.**")

        lines.append("")
        lines.append("## Szacowane oszczędności - Spot Instances")
        lines.append("")

        if spot_estimate:
            lines.append(
                f"- {spot_estimate['instance_type']}: "
                f"oszczędność {spot_estimate['monthly_savings_usd']} USD/mies. "
                f"(On-Demand: {spot_estimate['on_demand_monthly_usd']} USD "
                f"-> Spot: {spot_estimate['spot_monthly_usd']} USD)"
            )

        from pathlib import Path
        Path(report_file).write_text("\n".join(lines), encoding="utf-8")

        print(f"[OK] Raport zapisany: {report_file}")


if __name__ == "__main__":
    optimizer = CostOptimizationStrategy(region="eu-central-1")

    try:
        optimizer.setup_scheduled_scaling(asg_name="lesson36-asg")

        optimizer.apply_s3_lifecycle_policy(bucket_name="lesson36-primary-bucket")

        reserved_candidates = [
            {"instance_type": "t3.medium", "instance_count": 2},
        ]
        spot_estimate = optimizer.calculate_spot_savings(
            instance_type="t3.small",
            hours_per_month=720,
        )

        optimizer.generate_optimization_report(
            reserved_candidates=reserved_candidates,
            spot_estimate=spot_estimate,
        )

    except (ClientError, BotoCoreError) as exc:
        print(f"[ERROR] {exc}")