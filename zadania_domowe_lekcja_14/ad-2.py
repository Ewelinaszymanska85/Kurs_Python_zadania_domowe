import sqlite3

def najdrozszy_produkt():
    """Znajduje nazwę i cenę najdroższego produktu w tabeli Produkty."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT nazwa_produktu, cena
            FROM Produkty
            WHERE cena = (SELECT MAX(cena) FROM Produkty)
        """

        return cursor.execute(qr).fetchone()

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return None

    finally:
        if conn:
            conn.close()


wynik = najdrozszy_produkt()
if wynik:
    print(f"Najdroższy produkt: {wynik[0]} - {wynik[1]:.2f} zł")
else:
    print("Nie udało się znaleźć najdroższego produktu.") 