"""
Wiele wątków.
Uruchamia 5 wątków, każdy z własnym numerem, i czeka na wszystkie.
"""
import threading


def przywitaj_sie(numer_watku):
    """Wypisuje komunikat z numerem danego wątku."""
    print(f"Jestem wątkiem numer {numer_watku}")


if __name__ == "__main__":
    watki = []

    for i in range(1, 6):
        w = threading.Thread(target=przywitaj_sie, args=(i,))
        watki.append(w)
        w.start()

    # Czekamy na zakończenie WSZYSTKICH wątków
    for w in watki:
        w.join()

    print("Wszystkie wątki zakończyły pracę.") 