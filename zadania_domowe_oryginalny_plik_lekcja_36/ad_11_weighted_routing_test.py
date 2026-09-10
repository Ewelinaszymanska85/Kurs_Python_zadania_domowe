from collections import Counter

import boto3
import dns.resolver
from botocore.exceptions import BotoCoreError, ClientError


def setup_weighted_routing(
    hosted_zone_id: str,
    subdomain: str,
    primary_endpoint: str,
    canary_endpoint: str,
    primary_weight: int = 80,
    canary_weight: int = 20,
) -> None:
    """Konfiguruje weighted routing w Route53: primary vs canary."""
    route53 = boto3.client("route53")

    changes = [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": subdomain,
                "Type": "CNAME",
                "SetIdentifier": "primary",
                "Weight": primary_weight,
                "TTL": 60,
                "ResourceRecords": [{"Value": primary_endpoint}],
            },
        },
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": subdomain,
                "Type": "CNAME",
                "SetIdentifier": "canary",
                "Weight": canary_weight,
                "TTL": 60,
                "ResourceRecords": [{"Value": canary_endpoint}],
            },
        },
    ]

    route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={"Changes": changes},
    )

    print(f"[OK] Weighted routing skonfigurowany dla {subdomain}")
    print(f"[INFO] Primary ({primary_weight}%): {primary_endpoint}")
    print(f"[INFO] Canary ({canary_weight}%): {canary_endpoint}")


def test_weighted_distribution(
    subdomain: str,
    num_requests: int = 100,
    dns_server: str = "8.8.8.8",
) -> dict[str, int]:
    """
    Odpytuje bezpośrednio serwer DNS (z pominięciem cache) i zlicza,
    który endpoint (CNAME) został zwrócony przez Route53 weighted routing.
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    resolver.cache = None  # wyłącz cache, każde zapytanie ma trafić do Route53

    results = Counter()

    for i in range(num_requests):
        try:
            answer = resolver.resolve(subdomain, "CNAME")
            resolved_target = str(answer[0].target).rstrip(".")
            results[resolved_target] += 1

        except dns.resolver.NXDOMAIN:
            results["nxdomain"] += 1

        except dns.exception.DNSException as exc:
            results["error"] += 1
            print(f"[ERROR] Zapytanie {i + 1}: {exc}")

    print("\n=== WYNIK ROZKŁADU RUCHU (DNS) ===")

    for endpoint, count in results.items():
        percentage = (count / num_requests) * 100
        print(f"{endpoint}: {count}/{num_requests} ({percentage:.1f}%)")

    return dict(results)


if __name__ == "__main__":
    try:
        setup_weighted_routing(
            hosted_zone_id="Z1234567890ABC",
            subdomain="app.yourdomain.com",
            primary_endpoint="primary-alb-123456.eu-central-1.elb.amazonaws.com",
            canary_endpoint="canary-alb-654321.eu-central-1.elb.amazonaws.com",
        )

        print("\n[INFO] Poczekaj kilka sekund na propagację rekordów w Route53.\n")

        test_weighted_distribution(
            subdomain="app.yourdomain.com",
            num_requests=100,
        )

    except (ClientError, BotoCoreError) as exc:
        print(f"[ERROR] {exc}")