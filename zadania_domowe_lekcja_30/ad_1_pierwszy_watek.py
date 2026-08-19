"""
Pierwszy wątek.
Tworzy jeden wątek, który czeka 3 sekundy i wypisuje komunikat,
podczas gdy główny program informuje o oczekiwaniu.
"""
import threading
import time


def zadanie_watku():
    """Funkcja wykonywana w osobnym wątku - czeka i wypisuje komunikat."""
    time.sleep(3)
    print("Wątek zakończył pracę!")


if __name__ == "__main__":
    watek = threading.Thread(target=zadanie_watku)
    watek.start()

    print("Główny program czeka na wątek...")
    watek.join()  # czekamy na zakończenie wątku przed zakończeniem programu

    print("Program główny zakończony.")