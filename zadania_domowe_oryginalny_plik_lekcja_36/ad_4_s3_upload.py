import shutil
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def compress_and_upload(
    source_dir: str,
    bucket_name: str,
    region: str = "eu-central-1",
    prefix: str = "app-releases/",
) -> str:
    """Kompresuje folder aplikacji do ZIP i uploaduje do S3."""
    source = Path(source_dir)

    if not source.is_dir():
        raise NotADirectoryError(f"Katalog nie istnieje: {source}")

    archive_base_name = source.name
    archive_path = shutil.make_archive(
        archive_base_name,
        "zip",
        root_dir=source,
    )
    archive_file = Path(archive_path)

    print(f"[OK] Utworzono archiwum: {archive_file.name}")

    s3 = boto3.client("s3", region_name=region)
    object_key = f"{prefix}{archive_file.name}"

    s3.upload_file(
        str(archive_file),
        bucket_name,
        object_key,
    )

    print(f"[UPLOAD] {archive_file.name} -> s3://{bucket_name}/{object_key}")

    archive_file.unlink()
    print(f"[CLEANUP] Usunięto lokalne archiwum: {archive_file.name}")

    file_url = (
        f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_key}"
    )

    print(f"[URL] {file_url}")
    return file_url


if __name__ == "__main__":
    try:
        compress_and_upload(
            source_dir="moja_aplikacja",
            bucket_name="ewelina-python-course-lesson35-demo",
        )

    except NotADirectoryError as exc:
        print(f"[ERROR] {exc}")

    except (ClientError, BotoCoreError) as exc:
        print(f"[AWS ERROR] {exc}")