import sqlite3

try:
    conn = sqlite3.connect("biblioteka.db")
    kursor = conn.cursor()

    kursor.execute("SELECT * FROM ksiazki")
    ksiazki = kursor.fetchall()

    for ksiazka in ksiazki:
        print(f"ID: {ksiazka[0]} | Tytuł: {ksiazka[1]} | Autor: {ksiazka[2]} | Rok: {ksiazka[3]}")

except sqlite3.Error as e:
    print(f"Błąd podczas pracy z bazą danych: {e}")

finally:
    if conn:
        conn.close()
        print("Połączenie z bazą zostało zamknięte.") 