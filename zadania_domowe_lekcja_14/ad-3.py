import sqlite3

def suma_elektroniki():
    """Oblicza łączną wartość (sumę cen) produktów z kategorii 'Elektronika'."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT SUM(Produkty.cena)
            FROM Produkty
            JOIN Kategorie ON Produkty.id_kategorii = Kategorie.id_kategorii
            WHERE Kategorie.nazwa_kategorii = 'Elektronika'
        """

        wynik = cursor.execute(qr).fetchone()
        return wynik[0]

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return None

    finally:
        if conn:
            conn.close()


suma = suma_elektroniki()
if suma is not None:
    print(f"Łączna wartość elektroniki: {suma:.2f} zł")
else:
    print("Nie udało się obliczyć sumy.") 