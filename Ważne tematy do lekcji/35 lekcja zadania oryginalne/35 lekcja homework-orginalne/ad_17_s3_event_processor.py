from io import BytesIO
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from PIL import Image, UnidentifiedImageError


class S3ImageProcessor:
    """Przetwarza nowe obrazy z S3 i tworzy miniatury."""

    def __init__(
        self,
        bucket_name: str,
        thumbnail_size: tuple[int, int] = (300, 300),
    ) -> None:
        self.bucket_name = bucket_name
        self.thumbnail_size = thumbnail_size
        self.s3 = boto3.client("s3")

    def list_image_objects(self) -> list[str]:
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)

        return [
            obj["Key"]
            for obj in response.get("Contents", [])
            if obj["Key"].lower().endswith((".jpg", ".jpeg", ".png"))
            and not obj["Key"].startswith("thumbnails/")
        ]

    def create_thumbnail(self, object_key: str) -> str:
        response = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=object_key,
        )

        image_data = response["Body"].read()

        with Image.open(BytesIO(image_data)) as image:
            image_format = image.format or "JPEG"
            image.thumbnail(self.thumbnail_size)

            output = BytesIO()

            # RGBA nie jest wspierane przez JPEG - konwersja przy zapisie.
            if image_format == "JPEG" and image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            image.save(output, format=image_format)
            output.seek(0)

        thumbnail_key = f"thumbnails/{Path(object_key).name}"

        self.s3.upload_fileobj(
            output,
            self.bucket_name,
            thumbnail_key,
        )

        print(f"[OK] {object_key} -> {thumbnail_key}")
        return thumbnail_key

    def process(self) -> None:
        print("=== S3 IMAGE PROCESSOR ===")

        objects = self.list_image_objects()

        if not objects:
            print("[INFO] Brak obrazów do przetworzenia.")
            return

        processed = 0
        failed = 0

        for object_key in objects:
            try:
                self.create_thumbnail(object_key)
                processed += 1

            except UnidentifiedImageError:
                failed += 1
                print(f"[SKIP] {object_key}: nieprawidłowy plik obrazu.")

            except (ClientError, BotoCoreError) as exc:
                failed += 1
                print(f"[ERROR] {object_key}: {exc}")

        print(f"[SUMMARY] Przetworzono: {processed} | Błędów: {failed}")


if __name__ == "__main__":
    try:
        processor = S3ImageProcessor(
            bucket_name="ewelina-python-course-lesson35-demo",
            thumbnail_size=(300, 300),
        )
        processor.process()

    except NoCredentialsError:
        print("[ERROR] Brak danych uwierzytelniających AWS.")

    except ClientError as exc:
        print(
            f"[AWS ERROR] "
            f"{exc.response['Error'].get('Message', 'Nieznany błąd')}"
        )

    except BotoCoreError as exc:
        print(f"[ERROR] Błąd komunikacji z AWS: {exc}")