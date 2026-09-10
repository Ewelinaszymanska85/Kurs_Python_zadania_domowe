import boto3
from botocore.exceptions import BotoCoreError, ClientError


def create_web_security_group(
    vpc_id: str,
    group_name: str = "web-sg",
    region: str = "eu-central-1",
) -> str:
    """Tworzy Security Group zezwalającą tylko na HTTP i HTTPS z internetu."""
    ec2 = boto3.client("ec2", region_name=region)

    response = ec2.create_security_group(
        GroupName=group_name,
        Description="Zezwala na HTTP i HTTPS z internetu, blokuje reszte.",
        VpcId=vpc_id,
    )

    security_group_id = response["GroupId"]

    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 80,
                "ToPort": 80,
                "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "HTTP"}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 443,
                "ToPort": 443,
                "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "HTTPS"}],
            },
        ],
    )

    print(f"[OK] Utworzono Security Group: {security_group_id}")
    print("[INFO] Otwarte porty: 80 (HTTP), 443 (HTTPS)")
    print("[INFO] Wszystkie inne porty domyślnie zablokowane.")

    return security_group_id


if __name__ == "__main__":
    try:
        create_web_security_group(
            vpc_id="vpc-xxxxxxxxxxxxxxxxx",
        )

    except (ClientError, BotoCoreError) as exc:
        print(f"[ERROR] {exc}")