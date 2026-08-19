import sqlite3

def znajdz_produkty_w_kategorii(nazwa_kategorii):
    """Zwraca listę krotek (nazwa_produktu, cena) dla produktów w podanej kategorii."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT Produkty.nazwa_produktu, Produkty.cena
            FROM Produkty
            JOIN Kategorie ON Produkty.id_kategorii = Kategorie.id_kategorii
            WHERE Kategorie.nazwa_kategorii = ?
        """

        return cursor.execute(qr, (nazwa_kategorii,)).fetchall()

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return []

    finally:
        if conn:
            conn.close()


# Testowanie
kategorie = ["Elektronika", "Książki", "Dom i ogród"]

for kategoria in kategorie:
    print(f"\nKategoria: {kategoria}")
    produkty = znajdz_produkty_w_kategorii(kategoria)
    if produkty:
        for produkt in produkty:
            print(f"  - {produkt[0]} - {produkt[1]:.2f} zł")
    else:
        print("  (brak produktów)")       