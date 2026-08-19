import sqlite3

DB = "c:/Projects python/Kurs Python/python_lesson/zadania domowe/lesson15/zadania.db"


class TaskManagerRaw:
    """Zarzadza zadaniami w bazie SQLite przy uzyciu surowych zapytan SQL."""

    def __init__(self):
        self.db = DB
        self._inicjalizuj_baze()

    def _inicjalizuj_baze(self):
        conn = sqlite3.connect(self.db)
        kursor = conn.cursor()
        kursor.execute("""
            CREATE TABLE IF NOT EXISTS zadania (
                id INTEGER PRIMARY KEY,
                tytul TEXT NOT NULL,
                ukonczone INTEGER DEFAULT 0,
                priorytet INTEGER DEFAULT 1
            )
        """)
        conn.commit()
        conn.close()

    def dodaj(self, tytul, priorytet=1):
        conn = sqlite3.connect(self.db)
        kursor = conn.cursor()
        kursor.execute(
            "INSERT INTO zadania (tytul, priorytet) VALUES (?, ?)",
            (tytul, priorytet)
        )
        conn.commit()
        conn.close()

    def pobierz(self):
        conn = sqlite3.connect(self.db)
        kursor = conn.cursor()
        kursor.execute("SELECT * FROM zadania")
        zadania = kursor.fetchall()
        conn.close()
        return zadania

    def usun(self, id_zadania):
        conn = sqlite3.connect(self.db)
        kursor = conn.cursor()
        kursor.execute("DELETE FROM zadania WHERE id = ?", (id_zadania,))
        conn.commit()
        rowcount = kursor.rowcount
        conn.close()
        return rowcount > 0

    def wyszukaj(self, fraza):
        conn = sqlite3.connect(self.db)
        kursor = conn.cursor()
        kursor.execute(
            "SELECT * FROM zadania WHERE tytul LIKE ?",
            (f"%{fraza}%",)
        )
        wyniki = kursor.fetchall()
        conn.close()
        return wyniki

    def edytuj(self, id_zadania, nowy_tytul):
        """Aktualizuje tytul zadania o podanym ID. Zwraca True, jesli cos zaktualizowano."""
        conn = sqlite3.connect(self.db)
        kursor = conn.cursor()
        kursor.execute(
            "UPDATE zadania SET tytul = ? WHERE id = ?",
            (nowy_tytul, id_zadania)
        )
        conn.commit()
        rowcount = kursor.rowcount
        conn.close()
        return rowcount > 0


if __name__ == "__main__":
    manager = TaskManagerRaw()
    manager.dodaj("Zrobic zakupy", priorytet=2)
    manager.dodaj("Posprzatac", priorytet=1)

    print("Wszystkie zadania:")
    for z in manager.pobierz():
        print(f"ID: {z[0]} | {z[1]} | priorytet: {z[3]}")

    print("\nWyszukiwanie 'zakupy':")
    for z in manager.wyszukaj("zakupy"):
        print(f"ID: {z[0]} | {z[1]}")
