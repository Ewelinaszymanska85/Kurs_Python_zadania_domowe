import json

try:
    with open("config.json", "r", encoding="utf-8") as plik:
        konfiguracja = json.load(plik)

    uzytkownik = konfiguracja.get("uzytkownik", "admin")
    motyw = konfiguracja.get("motyw", "ciemny")

    print(f"Witaj, {uzytkownik}! Twój motyw to {motyw}.")

except FileNotFoundError:
    print("Błąd: plik config.json nie istnieje.")

except json.JSONDecodeError:
    print("Błąd: plik config.json ma niepoprawny format.") 
