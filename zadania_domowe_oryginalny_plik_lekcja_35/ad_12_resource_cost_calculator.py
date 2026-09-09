from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


class AWSCostCalculator:
    """Szacuje koszt dzia┼éania instancji EC2."""

    PRICES = {
        "t3.micro": 0.01,
        "t3.small": 0.02,
        "t3.medium": 0.04,
        "m5.large": 0.10,
    }

    def __init__(self, region: str = "eu-central-1") -> None:
        self.ec2 = boto3.client("ec2", region_name=region)

    def get_instances(self) -> list[dict]:
        """Pobiera instancje EC2 wraz z typem i czasem uruchomienia."""
        response = self.ec2.describe_instances()

        return [
            instance
            for reservation in response.get("Reservations", [])
            for instance in reservation.get("Instances", [])
            if instance.get("State", {}).get("Name") != "terminated"
        ]

    def calculate_instance_cost(self, instance: dict) -> float:
        """Oblicza szacowany koszt pojedynczej instancji (tylko running)."""
        state = instance.get("State", {}).get("Name")

        if state != "running":
            return 0.0

        instance_type = instance["InstanceType"]
        launch_time = instance["LaunchTime"]

        hourly_price = self.PRICES.get(instance_type, 0.0)

        if hourly_price == 0:
            print(f"[WARNING] Brak ceny dla typu: {instance_type}")
            return 0.0

        now = datetime.now(timezone.utc)
        hours = max(
            (now - launch_time).total_seconds() / 3600,
            0,
        )

        return hourly_price * hours

    def generate_report(self) -> float:
        """Generuje raport koszt├│w wszystkich instancji."""
        instances = self.get_instances()
        total_cost = 0.0

        print("=== AWS EC2 COST REPORT ===")

        if not instances:
            print("[INFO] Brak instancji do analizy.")
            return 0.0

        for instance in instances:
            cost = self.calculate_instance_cost(instance)
            total_cost += cost

            print(
                f"{instance['InstanceId']} | "
                f"{instance['InstanceType']} | "
                f"{instance['State']['Name']} | "
                f"{cost:.2f} USD"
            )

        print(f"\n[SUMMARY] Szacowany koszt: {total_cost:.2f} USD")
        return total_cost


if __name__ == "__main__":
    try:
        calculator = AWSCostCalculator()
        calculator.generate_report()

    except NoCredentialsError:
        print("[ERROR] Brak danych uwierzytelniaj─ůcych AWS.")

    except ClientError as exc:
        print(
            f"[AWS ERROR] "
            f"{exc.response['Error'].get('Message', 'Nieznany b┼é─ůd')}"
        )

    except BotoCoreError as exc:
        print(f"[ERROR] B┼é─ůd komunikacji z AWS: {exc}")
