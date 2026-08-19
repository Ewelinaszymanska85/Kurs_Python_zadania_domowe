import sqlite3

try:
    conn = sqlite3.connect("uczelnia.db")
    kursor = conn.cursor()

    przypisania = [
        (1, 1),  # Anna -> Budynek A, sala 101
        (2, 2),  # Piotr -> Budynek B, sala 205
        (3, 3),  # Kasia -> Budynek C, sala 310
        (4, 1),  # Marek -> Budynek A, sala 101
    ]

    kursor.executemany("""
        INSERT INTO przypisania (id_studenta, id_audytorium)
        VALUES (?, ?)
    """, przypisania)

    conn.commit()
    print(f"Dodano {len(przypisania)} przypisań.")

except sqlite3.Error as e:
    print(f"Błąd podczas pracy z bazą danych: {e}")

finally:
    if conn:
        conn.close()
        print("Połączenie z bazą zostało zamknięte.") 