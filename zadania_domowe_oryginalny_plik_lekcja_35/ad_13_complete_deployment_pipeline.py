import subprocess
import time
from dataclasses import dataclass

import requests


@dataclass
class DeploymentConfig:
    repo_url: str
    branch: str
    image_name: str
    ecr_repository: str
    ec2_host: str
    health_url: str


class DeploymentPipeline:
    """Symuluje kompletny pipeline wdrożeniowy."""

    def __init__(self, config: DeploymentConfig) -> None:
        self.config = config

    def run_command(self, command: list[str], step_name: str) -> None:
        print(f"[RUN] {step_name}")

        subprocess.run(
            command,
            check=True,
        )

        print(f"[OK] {step_name}")

    def update_repository(self) -> None:
        self.run_command(
            ["git", "pull", "origin", self.config.branch],
            "Aktualizacja repozytorium",
        )

    def run_tests(self) -> None:
        self.run_command(
            ["pytest"],
            "Uruchomienie testów",
        )

    def build_docker_image(self) -> None:
        self.run_command(
            [
                "docker",
                "build",
                "-t",
                self.config.image_name,
                ".",
            ],
            "Budowanie obrazu Docker",
        )

    def push_to_ecr(self) -> None:
        print(
            f"[SIMULATION] Push obrazu "
            f"{self.config.image_name} "
            f"do ECR: {self.config.ecr_repository}"
        )

    def deploy_to_ec2(self) -> None:
        print(
            f"[SIMULATION] Deployment przez SSH "
            f"na EC2: {self.config.ec2_host}"
        )

    def health_check(self) -> bool:
        print(f"[CHECK] {self.config.health_url}")

        try:
            response = requests.get(
                self.config.health_url,
                timeout=5,
            )

            if response.status_code == 200:
                print("[OK] Health check zakończony sukcesem.")
                return True

            print(
                f"[ERROR] Health check: "
                f"HTTP {response.status_code}"
            )
            return False

        except requests.RequestException as exc:
            print(f"[ERROR] Health check failed: {exc}")
            return False

    def rollback(self) -> None:
        print(
            "[ROLLBACK] Przywracanie poprzedniej "
            "wersji aplikacji..."
        )
        time.sleep(0.5)
        print("[OK] Rollback zakończony.")

    def deploy(self) -> bool:
        print("=== COMPLETE DEPLOYMENT PIPELINE ===")

        try:
            self.update_repository()
            self.run_tests()
            self.build_docker_image()
            self.push_to_ecr()
            self.deploy_to_ec2()

            if not self.health_check():
                self.rollback()
                return False

        except subprocess.CalledProcessError as exc:
            print(
                f"[ERROR] Pipeline przerwany. "
                f"Exit code: {exc.returncode}"
            )
            self.rollback()
            return False

        print("[SUCCESS] Deployment zakończony pomyślnie.")
        return True


if __name__ == "__main__":
    configuration = DeploymentConfig(
        repo_url="https://github.com/example/project.git",
        branch="main",
        image_name="myapp:latest",
        ecr_repository="123456789.dkr.ecr.eu-central-1.amazonaws.com/myapp",
        ec2_host="ec2-user@example.compute.amazonaws.com",
        health_url="https://example.com/health",
    )

    pipeline = DeploymentPipeline(configuration)
    pipeline.deploy()