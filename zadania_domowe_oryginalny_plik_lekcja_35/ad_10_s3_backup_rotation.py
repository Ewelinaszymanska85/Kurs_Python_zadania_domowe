from datetime import datetime, timedelta, timezone
from pathlib import Path
import shutil

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


def create_local_backup(source_dir: str) -> Path:
    """Tworzy archiwum ZIP katalogu i zwraca ścieżkę do pliku."""
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
    """Wysyła backup do S3."""
    s3 = boto3.client("s3")
    object_key = f"{prefix}{backup_path.name}"

    s3.upload_file(
        str(backup_path),
        bucket_name,
        object_key,
    )

    print(f"[UPLOAD] {backup_path.name} -> s3://{bucket_name}/{object_key}")
    return object_key


def rotate_old_backups(
    bucket_name: str,
    prefix: str = "backups/",
    retention_days: int = 7,
) -> int:
    """Usuwa z S3 backupy starsze niż określona liczba dni."""
    s3 = boto3.client("s3")
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix,
    )

    deleted = 0

    for obj in response.get("Contents", []):
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
    """Tworzy backup, wysyła go do S3 i wykonuje rotację."""
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

        print(f"[SUMMARY] Usunięto starych backupów: {deleted}")

    except NoCredentialsError:
        print("[ERROR] Brak danych uwierzytelniających AWS.")

    except ClientError as exc:
        message = exc.response["Error"].get(
            "Message",
            "Nieznany błąd AWS",
        )
        print(f"[AWS ERROR] {message}")

    except (BotoCoreError, OSError) as exc:
        print(f"[ERROR] {exc}")


if __name__ == "__main__":
    run_backup(
        source_dir="dane_testowe",
        bucket_name="ewelina-python-course-lesson35-demo",
    )