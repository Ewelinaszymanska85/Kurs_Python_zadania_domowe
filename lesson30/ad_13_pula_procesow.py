"""
Pula procesów do przetwarzania danych.
Tworzy listę 100 losowych liczb i za pomocą multiprocessing.Pool
sprawdza równolegle, które liczby są pierwsze.
"""
import multiprocessing
import random
import math


def czy_pierwsza(liczba):
    """Sprawdza, czy podana liczba jest liczbą pierwszą."""

    if liczba < 2:
        return False

    if liczba == 2:
        return True

    if liczba % 2 == 0:
        return False

    for dzielnik in range(3, math.isqrt(liczba) + 1, 2):
        if liczba % dzielnik == 0:
            return False

    return True


if __name__ == "__main__":
    liczby = [
        random.randint(1, 1000)
        for _ in range(100)
    ]

    with multiprocessing.Pool() as pool:
        wyniki = pool.map(czy_pierwsza, liczby)

    liczby_pierwsze = [
        liczba
        for liczba, wynik in zip(liczby, wyniki)
        if wynik
    ]

    print(f"Liczby pierwsze: {liczby_pierwsze}")
    print(
        f"Znaleziono {len(liczby_pierwsze)} "
        f"liczb pierwszych."
    )