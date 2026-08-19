"""
Proces z argumentem.
Uruchamia funkcję potega(liczba, pot) w osobnym procesie.
"""
import multiprocessing


def potega(liczba, pot):
    """Oblicza i wypisuje wynik potęgowania."""
    wynik = liczba ** pot
    print(f"{liczba} do potęgi {pot} = {wynik}")


if __name__ == "__main__":
    proces = multiprocessing.Process(target=potega, args=(5, 3))
    proces.start()
    proces.join()