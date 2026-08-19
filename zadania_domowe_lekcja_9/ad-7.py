from pathlib import Path

projekt = Path("Projekt")

(projekt / "src").mkdir(parents=True, exist_ok=True)
(projekt / "data").mkdir(parents=True, exist_ok=True)
(projekt / "docs").mkdir(parents=True, exist_ok=True)

print("Utworzono strukturę folderów Projekt.") 