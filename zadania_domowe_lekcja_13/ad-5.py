import sqlite3

try:
    conn = sqlite3.connect("biblioteka.db")
    kursor = conn.cursor()

    kursor.execute("UPDATE ksiazki SET rok_wydania = ? WHERE id = ?", (1891, 1))
    conn.commit()
    print(f"Zaktualizowano {kursor.rowcount} wiersz(y).")

    kursor.execute("SELECT * FROM ksiazki WHERE id = ?", (1,))
    ksiazka = kursor.fetchone()

    if ksiazka:
        print(f"ID: {ksiazka[0]} | Tytuł: {ksiazka[1]} | Autor: {ksiazka[2]} | Rok: {ksiazka[3]}")
    else:
        print("Nie znaleziono książki o podanym ID.")

except sqlite3.Error as e:
    print(f"Błąd podczas pracy z bazą danych: {e}")

finally:
    if conn:
        conn.close()
        print("Połączenie z bazą zostało zamknięte.") 