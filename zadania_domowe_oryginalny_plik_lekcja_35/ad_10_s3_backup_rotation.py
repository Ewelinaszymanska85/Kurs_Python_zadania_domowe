from datetime import datetime, timedelta, timezone
from pathlib import Path
import shutil

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


def create_local_backup(source_dir: str) -> Path:
    """Tworzy archiwum ZIP katalogu i zwraca ┼Ťcie┼╝k─Ö do pliku."""
    source = Path(source_dir)

    if not source.is_dir():
        raise NotADirectoryError(f"Katalog nie istnieje: {source}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"

    archive_path = shutil.make_archive(
        backup_name,
        "zip",
        root_dir=source,
    )

    return Path(archive_path)


def upload_backup_to_s3(
    backup_path: Path,
    bucket_name: str,
    prefix: str = "backups/",
) -> str:
    """Wysy┼éa backup do S3 i usuwa lokaln─ů kopi─Ö ZIP."""
    s3 = boto3.client("s3")
    object_key = f"{prefix}{backup_path.name}"

    s3.upload_file(
        str(backup_path),
        bucket_name,
        object_key,
    )

    print(f"[UPLOAD] {backup_path.name} -> s3://{bucket_name}/{object_key}")

    backup_path.unlink()
    print(f"[CLEANUP] Usuni─Öto lokalny plik: {backup_path.name}")

    return object_key


def rotate_old_backups(
    bucket_name: str,
    prefix: str = "backups/",
    retention_days: int = 7,
) -> int:
    """Usuwa z S3 backupy starsze ni┼╝ okre┼Ťlona liczba dni."""
    s3 = boto3.client("s3")
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

    paginator = s3.get_paginator("list_objects_v2")
    deleted = 0

    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get("Contents", []):
            if obj["LastModified"] < cutoff:
                s3.delete_object(
                    Bucket=bucket_name,
                    Key=obj["Key"],
                )

                deleted += 1
                print(f"[DELETE] {obj['Key']}")

    return deleted


def run_backup(
    source_dir: str,
    bucket_name: str,
) -> None:
    """Tworzy backup, wysy┼éa go do S3 i wykonuje rotacj─Ö."""
    try:
        print("=== S3 BACKUP WITH ROTATION ===")

        backup_path = create_local_backup(source_dir)

        print(f"[OK] Utworzono backup: {backup_path.name}")

        upload_backup_to_s3(
            backup_path,
            bucket_name,
        )

        deleted = rotate_old_backups(
            bucket_name,
            retention_days=7,
        )

        print(f"[SUMMARY] Usuni─Öto starych backup├│w: {deleted}")

    except NoCredentialsError:
        print("[ERROR] Brak danych uwierzytelniaj─ůcych AWS.")

    except ClientError as exc:
        message = exc.response["Error"].get(
            "Message",
            "Nieznany b┼é─ůd AWS",
        )
        print(f"[AWS ERROR] {message}")

    except (BotoCoreError, OSError) as exc:
        print(f"[ERROR] {exc}")


if __name__ == "__main__":
    run_backup(
        source_dir="dane_testowe",
        bucket_name="ewelina-python-course-lesson35-demo",
    )
