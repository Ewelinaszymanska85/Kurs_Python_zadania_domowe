import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class CustomMetricAutoScaler:
    """Publikuje custom metric do CloudWatch i konfiguruje Auto Scaling na jej podstawie."""

    def __init__(self, region: str = "eu-central-1") -> None:
        self.cloudwatch = boto3.client("cloudwatch", region_name=region)
        self.autoscaling = boto3.client("autoscaling", region_name=region)

    def publish_active_connections_metric(
        self,
        namespace: str,
        metric_name: str,
        active_connections: int,
    ) -> None:
        """Publikuje wartość metryki 'active connections' do CloudWatch."""
        self.cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Value": active_connections,
                    "Unit": "Count",
                }
            ],
        )

        print(f"[METRIC] {metric_name}: {active_connections} ({namespace})")

    def create_scaling_policies(
        self,
        asg_name: str,
        namespace: str,
        metric_name: str,
        scale_out_threshold: int = 100,
        scale_in_threshold: int = 20,
    ) -> tuple[str, str]:
        """Tworzy dwie step scaling policy: scale out i scale in bazujące na custom metric."""
        scale_out_response = self.autoscaling.put_scaling_policy(
            AutoScalingGroupName=asg_name,
            PolicyName=f"{asg_name}-scale-out",
            PolicyType="StepScaling",
            AdjustmentType="ChangeInCapacity",
            StepAdjustments=[
                {
                    "MetricIntervalLowerBound": 0,
                    "ScalingAdjustment": 1,
                },
            ],
        )
        scale_out_policy_arn = scale_out_response["PolicyARN"]

        scale_in_response = self.autoscaling.put_scaling_policy(
            AutoScalingGroupName=asg_name,
            PolicyName=f"{asg_name}-scale-in",
            PolicyType="StepScaling",
            AdjustmentType="ChangeInCapacity",
            StepAdjustments=[
                {
                    "MetricIntervalUpperBound": 0,
                    "ScalingAdjustment": -1,
                },
            ],
        )
        scale_in_policy_arn = scale_in_response["PolicyARN"]

        self.cloudwatch.put_metric_alarm(
            AlarmName=f"{asg_name}-high-connections",
            ComparisonOperator="GreaterThanThreshold",
            EvaluationPeriods=2,
            MetricName=metric_name,
            Namespace=namespace,
            Period=60,
            Statistic="Average",
            Threshold=scale_out_threshold,
            ActionsEnabled=True,
            AlarmActions=[scale_out_policy_arn],
        )

        self.cloudwatch.put_metric_alarm(
            AlarmName=f"{asg_name}-low-connections",
            ComparisonOperator="LessThanThreshold",
            EvaluationPeriods=2,
            MetricName=metric_name,
            Namespace=namespace,
            Period=60,
            Statistic="Average",
            Threshold=scale_in_threshold,
            ActionsEnabled=True,
            AlarmActions=[scale_in_policy_arn],
        )

        print(f"[OK] Scale out: connections > {scale_out_threshold} -> +1 instancja")
        print(f"[OK] Scale in: connections < {scale_in_threshold} -> -1 instancja")

        return scale_out_policy_arn, scale_in_policy_arn

    def run_metric_publisher_loop(
        self,
        namespace: str,
        metric_name: str,
        get_connections_count: callable,
        interval_seconds: int = 60,
    ) -> None:
        """Pętla publikująca metrykę co interval_seconds (domyślnie co minutę)."""
        print(f"=== PUBLIKOWANIE METRYKI CO {interval_seconds}s ===")

        while True:
            connections = get_connections_count()
            self.publish_active_connections_metric(namespace, metric_name, connections)
            time.sleep(interval_seconds)


def get_active_connections_from_app() -> int:
    """
    Placeholder - w prawdziwej aplikacji to powinno odpytywać
    faktyczny licznik połączeń (np. endpoint /metrics aplikacji).
    """
    import random
    return random.randint(0, 150)


if __name__ == "__main__":
    scaler = CustomMetricAutoScaler(region="eu-central-1")

    NAMESPACE = "Lesson36/CustomApp"
    METRIC_NAME = "ActiveConnections"
    ASG_NAME = "lesson36-asg"

    try:
        scaler.create_scaling_policies(
            asg_name=ASG_NAME,
            namespace=NAMESPACE,
            metric_name=METRIC_NAME,
            scale_out_threshold=100,
            scale_in_threshold=20,
        )

        scaler.run_metric_publisher_loop(
            namespace=NAMESPACE,
            metric_name=METRIC_NAME,
            get_connections_count=get_active_connections_from_app,
            interval_seconds=60,
        )

    except (ClientError, BotoCoreError) as exc:
        print(f"[ERROR] {exc}")