import boto3
import requests
from botocore.exceptions import BotoCoreError, ClientError


class ApplicationLoadBalancerSetup:
    """Tworzy kompletny setup ALB: load balancer, target group, listener, rejestracja instancji."""

    def __init__(self, region: str = "eu-central-1") -> None:
        self.elbv2 = boto3.client("elbv2", region_name=region)

    def create_load_balancer(
        self,
        name: str,
        subnet_ids: list[str],
        security_group_ids: list[str],
    ) -> str:
        """Tworzy ALB w podanych subnetach (min. 2, w różnych AZ)."""
        if len(subnet_ids) < 2:
            raise ValueError("ALB wymaga co najmniej 2 subnetów w różnych AZ.")

        response = self.elbv2.create_load_balancer(
            Name=name,
            Subnets=subnet_ids,
            SecurityGroups=security_group_ids,
            Scheme="internet-facing",
            Type="application",
            IpAddressType="ipv4",
        )

        load_balancer_arn = response["LoadBalancers"][0]["LoadBalancerArn"]
        dns_name = response["LoadBalancers"][0]["DNSName"]

        print(f"[OK] Utworzono ALB: {name}")
        print(f"[INFO] DNS: {dns_name}")

        return load_balancer_arn

    def create_target_group(
        self,
        name: str,
        vpc_id: str,
        port: int = 80,
        health_check_path: str = "/health",
    ) -> str:
        """Tworzy Target Group z health checkiem."""
        response = self.elbv2.create_target_group(
            Name=name,
            Protocol="HTTP",
            Port=port,
            VpcId=vpc_id,
            HealthCheckProtocol="HTTP",
            HealthCheckPath=health_check_path,
            HealthCheckIntervalSeconds=30,
            TargetType="instance",
        )

        target_group_arn = response["TargetGroups"][0]["TargetGroupArn"]

        print(f"[OK] Utworzono Target Group: {name}")

        return target_group_arn

    def create_listener(
        self,
        load_balancer_arn: str,
        target_group_arn: str,
        port: int = 80,
    ) -> str:
        """Tworzy listener na ALB przekazujący ruch do Target Group."""
        response = self.elbv2.create_listener(
            LoadBalancerArn=load_balancer_arn,
            Protocol="HTTP",
            Port=port,
            DefaultActions=[
                {
                    "Type": "forward",
                    "TargetGroupArn": target_group_arn,
                }
            ],
        )

        listener_arn = response["Listeners"][0]["ListenerArn"]

        print(f"[OK] Utworzono Listener na porcie {port}")

        return listener_arn

    def register_instances(
        self,
        target_group_arn: str,
        instance_ids: list[str],
    ) -> None:
        """Rejestruje instancje EC2 w Target Group."""
        self.elbv2.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[{"Id": instance_id} for instance_id in instance_ids],
        )

        print(f"[OK] Zarejestrowano {len(instance_ids)} instancje w Target Group.")

    def wait_for_healthy_targets(self, target_group_arn: str) -> None:
        """Czeka, aż zarejestrowane instancje osiągną status 'healthy'."""
        waiter = self.elbv2.get_waiter("target_in_service")
        waiter.wait(TargetGroupArn=target_group_arn)

        print("[OK] Wszystkie instancje są 'healthy'.")

    def setup(
        self,
        alb_name: str,
        target_group_name: str,
        vpc_id: str,
        subnet_ids: list[str],
        security_group_ids: list[str],
        instance_ids: list[str],
    ) -> tuple[str, str]:
        """Pełny setup: ALB + Target Group + Listener + rejestracja instancji."""
        print("=== APPLICATION LOAD BALANCER SETUP ===")

        load_balancer_arn = self.create_load_balancer(
            alb_name, subnet_ids, security_group_ids,
        )

        target_group_arn = self.create_target_group(
            target_group_name, vpc_id,
        )

        self.create_listener(load_balancer_arn, target_group_arn)

        self.register_instances(target_group_arn, instance_ids)

        self.wait_for_healthy_targets(target_group_arn)

        response = self.elbv2.describe_load_balancers(
            LoadBalancerArns=[load_balancer_arn],
        )
        dns_name = response["LoadBalancers"][0]["DNSName"]

        print(f"\n[SUCCESS] ALB gotowy: http://{dns_name}")

        return load_balancer_arn, dns_name


def test_traffic_distribution(dns_name: str, num_requests: int = 20) -> dict[str, int]:
    """Wysyła requesty do ALB i zlicza, ile trafiło do każdej instancji (po nagłówku/body)."""
    distribution: dict[str, int] = {}

    for _ in range(num_requests):
        try:
            response = requests.get(f"http://{dns_name}/health", timeout=5)
            instance_marker = response.headers.get("X-Instance-Id", "unknown")
            distribution[instance_marker] = distribution.get(instance_marker, 0) + 1

        except requests.RequestException as exc:
            print(f"[ERROR] Request nieudany: {exc}")

    print("\n=== ROZKŁAD RUCHU ===")
    for instance_id, count in distribution.items():
        print(f"{instance_id}: {count}/{num_requests} requestów")

    return distribution


if __name__ == "__main__":
    setup = ApplicationLoadBalancerSetup(region="eu-central-1")

    try:
        load_balancer_arn, dns_name = setup.setup(
            alb_name="lesson36-alb",
            target_group_name="lesson36-target-group",
            vpc_id="vpc-xxxxxxxxxxxxxxxxx",
            subnet_ids=["subnet-aaaaaaaa", "subnet-bbbbbbbb"],
            security_group_ids=["sg-xxxxxxxxxxxxxxxxx"],
            instance_ids=["i-instance1", "i-instance2"],
        )

        test_traffic_distribution(dns_name, num_requests=20)

    except (ClientError, BotoCoreError, ValueError) as exc:
        print(f"[ERROR] {exc}")