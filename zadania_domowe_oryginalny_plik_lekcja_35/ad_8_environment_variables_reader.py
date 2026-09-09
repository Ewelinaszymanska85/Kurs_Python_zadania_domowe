import os


AWS_VARIABLES = (
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_DEFAULT_REGION",
)


def check_aws_environment() -> dict[str, bool]:
    """Sprawdza, czy wymagane zmienne środowiskowe AWS są ustawione."""
    result = {}

    print("=== AWS ENVIRONMENT CHECK ===")

    for variable in AWS_VARIABLES:
        value = os.environ.get(variable)

        is_configured = bool(value)
        result[variable] = is_configured

        if is_configured:
            if "SECRET" in variable or "ACCESS_KEY" in variable:
                print(f"[OK] {variable}: ustawiona")
            else:
                print(f"[OK] {variable}: {value}")
        else:
            print(f"[WARNING] {variable}: brak wartości")

    return result


def print_summary(result: dict[str, bool]) -> None:
    """Wyświetla podsumowanie konfiguracji AWS."""
    configured = sum(result.values())
    total = len(result)

    print(f"\n[SUMMARY] Skonfigurowano {configured}/{total} zmiennych.")

    if configured == total:
        print("[OK] Środowisko AWS jest kompletne.")
    else:
        print("[WARNING] Konfiguracja AWS jest niekompletna.")


if __name__ == "__main__":
    configuration = check_aws_environment()
    print_summary(configuration)