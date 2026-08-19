from database_orm import dodaj_zadanie, pokaz_zadania, usun_zadanie, wyszukaj_zadania

while True:
    print("\n--- MENU ORM ---")
    print("1. Dodaj zadanie")
    print("2. Pokaz zadania")
    print("3. Usun zadanie")
    print("4. Wyszukaj zadanie")
    print("5. Wyjdz")

    wybor = input("Wybierz opcje: ")

    if wybor == "1":
        tytul = input("Podaj tytul zadania: ")
        dodaj_zadanie(tytul)
        print("Zadanie dodane!")

    elif wybor == "2":
        zadania = pokaz_zadania()
        if zadania:
            for z in zadania:
                status = "OK" if z.ukonczone else "X"
                print(f"ID: {z.id} | {z.tytul} | {status}")
        else:
            print("Brak zadan.")

    elif wybor == "3":
        id_zadania = int(input("Podaj ID zadania do usuniecia: "))
        usun_zadanie(id_zadania)
        print("Zadanie usuniete!")

    elif wybor == "4":
        fraza = input("Podaj fraze do wyszukania: ")
        wyniki = wyszukaj_zadania(fraza)
        if wyniki:
            for z in wyniki:
                status = "OK" if z.ukonczone else "X"
                print(f"ID: {z.id} | {z.tytul} | {status}")
        else:
            print(f"Nie znaleziono zadan zawierajacych fraze '{fraza}'.")

    elif wybor == "5":
        print("Do widzenia!")
        break

    else:
        print("Nieznana opcja, sprobuj jeszcze raz.")
