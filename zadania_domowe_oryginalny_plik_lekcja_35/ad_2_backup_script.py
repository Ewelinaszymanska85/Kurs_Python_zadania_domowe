from datetime import datetime
from pathlib import Path
import shutil


def create_backup(source_dir: str, backup_root: str = "backups") -> Path:
    """
    Tworzy kopię zapasową wskazanego katalogu.

    Backup otrzymuje nazwę zawierającą datę i czas utworzenia.
    """
    source = Path(source_dir)
    backup_directory = Path(backup_root)

    if not source.exists():
        raise FileNotFoundError(
            f"Katalog źródłowy nie istnieje: {source}"
        )

    if not source.is_dir():
        raise NotADirectoryError(
            f"Podana ścieżka nie jest katalogiem: {source}"
        )

    backup_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_path = backup_directory / (
        f"{source.name}_backup_{timestamp}"
    )

    if backup_path.exists():
        raise FileExistsError(
            f"Backup już istnieje: {backup_path}"
        )

    shutil.copytree(
        source,
        backup_path,
    )

    print("=== BACKUP COMPLETED ===")
    print(f"Źródło: {source.resolve()}")
    print(f"Backup: {backup_path.resolve()}")

    return backup_path


if __name__ == "__main__":
    try:
        create_backup(
            source_dir="dane_testowe",
        )
    except (
        FileNotFoundError,
        NotADirectoryError,
        FileExistsError,
        OSError,
    ) as exc:
        print(f"[ERROR] {exc}")