import sqlite3
from dataclasses import dataclass


@dataclass
class Produkt:
    """Reprezentuje pojedynczy produkt zmapowany z wiersza tabeli Produkty."""
    id_produktu: int
    nazwa_produktu: str
    cena: float

    def __str__(self):
        return f"ID: {self.id_produktu} | {self.nazwa_produktu} – {self.cena:.2f} zł"


def pobierz_wszystkie_produkty():
    """Łączy się z bazą, pobiera wszystkie produkty i mapuje je na listę obiektów Produkt."""
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        qr = """--sql
            SELECT id_produktu, nazwa_produktu, cena
            FROM Produkty
        """

        wiersze = cursor.execute(qr).fetchall()
        return [Produkt(w[0], w[1], w[2]) for w in wiersze]

    except sqlite3.Error as e:
        print(f"Błąd podczas pracy z bazą danych: {e}")
        return []

    finally:
        if conn:
            conn.close()


produkty = pobierz_wszystkie_produkty()
if produkty:
    for produkt in produkty:
        print(produkt)
else:
    print("Nie znaleziono żadnych produktów.") 