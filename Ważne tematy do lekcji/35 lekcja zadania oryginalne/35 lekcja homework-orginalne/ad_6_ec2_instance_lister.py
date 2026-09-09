import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from collections import Counter


def list_ec2_instances(region: str = "eu-central-1") -> list[dict]:
    """Pobiera i wyświetla podstawowe informacje o instancjach EC2."""
    ec2 = boto3.client("ec2", region_name=region)

    try:
        response = ec2.describe_instances()

        instances = []

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                info = {
                    "id": instance.get("InstanceId"),
                    "type": instance.get("InstanceType"),
                    "state": instance.get("State", {}).get("Name"),
                    "public_ip": instance.get("PublicIpAddress", "brak"),
                }
                instances.append(info)

        print(f"=== EC2 INSTANCES | REGION: {region} ===")

        if not instances:
            print("[INFO] Brak instancji EC2.")
            return []

        for number, instance in enumerate(instances, start=1):
            print(
                f"{number}. ID: {instance['id']} | "
                f"Type: {instance['type']} | "
                f"State: {instance['state']} | "
                f"Public IP: {instance['public_ip']}"
            )

        state_counts = Counter(instance["state"] for instance in instances)
        summary = ", ".join(f"{state}: {count}" for state, count in state_counts.items())

        print(f"\n[SUMMARY] Liczba instancji: {len(instances)} ({summary})")
        return instances

    except NoCredentialsError:
        print("[ERROR] Brak skonfigurowanych danych logowania AWS.")
        return []

    except ClientError as exc:
        message = exc.response["Error"].get("Message", "Nieznany błąd")
        print(f"[AWS ERROR] {message}")
        return []

    except BotoCoreError as exc:
        print(f"[ERROR] Błąd boto3: {exc}")
        return []


if __name__ == "__main__":
    list_ec2_instances()