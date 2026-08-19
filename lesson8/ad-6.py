class BladPrzetwarzaniaDanychError(Exception):
    pass

def przetworz_dane(dane):
    try:
        imie = dane["imie"]
        wiek = dane["wiek"]
        return f"{imie} ma {wiek} lat."
    except KeyError as e:
        brakujacy_klucz = e.args[0]

        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(f"Brak klucza: {brakujacy_klucz}\n")

        raise BladPrzetwarzaniaDanychError(
            f"Brak wymaganego klucza: {brakujacy_klucz}"
        ) from e

try:
    dane = {"imie": "Jan"}
    wynik = przetworz_dane(dane)
    print(wynik)
except BladPrzetwarzaniaDanychError as e:
    print("Błąd przetwarzania:", e) 