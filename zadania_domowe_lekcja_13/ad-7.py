import sqlite3

try:
    conn = sqlite3.connect("uczelnia.db")
    kursor = conn.cursor()

    studenci = [
        ("Anna", "Kowalska"),
        ("Piotr", "Nowak"),
        ("Kasia", "Wiśniewska"),
        ("Marek", "Zając")
    ]

    audytoria = [
        ("Budynek A", 101),
        ("Budynek B", 205),
        ("Budynek C", 310)
    ]

    kursor.executemany("""
        INSERT INTO studenci (imie, nazwisko)
        VALUES (?, ?)
    """, studenci)

    kursor.executemany("""
        INSERT INTO audytoria (nazwa_budynku, numer_sali)
        VALUES (?, ?)
    """, audytoria)

    conn.commit()
    print(f"Dodano {len(studenci)} studentów i {len(audytoria)} audytoria.")

except sqlite3.Error as e:
    print(f"Błąd podczas pracy z bazą danych: {e}")

finally:
    if conn:
        conn.close()
        print("Połączenie z bazą zostało zamknięte.") 