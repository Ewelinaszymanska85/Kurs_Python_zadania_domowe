import json
from pathlib import Path
from typing import Any


class MultiEnvironmentConfigManager:
    """Zarządza konfiguracjami wielu środowisk aplikacji."""

    def __init__(self, config_file: str = "environments.json") -> None:
        self.config_file = Path(config_file)

    def create_default_config(self) -> None:
        """Tworzy przykładową konfigurację środowisk."""
        config = {
            "development": {
                "debug": True,
                "database": "localhost",
                "workers": 1,
                "log_level": "DEBUG",
            },
            "staging": {
                "debug": False,
                "database": "staging-db.internal",
                "workers": 2,
                "log_level": "INFO",
            },
            "production": {
                "debug": False,
                "database": "production-db.internal",
                "workers": 4,
                "log_level": "WARNING",
            },
        }

        with self.config_file.open("w", encoding="utf-8") as file:
            json.dump(
                config,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def load_config(self) -> dict[str, Any]:
        """Wczytuje konfigurację z pliku JSON."""
        if not self.config_file.exists():
            self.create_default_config()

        with self.config_file.open("r", encoding="utf-8") as file:
            return json.load(file)

    def get_environment(self, environment: str) -> dict[str, Any]:
        """Pobiera konfigurację wybranego środowiska."""
        config = self.load_config()

        if environment not in config:
            raise ValueError(
                f"Nieznane środowisko: {environment}"
            )

        return config[environment]

    def deploy(self, environment: str) -> None:
        """Symuluje deployment wybranej konfiguracji."""
        config = self.get_environment(environment)

        print(f"=== DEPLOYMENT: {environment.upper()} ===")

        for key, value in config.items():
            print(f"{key:<12}: {value}")

        print("[OK] Konfiguracja wdrożona.")

    def compare(
        self,
        first_environment: str,
        second_environment: str,
    ) -> dict[str, tuple[Any, Any]]:
        """Porównuje konfiguracje dwóch środowisk."""
        first = self.get_environment(first_environment)
        second = self.get_environment(second_environment)

        differences = {}

        for key in sorted(set(first) | set(second)):
            first_value = first.get(key)
            second_value = second.get(key)

            if first_value != second_value:
                differences[key] = (
                    first_value,
                    second_value,
                )

        return differences


if __name__ == "__main__":
    try:
        manager = MultiEnvironmentConfigManager()

        manager.deploy("production")

        print("\n=== STAGING vs PRODUCTION ===")

        differences = manager.compare(
            "staging",
            "production",
        )

        for key, values in differences.items():
            print(
                f"{key:<12}: "
                f"{values[0]} -> {values[1]}"
            )

    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] {exc}")