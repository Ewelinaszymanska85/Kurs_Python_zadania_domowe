imiona = ["Anna", "Jan", "Piotr", "Kasia"]

szukane_imie = input("Podaj imię do wyszukania: ")

for imie in imiona:
    if imie == szukane_imie:
        print("Znaleziono!")
        break
else:
    # Ten blok wykona się tylko wtedy, gdy pętla nie została przerwana
    print("Nie znaleziono imienia na liście.") 