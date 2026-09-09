import re

import boto3
from botocore.exceptions import ClientError


def validate_bucket_name(bucket_name: str) -> None:
    """Sprawdza podstawowe wymagania nazwy bucketa S3."""
    if not 3 <= len(bucket_name) <= 63:
        raise ValueError("Nazwa bucketa musi mieć od 3 do 63 znaków.")

    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]*[a-z0-9]", bucket_name):
        raise ValueError(
            "Nazwa bucketa może zawierać tylko małe litery, cyfry, kropki i myślniki."
        )


def create_s3_bucket(
    bucket_name: str,
    region: str = "eu-central-1",
) -> bool:
    """Tworzy bucket S3 w podanym regionie."""
    validate_bucket_name(bucket_name)

    s3 = boto3.client("s3", region_name=region)

    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": region,
                },
            )

        print(f"[OK] Utworzono bucket: {bucket_name}")
        print(f"[INFO] Region: {region}")
        return True

    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]

        if error_code == "BucketAlreadyOwnedByYou":
            print(f"[WARNING] Bucket '{bucket_name}' już należy do Ciebie.")
            return False

        if error_code == "BucketAlreadyExists":
            print(f"[ERROR] Nazwa '{bucket_name}' jest już zajęta globalnie.")
            return False

        print(
            f"[AWS ERROR] {error_code}: "
            f"{exc.response['Error'].get('Message', 'Nieznany błąd')}"
        )
        return False


if __name__ == "__main__":
    try:
        create_s3_bucket(
            bucket_name="ewelina-python-course-lesson35-demo",
            region="eu-central-1",
        )
    except ValueError as exc:
        print(f"[VALIDATION ERROR] {exc}")