import sqlite3

def znajdz_sale_studenta(nazwisko):
    conn = sqlite3.connect("uczelnia.db")
    kursor = conn.cursor()

    kursor.execute("""
        SELECT studenci.imie, studenci.nazwisko, audytoria.nazwa_budynku, audytoria.numer_sali
        FROM studenci
        JOIN przypisania ON studenci.id_studenta = przypisania.id_studenta
        JOIN audytoria ON przypisania.id_audytorium = audytoria.id_audytorium
        WHERE studenci.nazwisko = ?
    """, (nazwisko,))

    wynik = kursor.fetchone()
    conn.close()

    if wynik:
        print(f"{wynik[0]} {wynik[1]} -> {wynik[2]}, sala {wynik[3]}")
    else:
        print(f"Nie znaleziono studenta o nazwisku '{nazwisko}'.")


# Testowanie
znajdz_sale_studenta("Kowalska")
znajdz_sale_studenta("Nowak")
znajdz_sale_studenta("Nieznany") 
