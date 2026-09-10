import subprocess
from pathlib import Path


def run_aws_command(command: list[str]) -> str:
    """Uruchamia komendę AWS CLI i zwraca jej output jako tekst."""
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def collect_aws_resources(output_file: str = "aws-resources.txt") -> None:
    """Zbiera informacje o EC2, RDS i S3 przez AWS CLI i zapisuje do pliku."""
    sections = {
        "EC2 INSTANCES": [
            "aws", "ec2", "describe-instances",
            "--query", "Reservations[].Instances[].[InstanceId,InstanceType,State.Name]",
            "--output", "table",
        ],
        "RDS DATABASES": [
            "aws", "rds", "describe-db-instances",
            "--query", "DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Engine]",
            "--output", "table",
        ],
        "S3 BUCKETS": [
            "aws", "s3", "ls",
        ],
    }

    output_lines = []

    for title, command in sections.items():
        print(f"[RUN] {title}")

        try:
            output = run_aws_command(command)
            output_lines.append(f"=== {title} ===")
            output_lines.append(output)

        except subprocess.CalledProcessError as exc:
            error_message = exc.stderr or str(exc)
            output_lines.append(f"=== {title} ===")
            output_lines.append(f"[ERROR] {error_message}")
            print(f"[ERROR] {title}: {error_message}")

        except FileNotFoundError:
            output_lines.append(f"=== {title} ===")
            output_lines.append("[ERROR] AWS CLI nie jest zainstalowane lub niedostępne w PATH.")
            print("[ERROR] AWS CLI nie znalezione.")
            break

    Path(output_file).write_text(
        "\n\n".join(output_lines),
        encoding="utf-8",
    )

    print(f"[OK] Zapisano wynik do: {output_file}")


if __name__ == "__main__":
    collect_aws_resources()