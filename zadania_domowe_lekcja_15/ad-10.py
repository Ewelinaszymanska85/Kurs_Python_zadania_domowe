# Interaktywna edycja (Raw SQL)

import sqlite3

DB = "c:/Projects python/Kurs Python/python_lesson/zadania domowe/lesson15/zadania.db"

def edytuj_zadanie(id_zadania, nowy_tytul):
    conn = sqlite3.connect(DB)
    kursor = conn.cursor()
    kursor.execute(
        "UPDATE zadania SET tytul = ? WHERE id = ?",
        (nowy_tytul, id_zadania)
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


# Test
print("Przed edycją:")
for z in pokaz_zadania():
    print(f"ID: {z[0]} | {z[1]} | priorytet: {z[3]}")

id_zadania = int(input("\nPodaj ID zadania do edycji: "))
nowy_tytul = input("Podaj nowy opis: ")
edytuj_zadanie(id_zadania, nowy_tytul)

print("\nPo edycji:")
for z in pokaz_zadania():
    print(f"ID: {z[0]} | {z[1]} | priorytet: {z[3]}") 