import csv

suma = 0.0

try:
    with open("produkty.csv", "r", encoding="utf-8") as plik:
        reader = csv.DictReader(plik)

        for wiersz in reader:
            cena = float(wiersz["cena"])
            suma += cena

    print(f"Suma cen wszystkich produktów: {suma:.2f}")

except FileNotFoundError:
    print("Błąd: plik produkty.csv nie istnieje.")

except KeyError:
    print("Błąd: brak kolumny 'cena' w pliku.")

except ValueError:
    print("Błąd: nieprawidłowa wartość ceny w pliku.") 