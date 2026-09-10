import time

import boto3
import requests
from botocore.exceptions import BotoCoreError, ClientError


class ZeroDowntimeDeployer:
    """Zarządza zero-downtime deploymentem przez Auto Scaling Group z rolling update."""

    def __init__(self, region: str = "eu-central-1") -> None:
        self.autoscaling = boto3.client("autoscaling", region_name=region)
        self.ec2 = boto3.client("ec2", region_name=region)
        self.elbv2 = boto3.client("elbv2", region_name=region)

    def create_launch_template(
        self,
        template_name: str,
        ami_id: str,
        instance_type: str,
        security_group_ids: list[str],
        user_data_script: str,
    ) -> str:
        """Tworzy Launch Template z user data script."""
        import base64

        encoded_user_data = base64.b64encode(
            user_data_script.encode("utf-8")
        ).decode("utf-8")

        response = self.ec2.create_launch_template(
            LaunchTemplateName=template_name,
            LaunchTemplateData={
                "ImageId": ami_id,
                "InstanceType": instance_type,
                "SecurityGroupIds": security_group_ids,
                "UserData": encoded_user_data,
            },
        )

        template_id = response["LaunchTemplate"]["LaunchTemplateId"]

        print(f"[OK] Utworzono Launch Template: {template_name} ({template_id})")

        return template_id

    def create_auto_scaling_group(
        self,
        asg_name: str,
        launch_template_id: str,
        subnet_ids: list[str],
        target_group_arn: str,
        min_size: int = 2,
        max_size: int = 4,
    ) -> None:
        """Tworzy Auto Scaling Group z minimum 2 instancjami i health checkiem z ALB."""
        self.autoscaling.create_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            LaunchTemplate={
                "LaunchTemplateId": launch_template_id,
                "Version": "$Latest",
            },
            MinSize=min_size,
            MaxSize=max_size,
            DesiredCapacity=min_size,
            VPCZoneIdentifier=",".join(subnet_ids),
            TargetGroupARNs=[target_group_arn],
            HealthCheckType="ELB",
            HealthCheckGracePeriod=120,
        )

        waiter = self.autoscaling.get_waiter("group_in_service")
        waiter.wait(AutoScalingGroupNames=[asg_name])

        print(f"[OK] Auto Scaling Group utworzony: {asg_name} (min={min_size}, max={max_size})")

    def start_rolling_update(
        self,
        asg_name: str,
        new_launch_template_version: str,
        min_healthy_percentage: int = 50,
    ) -> str:
        """Uruchamia rolling update ASG do nowej wersji Launch Template."""
        response = self.autoscaling.start_instance_refresh(
            AutoScalingGroupName=asg_name,
            Preferences={
                "MinHealthyPercentage": min_healthy_percentage,
                "InstanceWarmup": 120,
            },
        )

        refresh_id = response["InstanceRefreshId"]

        print(f"[OK] Rozpoczęto rolling update: {refresh_id}")
        print(f"[INFO] MinHealthyPercentage: {min_healthy_percentage}%")

        return refresh_id

    def monitor_refresh(
        self,
        asg_name: str,
        refresh_id: str,
        poll_interval: int = 15,
    ) -> str:
        """Śledzi postęp instance refresh aż do zakończenia lub błędu."""
        print("[WAIT] Monitorowanie postępu deploymentu...")

        while True:
            response = self.autoscaling.describe_instance_refreshes(
                AutoScalingGroupName=asg_name,
                InstanceRefreshIds=[refresh_id],
            )

            refresh = response["InstanceRefreshes"][0]
            status = refresh["Status"]
            percentage = refresh.get("PercentageComplete", 0)

            print(f"[STATUS] {status} | {percentage}% ukończone")

            if status in ("Successful", "Failed", "Cancelled"):
                return status

            time.sleep(poll_interval)

    def rollback(self, asg_name: str, refresh_id: str) -> None:
        """Anuluje trwający instance refresh, przywracając poprzednią wersję."""
        print("[ROLLBACK] Anulowanie deploymentu...")

        self.autoscaling.cancel_instance_refresh(AutoScalingGroupName=asg_name)

        waiter_status = self.monitor_refresh(asg_name, refresh_id)

        print(f"[OK] Rollback zakończony ze statusem: {waiter_status}")

    def check_target_health(self, target_group_arn: str) -> bool:
        """Sprawdza, czy wszystkie targety w Target Group są zdrowe."""
        response = self.elbv2.describe_target_health(TargetGroupArn=target_group_arn)

        targets = response["TargetHealthDescriptions"]

        if not targets:
            return False

        return all(
            target["TargetHealth"]["State"] == "healthy"
            for target in targets
        )

    def deploy(
        self,
        asg_name: str,
        target_group_arn: str,
        health_check_url: str,
        min_healthy_percentage: int = 50,
    ) -> None:
        """Pełny proces deploymentu z monitoringiem downtime i auto-rollbackiem."""
        print("=== ZERO-DOWNTIME DEPLOYMENT ===")

        deployment_start = time.time()
        downtime_detected = False

        refresh_id = self.start_rolling_update(asg_name, "$Latest", min_healthy_percentage)

        while True:
            response = self.autoscaling.describe_instance_refreshes(
                AutoScalingGroupName=asg_name,
                InstanceRefreshIds=[refresh_id],
            )
            refresh = response["InstanceRefreshes"][0]
            status = refresh["Status"]

            print(f"[STATUS] {status} | {refresh.get('PercentageComplete', 0)}%")

            try:
                response = requests.get(health_check_url, timeout=3)
                if response.status_code != 200:
                    downtime_detected = True
                    print(f"[DOWNTIME] Health check zwrócił {response.status_code}")
            except requests.RequestException:
                downtime_detected = True
                print("[DOWNTIME] Health check niedostępny")

            if status == "Successful":
                break

            if status in ("Failed", "Cancelled"):
                print("[ERROR] Rolling update nie powiódł się - uruchamiam rollback.")
                self.rollback(asg_name, refresh_id)