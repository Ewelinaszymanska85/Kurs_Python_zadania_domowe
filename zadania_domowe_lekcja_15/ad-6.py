import sqlite3

DB = "c:/Projects python/Kurs Python/python_lesson/zadania domowe/lesson15/zadania.db"


def wyszukaj_zadania(fraza):
    """Wyszukuje zadania, których tytuł zawiera podaną frazę."""
    conn = sqlite3.connect(DB)
    kursor = conn.cursor()
    kursor.execute(
        "SELECT * FROM zadania WHERE tytul LIKE ?",
        (f"%{fraza}%",)
    )
    wyniki = kursor.fetchall()
    conn.close()
    return wyniki


if __name__ == "__main__":
    fraza = input("Podaj frazę do wyszukania: ")
    wyniki = wyszukaj_zadania(fraza)

    if wyniki:
        for z in wyniki:
            print(f"ID: {z[0]} | {z[1]} | priorytet: {z[3]}")
    else:
        print("Nie znaleziono zadań.") 