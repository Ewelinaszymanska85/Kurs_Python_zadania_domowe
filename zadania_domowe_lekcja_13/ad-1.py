import sqlite3

try:
    conn = sqlite3.connect("biblioteka.db")
    kursor = conn.cursor()

    kursor.execute("""
        CREATE TABLE IF NOT EXISTS ksiazki (
            id INTEGER PRIMARY KEY,
            tytul TEXT NOT NULL,
            autor TEXT NOT NULL,
            rok_wydania INTEGER
        )
    """)

    conn.commit()
    print("Tabela 'ksiazki' została utworzona (lub już istniała).")

except sqlite3.Error as e:
    print(f"Błąd podczas pracy z bazą danych: {e}")

finally:
    if conn:
        conn.close()
        print("Połączenie z bazą zostało zamknięte.") 
        