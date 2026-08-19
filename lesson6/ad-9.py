def silnia(n: int) -> int:
    """
    Oblicza silnię liczby n rekurencyjnie.

    Silnia n (n!) to iloczyn wszystkich liczb naturalnych od 1 do n.
    Warunek bazowy: 0! = 1

    Parametry:
    n (int): liczba, dla której obliczana jest silnia

    Zwraca:
    int: wartość silni
    """

    # Warunek bazowy rekurencji
    if n == 0:
        return 1

    # Wywołanie rekurencyjne
    return n * silnia(n - 1)


print(silnia(5))  # 120 