import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


def sync_s3_buckets(
    source_bucket: str,
    destination_bucket: str,
) -> int:
    """Kopiuje wszystkie obiekty z jednego bucketa S3 do drugiego."""
    s3 = boto3.client("s3")

    try:
        response = s3.list_objects_v2(
            Bucket=source_bucket,
        )

        objects = response.get("Contents", [])

        if not objects:
            print("[INFO] Bucket źródłowy jest pusty.")
            return 0

        copied = 0

        print("=== S3 MULTI-REGION SYNC ===")
        print(f"Źródło: {source_bucket}")
        print(f"Cel: {destination_bucket}")
        print(f"Obiektów do skopiowania: {len(objects)}\n")

        for obj in objects:
            key = obj["Key"]

            copy_source = {
                "Bucket": source_bucket,
                "Key": key,
            }

            s3.copy_object(
                CopySource=copy_source,
                Bucket=destination_bucket,
                Key=key,
            )

            copied += 1
            print(f"[COPY] {key}")

        print(f"\n[OK] Skopiowano obiektów: {copied}")
        return copied

    except NoCredentialsError:
        print("[ERROR] Brak danych uwierzytelniających AWS.")

    except ClientError as exc:
        message = exc.response["Error"].get(
            "Message",
            "Nieznany błąd",
        )
        print(f"[AWS ERROR] {message}")

    except BotoCoreError as exc:
        print(f"[ERROR] Błąd komunikacji z AWS: {exc}")

    return 0


if __name__ == "__main__":
    sync_s3_buckets(
        source_bucket="source-backup-bucket",
        destination_bucket="destination-backup-bucket",
    )