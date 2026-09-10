import json

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class MonitoringSetup:
    """Konfiguruje kompletny monitoring: logi, custom metrics, alarmy, SNS, Slack, dashboard."""

    def __init__(self, region: str = "eu-central-1") -> None:
        self.region = region
        self.logs = boto3.client("logs", region_name=region)
        self.cloudwatch = boto3.client("cloudwatch", region_name=region)
        self.sns = boto3.client("sns", region_name=region)
        self.lambda_client = boto3.client("lambda", region_name=region)
        self.iam = boto3.client("iam", region_name=region)

    def create_log_group(self, log_group_name: str, retention_days: int = 30) -> None:
        """Tworzy CloudWatch Log Group dla logów aplikacji."""
        try:
            self.logs.create_log_group(logGroupName=log_group_name)
        except self.logs.exceptions.ResourceAlreadyExistsException:
            print(f"[INFO] Log Group już istnieje: {log_group_name}")

        self.logs.put_retention_policy(
            logGroupName=log_group_name,
            retentionInDays=retention_days,
        )

        print(f"[OK] Log Group gotowy: {log_group_name} (retencja: {retention_days} dni)")

    def publish_custom_metric(
        self,
        namespace: str,
        metric_name: str,
        value: float,
        unit: str = "Count",
    ) -> None:
        """Publikuje wartość custom metric (request rate, error rate, latency)."""
        self.cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Value": value,
                    "Unit": unit,
                }
            ],
        )

    def create_sns_topic(self, topic_name: str, email: str | None = None) -> str:
        """Tworzy SNS topic i opcjonalnie subskrybuje adres email."""
        response = self.sns.create_topic(Name=topic_name)
        topic_arn = response["TopicArn"]

        if email:
            self.sns.subscribe(
                TopicArn=topic_arn,
                Protocol="email",
                Endpoint=email,
            )
            print(f"[INFO] Subskrypcja email wysłana do: {email} (wymaga potwierdzenia)")

        print(f"[OK] SNS Topic utworzony: {topic_arn}")

        return topic_arn

    def create_slack_notifier_lambda(
        self,
        function_name: str,
        slack_webhook_url: str,
        lambda_role_arn: str,
        sns_topic_arn: str,
    ) -> str:
        """
        Tworzy funkcję Lambda, która odbiera powiadomienia z SNS
        i przekazuje je na Slacka przez webhook.
        """
        lambda_code = f'''
import json
import urllib.request

SLACK_WEBHOOK_URL = "{slack_webhook_url}"


def handler(event, context):
    for record in event["Records"]:
        message = record["Sns"]["Message"]
        subject = record["Sns"].get("Subject", "AWS Alert")

        slack_payload = {{
            "text": f"*{{subject}}*\\n{{message}}"
        }}

        request = urllib.request.Request(
            SLACK_WEBHOOK_URL,
            data=json.dumps(slack_payload).encode("utf-8"),
            headers={{"Content-Type": "application/json"}},
        )

        urllib.request.urlopen(request)

    return {{"statusCode": 200}}
'''

        import io
        import zipfile

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zip_file:
            zip_file.writestr("lambda_function.py", lambda_code)
        buffer.seek(0)

        response = self.lambda_client.create_function(
            FunctionName=function_name,
            Runtime="python3.12",
            Role=lambda_role_arn,
            Handler="lambda_function.handler",
            Code={"ZipFile": buffer.read()},
            Timeout=10,
            Description="Przekazuje powiadomienia SNS na Slacka",
        )

        function_arn = response["FunctionArn"]

        self.lambda_client.add_permission(
            FunctionName=function_name,
            StatementId="sns-invoke-permission",
            Action="lambda:InvokeFunction",
            Principal="sns.amazonaws.com",
            SourceArn=sns_topic_arn,
        )

        self.sns.subscribe(
            TopicArn=sns_topic_arn,
            Protocol="lambda",
            Endpoint=function_arn,
        )

        print(f"[OK] Lambda Slack notifier utworzona: {function_name}")
        print(f"[OK] Subskrybowana do SNS topic: {sns_topic_arn}")

        return function_arn

    def create_cpu_alarm(
        self,
        alarm_name: str,
        instance_id: str,
        sns_topic_arn: str,
        threshold: float = 80.0,
        evaluation_minutes: int = 5,
    ) -> None:
        """Alarm: CPU > threshold przez evaluation_minutes."""
        self.cloudwatch.put_metric_alarm(
            AlarmName=alarm_name,
            ComparisonOperator="GreaterThanThreshold",
            EvaluationPeriods=evaluation_minutes,
            MetricName="CPUUtilization",
            Namespace="AWS/EC2",
            Period=60,
            Statistic="Average",
            Threshold=threshold,
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            ActionsEnabled=True,
            AlarmActions=[sns_topic_arn],
            AlarmDescription=f"CPU powyżej {threshold}% przez {evaluation_minutes} minut",
        )

        print(f"[OK] Alarm CPU utworzony: {alarm_name} (próg: {threshold}%)")

    def create_error_rate_alarm(
        self,
        alarm_name: str,
        namespace: str,
        sns_topic_arn: str,
        threshold_percent: float = 5.0,
    ) -> None:
        """Alarm: error rate > threshold_percent."""
        self.cloudwatch.put_metric_alarm(
            AlarmName=alarm_name,
            ComparisonOperator="GreaterThanThreshold",
            EvaluationPeriods=1,
            MetricName="ErrorRate",
            Namespace=namespace,
            Period=60,
            Statistic="Average",
            Threshold=threshold_percent,
            ActionsEnabled=True,
            AlarmActions=[sns_topic_arn],
            AlarmDescription=f"Error rate powyżej {threshold_percent}%",
        )

        print(f"[OK] Alarm error rate utworzony: {alarm_name} (próg: {threshold_percent}%)")

    def create_latency_alarm(
        self,
        alarm_name: str,
        namespace: str,
        sns_topic_arn: str,
        threshold_seconds: float = 2.0,
    ) -> None:
        """Alarm: latency > threshold_seconds."""
        self.cloudwatch.put_metric_alarm(
            AlarmName=alarm_name,
            ComparisonOperator="GreaterThanThreshold",
            EvaluationPeriods=1,
            MetricName="Latency",
            Namespace=namespace,
            Period=60,
            Statistic="Average",
            Threshold=threshold_seconds,
            ActionsEnabled=True,
            AlarmActions=[sns_topic_arn],
            AlarmDescription=f"Latency powyżej {threshold_seconds}s",
        )

        print(f"[OK] Alarm latency utworzony: {alarm_name} (próg: {threshold_seconds}s)")

    def create_dashboard(
        self,
        dashboard_name: str,
        instance_id: str,
        namespace: str,
    ) -> None:
        """Tworzy CloudWatch Dashboard z kluczowymi metrykami."""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "x": 0, "y": 0, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [["AWS/EC2", "CPUUtilization", "InstanceId", instance_id]],
                        "period": 60,
                        "stat": "Average",
                        "region": self.region,
                        "title": "CPU Utilization",
                    },
                },
                {
                    "type": "metric",
                    "x": 12, "y": 0, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [[namespace, "ErrorRate"]],
                        "period": 60,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Error Rate",
                    },
                },
                {
                    "type": "metric",
                    "x": 0, "y": 6, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [[namespace, "Latency"]],
                        "period": 60,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Latency",
                    },
                },
                {
                    "type": "metric",
                    "x": 12, "y": 6, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [[namespace, "RequestRate"]],
                        "period": 60,
                        "stat": "Sum",
                        "region": self.region,
                        "title": "Request Rate",
                    },
                },
            ]
        }

        self.cloudwatch.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=json.dumps(dashboard_body),
        )

        print(f"[OK] Dashboard utworzony: {dashboard_name}")

    def setup_full_monitoring(
        self,
        app_name: str,
        instance_id: str,
        notification_email: str,
        slack_webhook_url: str,
        lambda_role_arn: str,
    ) -> None:
        """Pełny setup monitoringu: logi, SNS, Slack, alarmy, dashboard."""
        print("=== MONITORING I ALERTING SETUP ===")

        namespace = f"Lesson36/{app_name}"

        self.create_log_group(f"/lesson36/{app_name}")

        topic_arn = self.create_sns_topic(
            topic_name=f"{app_name}-alerts",
            email=notification_email,
        )

        self.create_slack_notifier_lambda(
            function_name=f"{app_name}-slack-notifier",
            slack_webhook_url=slack_webhook_url,
            lambda_role_arn=lambda_role_arn,
            sns_topic_arn=topic_arn,
        )

        self.create_cpu_alarm(
            alarm_name=f"{app_name}-high-cpu",
            instance_id=instance_id,
            sns_topic_arn=topic_arn,
        )

        self.create_error_rate_alarm(
            alarm_name=f"{app_name}-high-error-rate",
            namespace=namespace,
            sns_topic_arn=topic_arn,
        )

        self.create_latency_alarm(
            alarm_name=f"{app_name}-high-latency",
            namespace=namespace,
            sns_topic_arn=topic_arn,
        )

        self.create_dashboard(
            dashboard_name=f"{app_name}-dashboard",
            instance_id=instance_id,
            namespace=namespace,
        )

        print(f"\n[SUCCESS] Monitoring skonfigurowany dla: {app_name}")


if __name__ == "__main__":
    monitoring = MonitoringSetup(region="eu-central-1")

    try:
        monitoring.setup_full_monitoring(
            app_name="lesson36-app",
            instance_id="i-xxxxxxxxxxxxxxxxx",
            notification_email="admin@example.com",
            slack_webhook_url="https://hooks.slack.com/services/XXX/YYY/ZZZ",
            lambda_role_arn="arn:aws:iam::123456789:role/lesson36-lambda-slack-role",
        )

    except (ClientError, BotoCoreError) as exc:
        print(f"[ERROR] {exc}")