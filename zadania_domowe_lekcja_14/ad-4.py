import sqlite3

def srednia_cena_ksiazki():
    """Oblicza średnią cenę produktów w kategorii 'Książki'."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT AVG(Produkty.cena)
            FROM Produkty
            JOIN Kategorie ON Produkty.id_kategorii = Kategorie.id_kategorii
            WHERE Kategorie.nazwa_kategorii = 'Książki'
        """

        wynik = cursor.execute(qr).fetchone()
        return wynik[0]

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return None

    finally:
        if conn:
            conn.close()


srednia = srednia_cena_ksiazki()
if srednia is not None:
    print(f"Średnia cena książki: {srednia:.2f} zł")
else:
    print("Nie udało się obliczyć średniej.") 