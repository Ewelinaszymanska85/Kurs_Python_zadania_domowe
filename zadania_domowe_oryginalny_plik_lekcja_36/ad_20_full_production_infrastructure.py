import json

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class ProductionInfrastructureBuilder:
    """Buduje kompletną infrastrukturę produkcyjną AWS jako Infrastructure as Code."""

    def __init__(self, region: str = "eu-central-1") -> None:
        self.region = region
        self.ec2 = boto3.client("ec2", region_name=region)
        self.rds = boto3.client("rds", region_name=region)
        self.elbv2 = boto3.client("elbv2", region_name=region)
        self.autoscaling = boto3.client("autoscaling", region_name=region)
        self.route53 = boto3.client("route53")
        self.s3 = boto3.client("s3", region_name=region)
        self.cloudwatch = boto3.client("cloudwatch", region_name=region)
        self.iam = boto3.client("iam", region_name=region)
        self.secrets = boto3.client("secretsmanager", region_name=region)
        self.wafv2 = boto3.client("wafv2", region_name=region)

    # --- VPC i sieć ---

    def create_vpc_with_subnets(
        self,
        vpc_cidr: str = "10.0.0.0/16",
        availability_zones: list[str] | None = None,
    ) -> dict:
        """Tworzy VPC z publicznymi i prywatnymi subnetami w 3 AZ."""
        availability_zones = availability_zones or [
            f"{self.region}a", f"{self.region}b", f"{self.region}c",
        ]

        vpc_response = self.ec2.create_vpc(CidrBlock=vpc_cidr)
        vpc_id = vpc_response["Vpc"]["VpcId"]

        self.ec2.get_waiter("vpc_available").wait(VpcIds=[vpc_id])

        internet_gateway = self.ec2.create_internet_gateway()
        igw_id = internet_gateway["InternetGateway"]["InternetGatewayId"]
        self.ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

        public_subnets = []
        private_subnets = []

        for index, az in enumerate(availability_zones):
            public_subnet = self.ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=f"10.0.{index * 2}.0/24",
                AvailabilityZone=az,
            )
            public_subnets.append(public_subnet["Subnet"]["SubnetId"])

            private_subnet = self.ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=f"10.0.{index * 2 + 1}.0/24",
                AvailabilityZone=az,
            )
            private_subnets.append(private_subnet["Subnet"]["SubnetId"])

        route_table = self.ec2.create_route_table(VpcId=vpc_id)
        route_table_id = route_table["RouteTable"]["RouteTableId"]

        self.ec2.create_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock="0.0.0.0/0",
            GatewayId=igw_id,
        )

        for subnet_id in public_subnets:
            self.ec2.associate_route_table(RouteTableId=route_table_id, SubnetId=subnet_id)

        print(f"[OK] VPC utworzony: {vpc_id}")
        print(f"[OK] Subnety publiczne ({len(public_subnets)}): {public_subnets}")
        print(f"[OK] Subnety prywatne ({len(private_subnets)}): {private_subnets}")

        return {
            "vpc_id": vpc_id,
            "public_subnets": public_subnets,
            "private_subnets": private_subnets,
        }

    # --- IAM ---

    def create_least_privilege_role(
        self,
        role_name: str,
        service: str = "ec2.amazonaws.com",
        managed_policy_arns: list[str] | None = None,
    ) -> str:
        """Tworzy rolę IAM z minimalnym zestawem uprawnień (least privilege)."""
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": service},
                    "Action": "sts:AssumeRole",
                }
            ],
        }

        response = self.iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
        )

        role_arn = response["Role"]["Arn"]

        for policy_arn in (managed_policy_arns or []):
            self.iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)

        print(f"[OK] Rola IAM utworzona: {role_name}")

        return role_arn

    # --- Secrets Manager ---

    def store_database_credentials(
        self,
        secret_name: str,
        username: str,
        password: str,
    ) -> str:
        """Zapisuje dane dostępowe do bazy w Secrets Manager (zamiast w kodzie)."""
        secret_value = json.dumps({"username": username, "password": password})

        response = self.secrets.create_secret(
            Name=secret_name,
            SecretString=secret_value,
        )

        print(f"[OK] Dane dostępowe zapisane w Secrets Manager: {secret_name}")

        return response["ARN"]

    # --- RDS Multi-AZ z Read Replicas ---

    def create_multi_az_rds_with_replicas(
        self,
        db_identifier: str,
        secret_arn: str,
        subnet_group_name: str,
        replica_count: int = 1,
    ) -> dict:
        """Tworzy Multi-AZ RDS wraz z Read Replicas."""
        secret_value = json.loads(
            self.secrets.get_secret_value(SecretId=secret_arn)["SecretString"]
        )

        self.rds.create_db_instance(
            DBInstanceIdentifier=db_identifier,
            DBInstanceClass="db.t3.medium",
            Engine="postgres",
            MasterUsername=secret_value["username"],
            MasterUserPassword=secret_value["password"],
            AllocatedStorage=50,
            MultiAZ=True,
            DBSubnetGroupName=subnet_group_name,
            PubliclyAccessible=False,
        )

        self.rds.get_waiter("db_instance_available").wait(DBInstanceIdentifier=db_identifier)

        replica_ids = []
        for i in range(replica_count):
            replica_id = f"{db_identifier}-replica-{i + 1}"
            self.rds.create_db_instance_read_replica(
                DBInstanceIdentifier=replica_id,
                SourceDBInstanceIdentifier=db_identifier,
            )
            replica_ids.append(replica_id)

        for replica_id in replica_ids:
            self.rds.get_waiter("db_instance_available").wait(DBInstanceIdentifier=replica_id)

        print(f"[OK] RDS Multi-AZ utworzony: {db_identifier} z {replica_count} replikami")

        return {"primary": db_identifier, "replicas": replica_ids}

    # --- ALB z SSL ---

    def create_alb_with_ssl(
        self,
        alb_name: str,
        subnet_ids: list[str],
        security_group_ids: list[str],
        certificate_arn: str,
        target_group_arn: str,
    ) -> str:
        """Tworzy ALB z listenerem HTTPS (SSL) i przekierowaniem HTTP -> HTTPS."""
        alb_response = self.elbv2.create_load_balancer(
            Name=alb_name,
            Subnets=subnet_ids,
            SecurityGroups=security_group_ids,
            Scheme="internet-facing",
            Type="application",
        )
        load_balancer_arn = alb_response["LoadBalancers"][0]["LoadBalancerArn"]

        self.elbv2.create_listener(
            LoadBalancerArn=load_balancer_arn,
            Protocol="HTTPS",
            Port=443,
            Certificates=[{"CertificateArn": certificate_arn}],
            SslPolicy="ELBSecurityPolicy-TLS13-1-2-2021-06",
            DefaultActions=[{"Type": "forward", "TargetGroupArn": target_group_arn}],
        )

        self.elbv2.create_listener(
            LoadBalancerArn=load_balancer_arn,
            Protocol="HTTP",
            Port=80,
            DefaultActions=[
                {
                    "Type": "redirect",
                    "RedirectConfig": {
                        "Protocol": "HTTPS",
                        "Port": "443",
                        "StatusCode": "HTTP_301",
                    },
                }
            ],
        )

        print(f"[OK] ALB z SSL utworzony: {alb_name}")

        return load_balancer_arn

    # --- WAF ---

    def attach_waf_to_alb(self, alb_arn: str, web_acl_name: str = "lesson36-waf") -> None:
        """Tworzy WAF Web ACL z regułami AWS Managed Rules i podpina do ALB."""
        response = self.wafv2.create_web_acl(
            Name=web_acl_name,
            Scope="REGIONAL",
            DefaultAction={"Allow": {}},
            VisibilityConfig={
                "SampledRequestsEnabled": True,
                "CloudWatchMetricsEnabled": True,
                "MetricName": web_acl_name,
            },
            Rules=[
                {
                    "Name": "AWS-CommonRuleSet",
                    "Priority": 0,
                    "OverrideAction": {"None": {}},
                    "Statement": {
                        "ManagedRuleGroupStatement": {
                            "VendorName": "AWS",
                            "Name": "AWSManagedRulesCommonRuleSet",
                        }
                    },
                    "VisibilityConfig": {
                        "SampledRequestsEnabled": True,
                        "CloudWatchMetricsEnabled": True,
                        "MetricName": "CommonRuleSet",
                    },
                },
            ],
        )

        web_acl_arn = response["Summary"]["ARN"]

        self.wafv2.associate_web_acl(WebACLArn=web_acl_arn, ResourceArn=alb_arn)

        print(f"[OK] WAF podpięty do ALB: {web_acl_name}")

    # --- S3 z versioning i lifecycle ---

    def setup_s3_with_versioning_and_lifecycle(self, bucket_name: str) -> None:
        """Tworzy bucket S3 z włączonym versioning i lifecycle policy."""
        self.s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": self.region},
        )

        self.s3.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={"Status": "Enabled"},
        )

        self.s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration={
                "Rules": [
                    {
                        "ID": "archive-old-versions",
                        "Status": "Enabled",
                        "Filter": {},
                        "NoncurrentVersionTransitions": [
                            {"NoncurrentDays": 30, "StorageClass": "GLACIER"}
                        ],
                    }
                ]
            },
        )

        print(f"[OK] S3 bucket z versioning + lifecycle: {bucket_name}")

    # --- Route53 weighted routing (stable/canary) ---

    def setup_weighted_dns(
        self,
        hosted_zone_id: str,
        domain: str,
        stable_endpoint: str,
        canary_endpoint: str,
    ) -> None:
        """Konfiguruje weighted routing: 90% stable, 10% canary."""
        changes = [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": domain, "Type": "CNAME", "SetIdentifier": "stable",
                    "Weight": 90, "TTL": 60,
                    "ResourceRecords": [{"Value": stable_endpoint}],
                },
            },
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": domain, "Type": "CNAME", "SetIdentifier": "canary",
                    "Weight": 10, "TTL": 60,
                    "ResourceRecords": [{"Value": canary_endpoint}],
                },
            },
        ]

        self.route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={"Changes": changes},
        )

        print(f"[OK] Weighted routing: 90% stable / 10% canary dla {domain}")

    # --- Orchestracja całości ---

    def provision_full_infrastructure(self, config: dict) -> dict:
        """Buduje całą infrastrukturę produkcyjną na podstawie konfiguracji."""
        print("=== FULL PRODUCTION INFRASTRUCTURE PROVISIONING ===\n")

        network = self.create_vpc_with_subnets(config["vpc_cidr"])

        ec2_role_arn = self.create_least_privilege_role(
            role_name=config["ec2_role_name"],
            service="ec2.amazonaws.com",
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy",
            ],
        )

        secret_arn = self.store_database_credentials(
            secret_name=config["db_secret_name"],
            username=config["db_username"],
            password=config["db_password"],
        )

        database = self.create_multi_az_rds_with_replicas(
            db_identifier=config["db_identifier"],
            secret_arn=secret_arn,
            subnet_group_name=config["db_subnet_group_name"],
            replica_count=2,
        )

        self.setup_s3_with_versioning_and_lifecycle(config["s3_bucket_name"])

        load_balancer_arn = self.create_alb_with_ssl(
            alb_name=config["alb_name"],
            subnet_ids=network["public_subnets"],
            security_group_ids=config["security_group_ids"],
            certificate_arn=config["certificate_arn"],
            target_group_arn=config["target_group_arn"],
        )

        self.attach_waf_to_alb(load_balancer_arn)

        self.setup_weighted_dns(
            hosted_zone_id=config["hosted_zone_id"],
            domain=config["domain"],
            stable_endpoint=config["stable_endpoint"],
            canary_endpoint=config["canary_endpoint"],
        )

        print("\n[SUCCESS] Infrastruktura produkcyjna gotowa.")
        print(f"[INFO] VPC: {network['vpc_id']}")
        print(f"[INFO] Baza danych: {database['primary']} + {len(database['replicas'])} replik")
        print(f"[INFO] Load Balancer: {load_balancer_arn}")

        return {
            "network": network,
            "database": database,
            "load_balancer_arn": load_balancer_arn,
            "ec2_role_arn": ec2_role_arn,
        }


if __name__ == "__main__":
    builder = ProductionInfrastructureBuilder(region="eu-central-1")

    config = {
        "vpc_cidr": "10.0.0.0/16",
        "ec2_role_name": "lesson36-ec2-role",
        "db_secret_name": "lesson36/rds/credentials",
        "db_username": "admin_user",
        "db_password": "ZmienToHaslo123!",
        "db_identifier": "lesson36-production-db",
        "db_subnet_group_name": "lesson36-db-subnet-group",
        "s3_bucket_name": "lesson36-production-releases",
        "alb_name": "lesson36-production-alb",
        "security_group_ids": ["sg-xxxxxxxxxxxxxxxxx"],
        "certificate_arn": "arn:aws:acm:eu-central-1:123456789:certificate/xxxxx",
        "target_group_arn": "arn:aws:elasticloadbalancing:eu-central-1:123456789:targetgroup/lesson36-tg/abc123",
        "hosted_zone_id": "Z1234567890ABC",
        "domain": "app.yourdomain.com",
        "stable_endpoint": "lesson36-production-alb-123456.eu-central-1.elb.amazonaws.com",
        "canary_endpoint": "lesson36-canary-alb-654321.eu-central-1.elb.amazonaws.com",
    }

    try:
        result = builder.provision_full_infrastructure(config)

    except (ClientError, BotoCoreError) as exc:
        print(f"[ERROR] {exc}")