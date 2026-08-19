"""
Równoległe przetwarzanie obrazów.
Obrazy są reprezentowane przez macierze losowych liczb.
Porównujemy przetwarzanie sekwencyjne z multiprocessing.Pool.
"""
import multiprocessing
import random
import time


LICZBA_OBRAZOW = 10
ROZMIAR = 1000


def utworz_obraz():
    """Tworzy obraz jako macierz losowych wartości."""

    return [
        [random.random() for _ in range(ROZMIAR)]
        for _ in range(ROZMIAR)
    ]


def zastosuj_filtr(obraz):
    """Wykonuje operację matematyczną na każdym pikselu."""

    return [
        [piksel * 1.1 for piksel in wiersz]
        for wiersz in obraz
    ]


if __name__ == "__main__":
    obrazy = [
        utworz_obraz()
        for _ in range(LICZBA_OBRAZOW)
    ]

    # Przetwarzanie sekwencyjne.
    start = time.perf_counter()

    for obraz in obrazy:
        zastosuj_filtr(obraz)

    czas_sekwencyjny = time.perf_counter() - start

    # Przetwarzanie równoległe.
    start = time.perf_counter()

    with multiprocessing.Pool() as pool:
        pool.map(zastosuj_filtr, obrazy)

    czas_rownolegly = time.perf_counter() - start

    print(
        f"Czas sekwencyjny: {czas_sekwencyjny:.2f} s"
    )
    print(
        f"Czas równoległy:  {czas_rownolegly:.2f} s"
    )

    if czas_rownolegly < czas_sekwencyjny:
        print("Przetwarzanie równoległe było szybsze.")
    else:
        print("Przetwarzanie sekwencyjne było szybsze.")