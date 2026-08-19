def analiza_listy(lista: list[int]) -> tuple[int, int, int]:
    """
    Analizuje listę liczb i zwraca jej podstawowe statystyki.

    Funkcja zwraca:
    - najmniejszą wartość (minimum)
    - największą wartość (maksimum)
    - sumę wszystkich elementów

    Parametry:
    lista (list[int]): lista liczb całkowitych

    Zwraca:
    tuple[int, int, int]: (min, max, suma)
    """

    minimum = min(lista)
    maksimum = max(lista)
    suma = sum(lista)

    return minimum, maksimum, suma


wynik = analiza_listy([3, 7, 1, 9, 4])
print("Min, Max, Suma:", wynik) 