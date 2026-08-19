import sqlite3

def liczba_produktow():
    """Łączy się z bazą sklep.db i zlicza wszystkie produkty w tabeli Produkty."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT COUNT(*)
            FROM Produkty
        """

        wynik = cursor.execute(qr).fetchone()
        return wynik[0]

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return None

    finally:
        if conn:
            conn.close()


# Wywołanie funkcji i wyświetlenie wyniku
liczba = liczba_produktow()
if liczba is not None:
    print(f"Liczba produktów w bazie: {liczba}")
else:
    print("Nie udało się policzyć produktów.") 