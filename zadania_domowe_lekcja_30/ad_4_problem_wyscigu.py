"""
Problem wyścigu (race condition).
Dwa wątki dodają elementy do współdzielonej listy bez synchronizacji -
demonstruje, że mimo GIL, niektóre operacje mogą prowadzić do
nieoczekiwanych rezultatów przy dużej liczbie iteracji.
"""
import threading

wspolna_lista = []


def dodaj_jedynki():
    for _ in range(100_000):
        wspolna_lista.append(1)


def dodaj_dwojki():
    for _ in range(100_000):
        wspolna_lista.append(2)


if __name__ == "__main__":
    watek1 = threading.Thread(target=dodaj_jedynki)
    watek2 = threading.Thread(target=dodaj_dwojki)

    watek1.start()
    watek2.start()
    watek1.join()
    watek2.join()

    print(f"Długość listy: {len(wspolna_lista)}")
    print(f"Oczekiwano: 200000")

    if len(wspolna_lista) == 200_000:
        print("Wynik poprawny (append na liście jest w CPythonie atomowy).")
    else:
        print("Wystąpił błąd synchronizacji!")

    # Uwaga: append() na liście w CPythonie jest w praktyce operacją
    # atomową dzięki GIL, więc ten konkretny przykład zwykle NIE pokaże
    # błędu. Prawdziwy race condition łatwiej zaobserwować przy operacjach
    # typu odczyt-modyfikacja-zapis (np. x += 1) - patrz Zadanie 18. 