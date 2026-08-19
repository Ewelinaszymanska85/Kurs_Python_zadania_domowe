def oblicz_pole_prostokata(a, b):
    
    """
    Funkcja oblicza pole prostokąta.

    Argumenty:
    a -- długość pierwszego boku
    b -- długość drugiego boku

    Zwraca:
    Pole prostokąta jako iloczyn boków.
    """
    

    pole = a * b

    return pole


bok_a = 10
bok_b = 20

# Wywołanie funkcji i zapisanie wyniku
wynik = oblicz_pole_prostokata(bok_a, bok_b)

# Wyświetlenie wyniku na ekranie
print(f"Pole prostokąta o bokach {bok_a} i {bok_b} wynosi {wynik}.")