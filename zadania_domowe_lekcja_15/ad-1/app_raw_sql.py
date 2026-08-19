from database_raw import TaskManagerRaw

manager = TaskManagerRaw()

while True:
    print("\n--- MENU ---")
    print("1. Dodaj zadanie")
    print("2. Pokaz zadania")
    print("3. Usun zadanie")
    print("4. Wyszukaj zadanie")
    print("5. Edytuj zadanie")
    print("6. Wyjdz")

    wybor = input("Wybierz opcje: ")

    if wybor == "1":
        tytul = input("Podaj tytul zadania: ")
        priorytet = int(input("Podaj priorytet (1-3): "))
        manager.dodaj(tytul, priorytet)
        print("Zadanie dodane!")

    elif wybor == "2":
        zadania = manager.pobierz()
        if zadania:
            for z in zadania:
                status = "OK" if z[2] else "X"
                print(f"ID: {z[0]} | {z[1]} | {status}")
        else:
            print("Brak zadan.")

    elif wybor == "3":
        try:
            id_zadania = int(input("Podaj ID zadania do usuniecia: "))
            if manager.usun(id_zadania):
                print("Zadanie usuniete!")
            else:
                print(f"Nie znaleziono zadania o ID {id_zadania}.")
        except ValueError:
            print("Podaj poprawny numer ID (liczbe calkowita).")

    elif wybor == "4":
        fraza = input("Podaj fraze do wyszukania: ")
        wyniki = manager.wyszukaj(fraza)
        if wyniki:
            for z in wyniki:
                status = "OK" if z[2] else "X"
                print(f"ID: {z[0]} | {z[1]} | {status} | priorytet: {z[3]}")
        else:
            print(f"Nie znaleziono zadan zawierajacych fraze '{fraza}'.")

    elif wybor == "5":
        try:
            id_zadania = int(input("Podaj ID zadania do edycji: "))
            nowy_tytul = input("Podaj nowy opis zadania: ")
            if manager.edytuj(id_zadania, nowy_tytul):
                print("Zadanie zaktualizowane!")
            else:
                print(f"Nie znaleziono zadania o ID {id_zadania}.")
        except ValueError:
            print("Podaj poprawny numer ID (liczbe calkowita).")

    elif wybor == "6":
        print("Do widzenia!")
        break

    else:
        print("Nieznana opcja, sprobuj jeszcze raz.")
