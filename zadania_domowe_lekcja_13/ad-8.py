import sqlite3

try:
    conn = sqlite3.connect("uczelnia.db")
    kursor = conn.cursor()

    kursor.execute("""
        CREATE TABLE IF NOT EXISTS przypisania (
            id_przypisania INTEGER PRIMARY KEY,
            id_studenta INTEGER,
            id_audytorium INTEGER,
            FOREIGN KEY (id_studenta) REFERENCES studenci(id_studenta),
            FOREIGN KEY (id_audytorium) REFERENCES audytoria(id_audytorium)
        )
    """)

    conn.commit()
    print("Tabela 'przypisania' została utworzona (lub już istniała).")

except sqlite3.Error as e:
    print(f"Błąd podczas pracy z bazą danych: {e}")

finally:
    if conn:
        conn.close()
        print("Połączenie z bazą zostało zamknięte.") 