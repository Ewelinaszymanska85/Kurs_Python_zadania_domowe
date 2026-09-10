import boto3
from botocore.exceptions import BotoCoreError, ClientError


def create_target_group(
    vpc_id: str,
    target_group_name: str = "app-target-group",
    port: int = 8000,
    health_check_path: str = "/health",
    health_check_interval: int = 30,
    region: str = "eu-central-1",
) -> str:
    """Tworzy Target Group z health checkiem dla ALB."""
    elbv2 = boto3.client("elbv2", region_name=region)

    response = elbv2.create_target_group(
        Name=target_group_name,
        Protocol="HTTP",
        Port=port,
        VpcId=vpc_id,
        HealthCheckProtocol="HTTP",
        HealthCheckPath=health_check_path,
        HealthCheckIntervalSeconds=health_check_interval,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=3,
        UnhealthyThresholdCount=3,
        TargetType="instance",
    )

    target_group_arn = response["TargetGroups"][0]["TargetGroupArn"]

    print(f"[OK] Utworzono Target Group: {target_group_name}")
    print(f"[INFO] ARN: {target_group_arn}")
    print(f"[INFO] Protokol/Port: HTTP/{port}")
    print(f"[INFO] Health check: {health_check_path} co {health_check_interval}s")

    return target_group_arn


if __name__ == "__main__":
    try:
        create_target_group(
            vpc_id="vpc-xxxxxxxxxxxxxxxxx",
        )

    except (ClientError, BotoCoreError) as exc:
        print(f"[ERROR] {exc}")