nazwa_pliku = input("Podaj nazwę pliku: ") 

try:
    with open(nazwa_pliku, "r",encoding="utf-8") as plik: 
        tekst = plik.read() 
        slowa = tekst.split() 
        liczba_slow = len(slowa) 
        
        print("Liczba słów w pliku:", liczba_slow) 
        
except FileNotFoundError: 
    print("Błąd: podany plik nie istnieje.") 