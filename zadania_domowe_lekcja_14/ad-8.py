import sqlite3

def kategorie_z_liczba_produktow():
    """Wyświetla nazwę każdej kategorii oraz liczbę produktów w niej."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT Kategorie.nazwa_kategorii, COUNT(Produkty.id_produktu) AS liczba_produktow
            FROM Kategorie
            JOIN Produkty ON Kategorie.id_kategorii = Produkty.id_kategorii
            GROUP BY Kategorie.nazwa_kategorii
            ORDER BY liczba_produktow DESC
        """

        return cursor.execute(qr).fetchall()

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return []

    finally:
        if conn:
            conn.close()


wyniki = kategorie_z_liczba_produktow()
if wyniki:
    for wiersz in wyniki:
        print(f"Kategoria: {wiersz[0]} | Liczba produktów: {wiersz[1]}")
else:
    print("Nie znaleziono żadnych kategorii.") 