"""
Pierwszy proces.
Uruchamia osobny proces (nie wątek!), który oblicza silnię liczby 10.
W przeciwieństwie do wątków, procesy mają OSOBNĄ przestrzeń pamięci
i omijają ograniczenie GIL - prawdziwa równoległość dla obliczeń CPU-bound.
"""
import multiprocessing
import math


def oblicz_silnie(liczba):
    """Oblicza i wypisuje silnię podanej liczby."""
    wynik = math.factorial(liczba)
    print(f"Silnia z {liczba} = {wynik}")


if __name__ == "__main__":
    proces = multiprocessing.Process(target=oblicz_silnie, args=(10,))
    proces.start()
    proces.join()

    print("Proces zakończony.") 