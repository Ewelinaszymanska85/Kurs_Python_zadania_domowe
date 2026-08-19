"""
Naprawa wyścigu przy pomocy threading.Lock.
Zabezpiecza dostęp do współdzielonej listy blokadą, gwarantując
poprawność wyniku niezależnie od szczegółów implementacji.
"""
import threading

wspolna_lista = []
blokada = threading.Lock()


def dodaj_jedynki():
    for _ in range(100_000):
        with blokada:  # zapewnia, że tylko jeden wątek na raz modyfikuje listę
            wspolna_lista.append(1)


def dodaj_dwojki():
    for _ in range(100_000):
        with blokada:
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
    assert len(wspolna_lista) == 200_000, "Błąd synchronizacji!"
    print("Wynik zawsze poprawny dzięki threading.Lock.")