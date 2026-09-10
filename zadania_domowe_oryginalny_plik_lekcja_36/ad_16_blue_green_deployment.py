import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class BlueGreenDeployer:
    """Implementuje blue-green deployment z dwoma Auto Scaling Groups i jednym Target Group."""

    def __init__(self, region: str = "eu-central-1") -> None:
        self.autoscaling = boto3.client("autoscaling", region_name=region)
        self.elbv2 = boto3.client("elbv2", region_name=region)

    def get_active_environment(
        self,
        target_group_arn: str,
        blue_asg_name: str,
        green_asg_name: str,
    ) -> str:
        """Sprawdza, które środowisko (blue/green) jest aktualnie podłączone do Target Group."""
        response = self.elbv2.describe_target_health(TargetGroupArn=target_group_arn)
        registered_instance_ids = {t["Target"]["Id"] for t in response["TargetHealthDescriptions"]}

        blue_instances = self._get_asg_instance_ids(blue_asg_name)
        green_instances = self._get_asg_instance_ids(green_asg_name)

        if registered_instance_ids & set(blue_instances):
            return "blue"
        if registered_instance_ids & set(green_instances):
            return "green"

        return "none"

    def _get_asg_instance_ids(self, asg_name: str) -> list[str]:
        response = self.autoscaling.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name],
        )

        instances = response["AutoScalingGroups"][0]["Instances"]
        return [instance["InstanceId"] for instance in instances]

    def deploy_to_inactive_environment(
        self,
        target_group_arn: str,
        blue_asg_name: str,
        green_asg_name: str,
        new_launch_template_version: str = "$Latest",
    ) -> str:
        """Deployuje nową wersję do nieaktywnego środowiska (bez przełączania ruchu)."""
        active_environment = self.get_active_environment(
            target_group_arn, blue_asg_name, green_asg_name,
        )

        inactive_asg_name = green_asg_name if active_environment == "blue" else blue_asg_name

        print(f"[INFO] Aktywne środowisko: {active_environment}")
        print(f"[RUN] Deployment do nieaktywnego środowiska: {inactive_asg_name}")

        self.autoscaling.start_instance_refresh(
            AutoScalingGroupName=inactive_asg_name,
            Preferences={"MinHealthyPercentage": 0, "InstanceWarmup": 60},
        )

        waiter = self.autoscaling.get_waiter("group_in_service")
        waiter.wait(AutoScalingGroupNames=[inactive_asg_name])

        print(f"[OK] Nowa wersja wdrożona w: {inactive_asg_name}")

        return inactive_asg_name

    def validate_health(self, asg_name: str) -> bool:
        """Sprawdza, czy wszystkie instancje w podanym ASG są zdrowe."""
        response = self.autoscaling.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name],
        )

        instances = response["AutoScalingGroups"][0]["Instances"]

        if not instances:
            return False

        return all(
            instance["HealthStatus"] == "Healthy" and instance["LifecycleState"] == "InService"
            for instance in instances
        )

    def switch_traffic(
        self,
        target_group_arn: str,
        new_asg_name: str,
        old_asg_name: str,
    ) -> None:
        """Przełącza ruch: rejestruje instancje z nowego ASG, wyrejestrowuje ze starego."""
        new_instance_ids = self._get_asg_instance_ids(new_asg_name)
        old_instance_ids = self._get_asg_instance_ids(old_asg_name)

        self.elbv2.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[{"Id": instance_id} for instance_id in new_instance_ids],
        )

        waiter = self.elbv2.get_waiter("target_in_service")
        waiter.wait(TargetGroupArn=target_group_arn)

        print(f"[OK] Ruch przełączony na: {new_asg_name}")

        self.elbv2.deregister_targets(
            TargetGroupArn=target_group_arn,
            Targets=[{"Id": instance_id} for instance_id in old_instance_ids],
        )

        print(f"[OK] Wyrejestrowano stare środowisko: {old_asg_name}")

    def rollback(
        self,
        target_group_arn: str,
        current_asg_name: str,
        previous_asg_name: str,
    ) -> None:
        """Natychmiastowy rollback: przełącza ruch z powrotem na poprzednie środowisko."""
        print(f"[ROLLBACK] Przywracanie ruchu na: {previous_asg_name}")
        self.switch_traffic(target_group_arn, previous_asg_name, current_asg_name)

    def deploy(
        self,
        target_group_arn: str,
        blue_asg_name: str,
        green_asg_name: str,
    ) -> None:
        """Pełny proces blue-green deployment z walidacją i możliwością rollbacku."""
        print("=== BLUE-GREEN DEPLOYMENT ===")

        active_environment = self.get_active_environment(
            target_group_arn, blue_asg_name, green_asg_name,
        )
        old_asg_name = blue_asg_name if active_environment == "blue" else green_asg_name

        new_asg_name = self.deploy_to_inactive_environment(
            target_group_arn, blue_asg_name, green_asg_name,
        )

        print("[RUN] Walidacja zdrowia nowego środowiska...")
        time.sleep(30)

        if not self.validate_health(new_asg_name):
            print("[ERROR] Nowe środowisko niezdrowe - deployment przerwany, bez przełączenia ruchu.")
            return

        print("[OK] Nowe środowisko zdrowe - przełączanie ruchu.")

        self.switch_traffic(target_group_arn, new_asg_name, old_asg_name)

        print(f"\n[SUCCESS] Deployment zakończony. Aktywne środowisko: {new_asg_name}")
        print(f"[INFO] Poprzednie środowisko ({old_asg_name}) dostępne do natychmiastowego rollbacku.")


if __name__ == "__main__":
    deployer = BlueGreenDeployer(region="eu-central-1")

    TARGET_GROUP_ARN = "arn:aws:elasticloadbalancing:eu-central-1:123456789:targetgroup/lesson36-tg/abc123"
    BLUE_ASG = "lesson36-asg-blue"
    GREEN_ASG = "lesson36-asg-green"

    try:
        deployer.deploy(
            target_group_arn=TARGET_GROUP_ARN,
            blue_asg_name=BLUE_ASG,
            green_asg_name=GREEN_ASG,
        )

    except (ClientError, BotoCoreError) as exc:
        print(f"[ERROR] {exc}")