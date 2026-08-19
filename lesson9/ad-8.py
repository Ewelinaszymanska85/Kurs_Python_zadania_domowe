szukane_slowo = input("Podaj słowo do wyszukania (ERROR): ")

try:
    with open("log.txt", "r", encoding="utf-8") as plik_we:
        linie = plik_we.readlines()

    with open("wyniki_wyszukiwania.txt", "w", encoding="utf-8") as plik_wy:
        for linia in linie:
            if szukane_slowo in linia:
                plik_wy.write(linia)

    print("Zapisano wyniki do pliku wyniki_wyszukiwania.txt")

except FileNotFoundError:
    print("Błąd: plik log.txt nie istnieje.") 