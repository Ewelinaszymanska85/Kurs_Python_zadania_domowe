"""
Symulacja pobierania danych.
Porównanie czasu wykonania sekwencyjnego i wielowątkowego dla operacji
zawierających time.sleep (operacja I/O-bound, dobrze nadaje się do
przyspieszenia przez wątki, mimo GIL).
"""
import threading
import time


def pobierz_dane(id_danych):
    """Symuluje pobieranie danych (np. z sieci) przez opóźnienie."""
    print(f"Rozpoczynam pobieranie danych {id_danych}...")
    time.sleep(2)
    print(f"Zakończono pobieranie danych {id_danych}")


if __name__ == "__main__":
    identyfikatory = [1, 2, 3]

    # --- Wersja sekwencyjna ---
    start = time.time()
    for id_danych in identyfikatory:
        pobierz_dane(id_danych)
    czas_sekwencyjny = time.time() - start
    print(f"\nCzas sekwencyjny: {czas_sekwencyjny:.2f}s\n")

    # --- Wersja wielowątkowa ---
    start = time.time()
    watki = [threading.Thread(target=pobierz_dane, args=(id_danych,)) for id_danych in identyfikatory]
    for w in watki:
        w.start()
    for w in watki:
        w.join()
    czas_watkowy = time.time() - start
    print(f"\nCzas wielowątkowy: {czas_watkowy:.2f}s")

    print(f"\nPrzyspieszenie: {czas_sekwencyjny / czas_watkowy:.2f}x")
    # Wniosek: dla operacji I/O-bound (time.sleep symuluje np. czekanie
    # na sieć), wątki dają realne przyspieszenie, bo GIL jest zwalniany
    # na czas oczekiwania. 