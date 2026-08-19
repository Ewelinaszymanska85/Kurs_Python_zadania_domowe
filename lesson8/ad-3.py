def czytaj_plik(nazwa_pliku): 
    try: 
        with open(nazwa_pliku, "r", encoding="utf-8") as plik: 
            zawartosc = plik.read() 
    except FileNotFoundError:
        print("Błąd: plik nie istnieje.") 
    except PermissionError: 
        print("Błąd: brak uprawnień do odczytu pliku.") 
    else: 
        print("Zawartość pliku:\n") 
        print(zawartosc) 
    finally: 
        print("\nZakończono próbę odczytu pliku.") 
        
        
nazwa = input("Podaj nazwę pliku: ") 
czytaj_plik(nazwa) 
            