import sqlite3

def zamowienia_anny():
    """Znajduje nazwy produktów zamówionych przez klienta 'Anna Nowak'."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT Produkty.nazwa_produktu
            FROM Klienci
            JOIN Zamowienia ON Klienci.id_klienta = Zamowienia.id_klienta
            JOIN Zamowienia_Produkty ON Zamowienia.id_zamowienia = Zamowienia_Produkty.id_zamowienia
            JOIN Produkty ON Zamowienia_Produkty.id_produktu = Produkty.id_produktu
            WHERE Klienci.imie = 'Anna Nowak'
        """

        return cursor.execute(qr).fetchall()

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return []

    finally:
        if conn:
            conn.close()


produkty = zamowienia_anny()
if produkty:
    print("Zamówione produkty przez Annę Nowak:")
    for produkt in produkty:
        print(f"- {produkt[0]}")
else:
    print("Brak zamówień.") 