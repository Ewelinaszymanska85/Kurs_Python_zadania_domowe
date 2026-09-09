import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


def list_aws_regions() -> None:
    """Pobiera i wy┼Ťwietla dost─Öpne regiony AWS EC2 wraz z endpointami."""
    try:
        ec2 = boto3.client("ec2", region_name="eu-central-1")

        response = ec2.describe_regions(AllRegions=True)
        regions = sorted(
            response["Regions"],
            key=lambda region: region["RegionName"],
        )

        print("=== AWS REGIONS ===")
        print(f"Liczba region├│w: {len(regions)}\n")

        for number, region in enumerate(regions, start=1):
            name = region["RegionName"]
            endpoint = region.get("Endpoint", "brak endpointu")
            status = region.get("OptInStatus", "unknown")

            print(f"{number:02}. {name:<20} | {endpoint:<35} | status: {status}")

    except NoCredentialsError:
        print("[ERROR] Nie znaleziono danych logowania AWS.")

    except ClientError as exc:
        print(f"[AWS ERROR] {exc.response['Error']['Message']}")

    except BotoCoreError as exc:
        print(f"[ERROR] B┼é─ůd boto3: {exc}")


if __name__ == "__main__":
    list_aws_regions()
