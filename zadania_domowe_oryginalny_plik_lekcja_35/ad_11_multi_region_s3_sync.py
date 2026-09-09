import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


def sync_s3_buckets(
    source_bucket: str,
    destination_bucket: str,
) -> int:
    """Kopiuje wszystkie obiekty z jednego bucketa S3 do drugiego."""
    s3 = boto3.client("s3")

    try:
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=source_bucket)

        objects = [
            obj
            for page in pages
            for obj in page.get("Contents", [])
        ]

        if not objects:
            print("[INFO] Bucket ┼║r├│d┼éowy jest pusty.")
            return 0

        copied = 0
        failed = 0

        print("=== S3 MULTI-REGION SYNC ===")
        print(f"┼╣r├│d┼éo: {source_bucket}")
        print(f"Cel: {destination_bucket}")
        print(f"Obiekt├│w do skopiowania: {len(objects)}\n")

        for obj in objects:
            key = obj["Key"]

            copy_source = {
                "Bucket": source_bucket,
                "Key": key,
            }

            try:
                s3.copy_object(
                    CopySource=copy_source,
                    Bucket=destination_bucket,
                    Key=key,
                )

                copied += 1
                print(f"[COPY] {key}")

            except ClientError as exc:
                failed += 1
                message = exc.response["Error"].get("Message", "Nieznany b┼é─ůd")
                print(f"[FAILED] {key}: {message}")

        print(f"\n[OK] Skopiowano obiekt├│w: {copied} | B┼é─Öd├│w: {failed}")
        return copied

    except NoCredentialsError:
        print("[ERROR] Brak danych uwierzytelniaj─ůcych AWS.")

    except ClientError as exc:
        message = exc.response["Error"].get(
            "Message",
            "Nieznany b┼é─ůd",
        )
        print(f"[AWS ERROR] {message}")

    except BotoCoreError as exc:
        print(f"[ERROR] B┼é─ůd komunikacji z AWS: {exc}")

    return 0


if __name__ == "__main__":
    sync_s3_buckets(
        source_bucket="source-backup-bucket",
        destination_bucket="destination-backup-bucket",
    )
