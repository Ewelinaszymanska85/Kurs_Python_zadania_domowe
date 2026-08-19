while True: 
    linia = input("Wpisz tekst (lub 'koniec', aby zakończyc): ") 
    
    if linia == "koniec": 
        print("Zamykanien programu...") 
        break 
    
    with open("dziennik.txt", "a", "encoding=utf-8") as plik: 
        plik.write(linia + "\n") 