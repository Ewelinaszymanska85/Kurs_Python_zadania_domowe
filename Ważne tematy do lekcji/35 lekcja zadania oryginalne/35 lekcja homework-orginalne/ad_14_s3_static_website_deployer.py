import argparse
import json
import mimetypes
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


class S3StaticWebsiteDeployer:
    """Wdraża statyczną stronę WWW do bucketa Amazon S3."""

    def __init__(self, bucket_name: str, region: str) -> None:
        self.bucket_name = bucket_name
        self.region = region
        self.s3 = boto3.client("s3", region_name=region)

    def create_bucket(self) -> None:
        try:
            if self.region == "us-east-1":
                self.s3.create_bucket(Bucket=self.bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={
                        "LocationConstraint": self.region,
                    },
                )
            print(f"[OK] Utworzono bucket: {self.bucket_name}")

        except ClientError as exc:
            code = exc.response["Error"]["Code"]

            if code == "BucketAlreadyOwnedByYou":
                print("[INFO] Bucket już istnieje i należy do Ciebie.")
            else:
                raise

    def configure_website(self) -> None:
        self.s3.put_bucket_website(
            Bucket=self.bucket_name,
            WebsiteConfiguration={
                "IndexDocument": {"Suffix": "index.html"},
                "ErrorDocument": {"Key": "error.html"},
            },
        )

        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{self.bucket_name}/*",
                }
            ],
        }

        self.s3.put_bucket_policy(
            Bucket=self.bucket_name,
            Policy=json.dumps(policy),
        )

        print("[OK] Skonfigurowano hosting statyczny i bucket policy.")

    def upload_files(self, directory: str) -> int:
        source = Path(directory)

        if not source.is_dir():
            raise NotADirectoryError(
                f"Katalog strony nie istnieje: {source}"
            )

        allowed_extensions = {".html", ".css", ".js"}
        uploaded = 0

        for file_path in source.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in allowed_extensions:
                continue

            object_key = file_path.relative_to(source).as_posix()
            content_type = (
                mimetypes.guess_type(file_path.name)[0]
                or "application/octet-stream"
            )

            self.s3.upload_file(
                str(file_path),
                self.bucket_name,
                object_key,
                ExtraArgs={
                    "ContentType": content_type,
                },
            )

            uploaded += 1
            print(f"[UPLOAD] {object_key} | {content_type}")

        return uploaded

    def get_website_url(self) -> str:
        """Buduje poprawny URL strony statycznej dla danego regionu."""
        if self.region == "us-east-1":
            return f"http://{self.bucket_name}.s3-website-us-east-1.amazonaws.com"

        return (
            f"http://{self.bucket_name}.s3-website."
            f"{self.region}.amazonaws.com"
        )

    def deploy(self, directory: str) -> None:
        print("=== S3 STATIC WEBSITE DEPLOYMENT ===")

        self.create_bucket()
        self.configure_website()

        uploaded = self.upload_files(directory)

        print(f"\n[OK] Wysłano plików: {uploaded}")
        print(f"[URL] {self.get_website_url()}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deployment statycznej strony WWW na Amazon S3."
    )

    parser.add_argument(
        "directory",
        help="Katalog zawierający pliki strony.",
    )

    parser.add_argument(
        "--bucket",
        required=True,
        help="Nazwa bucketa S3.",
    )

    parser.add_argument(
        "--region",
        default="eu-central-1",
        help="Region AWS.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    try:
        deployer = S3StaticWebsiteDeployer(
            bucket_name=args.bucket,
            region=args.region,
        )
        deployer.deploy(args.directory)

    except (ClientError, OSError) as exc:
        print(f"[ERROR] Deployment nieudany: {exc}")