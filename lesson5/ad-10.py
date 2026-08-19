kursy = {"USD": 4.0, "EUR": 4.3}

while True:
    kwota_pln = float(input("Podaj kwotę w PLN: "))
    waluta = input("Podaj walutę (USD/EUR): ").upper()

    if waluta == "USD":
        wynik = kwota_pln / kursy["USD"]
    elif waluta == "EUR":
        wynik = kwota_pln / kursy["EUR"]
    else:
        print("Nieobsługiwana waluta.")
        continue

    print(f"Otrzymasz {wynik:.2f} {waluta}")

    dalej = input("Czy chcesz kontynuować? (tak/nie): ").lower()
    if dalej == "nie":
        break 