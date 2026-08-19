import sqlite3

def produkty_drozsze_od_sredniej():
    """Znajduje produkty, których cena jest wyższa niż średnia cena wszystkich produktów."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT nazwa_produktu, cena
            FROM Produkty
            WHERE cena > (SELECT AVG(cena) FROM Produkty)
            ORDER BY cena DESC
        """

        return cursor.execute(qr).fetchall()

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return []

    finally:
        if conn:
            conn.close()


produkty = produkty_drozsze_od_sredniej()
if produkty:
    for produkt in produkty:
        print(f"{produkt[0]} - {produkt[1]:.2f} zł")
else:
    print("Nie znaleziono produktów droższych od średniej.") 