from pathlib import Path

import boto3
from botocore.exceptions import ClientError


def upload_jpg_files(
    source_dir: str,
    bucket_name: str,
    prefix: str = "uploads/",
) -> int:
    """Wysyła wszystkie pliki JPG z katalogu do bucketa S3."""
    directory = Path(source_dir)

    if not directory.exists():
        raise FileNotFoundError(
            f"Katalog nie istnieje: {directory}"
        )

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Podana ścieżka nie jest katalogiem: {directory}"
        )

    s3 = boto3.client("s3")
    uploaded_count = 0

    jpg_files = sorted(directory.glob("*.jpg"))

    if not jpg_files:
        print("[INFO] Nie znaleziono plików JPG.")
        return 0

    for file_path in jpg_files:
        object_key = f"{prefix}{file_path.name}"

        try:
            s3.upload_file(
                str(file_path),
                bucket_name,
                object_key,
            )

            uploaded_count += 1

            print(
                f"[OK] {file_path.name} -> "
                f"s3://{bucket_name}/{object_key}"
            )

        except ClientError as exc:
            print(
                f"[AWS ERROR] {file_path.name}: "
                f"{exc.response['Error'].get('Message', 'Nieznany błąd')}"
            )

    print(
        f"[SUMMARY] Wysłano {uploaded_count} "
        f"z {len(jpg_files)} plików."
    )

    return uploaded_count


if __name__ == "__main__":
    try:
        upload_jpg_files(
            source_dir="obrazy",
            bucket_name="ewelina-python-course-lesson35-demo",
        )
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"[ERROR] {exc}")