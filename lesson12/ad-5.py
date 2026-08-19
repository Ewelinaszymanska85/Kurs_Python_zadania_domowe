try:
    with open("nieistniejacy.txt", "r", encoding="utf-8") as plik:
        zawartosc = plik.read()
        print(zawartosc)

except FileNotFoundError:
    print("Błąd: plik 'nieistniejacy.txt' nie istnieje.")