import sqlite3

try:
    conn = sqlite3.connect("biblioteka.db")
    kursor = conn.cursor()

    ulubiony_autor = "Andrzej Sapkowski"

    kursor.execute("SELECT * FROM ksiazki WHERE autor = ?", (ulubiony_autor,))
    ksiazki = kursor.fetchall()

    if ksiazki:
        print(f"Książki autora {ulubiony_autor}:")
        for ksiazka in ksiazki:
            print(f"ID: {ksiazka[0]} | Tytuł: {ksiazka[1]} | Autor: {ksiazka[2]} | Rok: {ksiazka[3]}")
    else:
        print(f"Nie znaleziono książek autora {ulubiony_autor}.")

except sqlite3.Error as e:
    print(f"Błąd podczas pracy z bazą danych: {e}")

finally:
    if conn:
        conn.close()
        print("Połączenie z bazą zostało zamknięte.") 