# Zadanie 4 – Dodanie priorytetu (Raw SQL)

import sqlite3

DB = "c:/Projects python/Kurs Python/python_lesson/zadania domowe/lesson15/zadania.db"

def inicjalizuj_baze():
    conn = sqlite3.connect(DB)
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

def dodaj_zadanie(tytul, priorytet=1):
    conn = sqlite3.connect(DB)
    kursor = conn.cursor()
    kursor.execute(
        "INSERT INTO zadania (tytul, priorytet) VALUES (?, ?)",
        (tytul, priorytet)
    )
    conn.commit()
    conn.close()

def pokaz_zadania():
    conn = sqlite3.connect(DB)
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM zadania")
    zadania = kursor.fetchall()
    conn.close()
    return zadania

def usun_zadanie(id_zadania):
    conn = sqlite3.connect(DB)
    kursor = conn.cursor()
    kursor.execute("DELETE FROM zadania WHERE id = ?", (id_zadania,))
    conn.commit()
    conn.close()

# Test
inicjalizuj_baze()
dodaj_zadanie("Kupić mleko", priorytet=2)
dodaj_zadanie("Zadzwonić do mamy", priorytet=1)

zadania = pokaz_zadania()
for z in zadania:
    print(f"ID: {z[0]} | {z[1]} | priorytet: {z[3]}") 