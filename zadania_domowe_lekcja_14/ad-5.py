import sqlite3

def lista_klientow():
    """Pobiera imiona i adresy e-mail wszystkich klientów z tabeli Klienci."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT imie, email
            FROM Klienci
        """

        return cursor.execute(qr).fetchall()

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return []

    finally:
        if conn:
            conn.close()


klienci = lista_klientow()
if klienci:
    for klient in klienci:
        print(f"Imię: {klient[0]} | Email: {klient[1]}")
else:
    print("Nie znaleziono żadnych klientów.") 