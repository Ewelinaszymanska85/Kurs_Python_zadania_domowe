"""
Komunikacja dwukierunkowa.
Proces nadrzędny wysyła listę liczb przez multiprocessing.Pipe.
Proces potomny oblicza sumę i średnią, a następnie odsyła wyniki.
"""
import multiprocessing


def oblicz(polaczenie):
    """Odbiera liczby i odsyła sumę oraz średnią."""

    liczby = polaczenie.recv()

    suma = sum(liczby)
    srednia = suma / len(liczby)

    polaczenie.send((suma, srednia))
    polaczenie.close()


if __name__ == "__main__":
    liczby = [10, 20, 30, 40, 50]

    rodzic, dziecko = multiprocessing.Pipe()

    proces = multiprocessing.Process(
        target=oblicz,
        args=(dziecko,)
    )

    proces.start()

    rodzic.send(liczby)

    suma, srednia = rodzic.recv()

    proces.join()

    print(f"Liczby: {liczby}")
    print(f"Suma: {suma}")
    print(f"Średnia: {srednia:.2f}")