dane = input("Podaj imię i nazwisko (np. 'jan kowalski'): ")

# usunięcie zbędnych spacji
dane = dane.strip()

# każda część z wielkiej litery
dane = dane.title()

# długość tekstu
dlugosc = len(dane)

print("Sformatowane dane:", dane)
print("Długość tekstu:", dlugosc) 