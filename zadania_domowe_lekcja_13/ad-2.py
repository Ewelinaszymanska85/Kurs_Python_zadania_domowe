import sqlite3

try:
    conn = sqlite3.connect("biblioteka.db")
    cursor = conn.cursor()

    ksiazki = [
        ("Lalka", "Bolesław Prus", 1890),
        ("Zbrodnia i kara", "Fiodor Dostojewski", 1866),
        ("Wiedźmin: Ostatnie życzenie", "Andrzej Sapkowski", 1993)
    ]

    cursor.executemany("""
        INSERT INTO ksiazki (tytul, autor, rok_wydania)
        VALUES (?, ?, ?)
    """, ksiazki)

    conn.commit()
    print(f"Dodano {cursor.rowcount} książki do tabeli 'ksiazki'.")

except sqlite3.Error as e:
    print(f"Błąd podczas pracy z bazą danych: {e}")

finally:
    if conn:
        conn.close()
        print("Połączenie z bazą zostało zamknięte.") 