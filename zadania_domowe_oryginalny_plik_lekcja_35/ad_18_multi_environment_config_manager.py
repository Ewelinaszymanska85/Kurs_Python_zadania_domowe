import json
from pathlib import Path
from typing import Any


class MultiEnvironmentConfigManager:
    """Zarz─ůdza konfiguracjami wielu ┼Ťrodowisk infrastruktury."""

    def __init__(self, config_file: str = "environments.json") -> None:
        self.config_file = Path(config_file)

    def create_default_config(self) -> None:
        """Tworzy przyk┼éadow─ů konfiguracj─Ö ┼Ťrodowisk."""
        config = {
            "dev": {
                "region": "eu-central-1",
                "instance_type": "t3.micro",
                "db_size": "db.t3.micro",
            },
            "staging": {
                "region": "eu-central-1",
                "instance_type": "t3.small",
                "db_size": "db.t3.small",
            },
            "production": {
                "region": "eu-west-1",
                "instance_type": "m5.large",
                "db_size": "db.m5.large",
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
        """Wczytuje konfiguracj─Ö z pliku JSON."""
        if not self.config_file.exists():
            self.create_default_config()

        with self.config_file.open("r", encoding="utf-8") as file:
            return json.load(file)

    def get_environment(self, environment: str) -> dict[str, Any]:
        """Pobiera konfiguracj─Ö wybranego ┼Ťrodowiska."""
        config = self.load_config()

        if environment not in config:
            raise ValueError(
                f"Nieznane ┼Ťrodowisko: {environment}"
            )

        return config[environment]

    def deploy(self, environment: str) -> None:
        """Wy┼Ťwietla, jakie zasoby nale┼╝y utworzy─ç dla danego ┼Ťrodowiska."""
        config = self.get_environment(environment)

        print(f"=== DEPLOYMENT: {environment.upper()} ===")
        print(f"Region        : {config['region']}")
        print(f"Instancja EC2 : {config['instance_type']}")
        print(f"Baza danych   : {config['db_size']}")
        print("[OK] Zasoby gotowe do utworzenia.")

    def compare(
        self,
        first_environment: str,
        second_environment: str,
    ) -> dict[str, tuple[Any, Any]]:
        """Por├│wnuje konfiguracje dw├│ch ┼Ťrodowisk."""
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
                f"{key:<14}: "
                f"{values[0]} -> {values[1]}"
            )

    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] {exc}")
