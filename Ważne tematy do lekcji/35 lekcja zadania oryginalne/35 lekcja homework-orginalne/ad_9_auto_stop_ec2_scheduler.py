import logging

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def get_tag_value(tags: list[dict] | None, key: str) -> str | None:
    """Zwraca wartość wskazanego taga EC2."""
    if not tags:
        return None

    for tag in tags:
        if tag.get("Key") == key:
            return tag.get("Value")

    return None


def auto_stop_instances(region: str = "eu-central-1") -> list[str]:
    """
    Zatrzymuje działające instancje EC2 oznaczone tagiem AutoStop=true.
    """
    ec2 = boto3.client("ec2", region_name=region)

    stopped_instances = []

    logging.info("Uruchamiam scheduler AutoStop | region=%s", region)

    try:
        response = ec2.describe_instances(
            Filters=[
                {
                    "Name": "instance-state-name",
                    "Values": ["running"],
                }
            ]
        )

        print("=== EC2 AUTO STOP SCHEDULER ===")

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance["InstanceId"]
                auto_stop = get_tag_value(
                    instance.get("Tags"),
                    "AutoStop",
                )

                if str(auto_stop).lower() != "true":
                    logging.info(
                        "Pomijam %s | AutoStop=%s",
                        instance_id,
                        auto_stop,
                    )
                    continue

                ec2.stop_instances(
                    InstanceIds=[instance_id],
                )

                stopped_instances.append(instance_id)

                logging.info(
                    "Zatrzymuję instancję %s | AutoStop=true",
                    instance_id,
                )

                print(
                    f"[STOP] {instance_id} | AutoStop=true"
                )

        logging.info(
            "Scheduler zakończony | zatrzymano %d instancji",
            len(stopped_instances),
        )

        print(
            f"[SUMMARY] Zatrzymano instancji: "
            f"{len(stopped_instances)}"
        )

        return stopped_instances

    except NoCredentialsError:
        logging.error("Brak danych uwierzytelniających AWS.")
        print("[ERROR] Brak danych uwierzytelniających AWS.")

    except ClientError as exc:
        message = exc.response["Error"].get(
            "Message",
            "Nieznany błąd AWS",
        )
        logging.error("Błąd AWS: %s", message)
        print(f"[AWS ERROR] {message}")

    except BotoCoreError as exc:
        logging.error("Błąd komunikacji z AWS: %s", exc)
        print(f"[ERROR] Błąd komunikacji z AWS: {exc}")

    return []


if __name__ == "__main__":
    auto_stop_instances()