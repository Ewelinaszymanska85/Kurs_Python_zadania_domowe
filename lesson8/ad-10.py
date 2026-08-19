suma = 0

try:
    nazwa_pliku = input("Podaj nazwę pliku: ")

    with open(nazwa_pliku, "r") as plik:
        for linia in plik:
            try:
                liczba = int(linia.strip())
                suma += liczba
            except ValueError:
                # ignorujemy błędne linie
                pass

except FileNotFoundError:
    print("Plik nie istnieje.")

finally:
    print("Suma liczb:", suma) 