import json
import os

PLIK = "zadania.json"

# ---- wczytywanie danych ----
def wczytaj_zadania():
    if os.path.exists(PLIK):
        try:
            with open(PLIK, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# ---- zapisywanie danych ----
def zapisz_zadania(zadania):
    with open(PLIK, "w", encoding="utf-8") as f:
        json.dump(zadania, f, ensure_ascii=False, indent=4)

# ---- wyświetlanie ----
def pokaz_zadania(zadania):
    if not zadania:
        print("Brak zadań.")
        return
    print("\nLista zadań:")
    for i, zadanie in enumerate(zadania, start=1):
        print(f"{i}. {zadanie}")

# ---- program główny ----
zadania = wczytaj_zadania()

while True:
    print("\n--- MENU ---")
    print("1. Dodaj zadanie")
    print("2. Pokaż zadania")
    print("3. Zapisz i wyjdź")

    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        nowe = input("Podaj treść zadania: ")
        zadania.append(nowe)
        print("Zadanie dodane!")

    elif wybor == "2":
        pokaz_zadania(zadania)

    elif wybor == "3":
        zapisz_zadania(zadania)
        print("Zadania zapisane. Do widzenia!")
        break

    else:
        print("Nieznana opcja, spróbuj ponownie.")