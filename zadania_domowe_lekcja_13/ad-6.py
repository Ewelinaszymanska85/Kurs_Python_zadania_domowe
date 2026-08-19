import sqlite3

try:
    conn = sqlite3.connect("uczelnia.db")
    kursor = conn.cursor()

    kursor.execute("""
        CREATE TABLE IF NOT EXISTS studenci (
            id_studenta INTEGER PRIMARY KEY,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL
        )
    """)

    kursor.execute("""
        CREATE TABLE IF NOT EXISTS audytoria (
            id_audytorium INTEGER PRIMARY KEY,
            nazwa_budynku TEXT NOT NULL,
            numer_sali INTEGER NOT NULL
        )
    """)

    conn.commit()
    print("Tabele 'studenci' i 'audytoria' zostały utworzone (lub już istniały).")

except sqlite3.Error as e:
    print(f"Błąd podczas pracy z bazą danych: {e}")

finally:
    if conn:
        conn.close()
        print("Połączenie z bazą zostało zamknięte.") 