import boto3
from botocore.exceptions import BotoCoreError, ClientError


def create_a_record(
    hosted_zone_id: str,
    subdomain: str,
    ip_address: str = "1.2.3.4",
    ttl: int = 300,
) -> dict:
    """Tworzy rekord A w Route53 wskazujący na podany adres IP."""
    route53 = boto3.client("route53")

    change_batch = {
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": subdomain,
                    "Type": "A",
                    "TTL": ttl,
                    "ResourceRecords": [
                        {"Value": ip_address},
                    ],
                },
            }
        ]
    }

    response = route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch=change_batch,
    )

    change_id = response["ChangeInfo"]["Id"]
    status = response["ChangeInfo"]["Status"]

    print(f"[OK] Utworzono rekord A: {subdomain} -> {ip_address} (TTL: {ttl}s)")
    print(f"[INFO] Change ID: {change_id} | Status: {status}")

    return response["ChangeInfo"]


if __name__ == "__main__":
    try:
        create_a_record(
            hosted_zone_id="Z1234567890ABC",
            subdomain="test.yourdomain.com",
            ip_address="1.2.3.4",
            ttl=300,
        )

    except (ClientError, BotoCoreError) as exc:
        print(f"[ERROR] {exc}")