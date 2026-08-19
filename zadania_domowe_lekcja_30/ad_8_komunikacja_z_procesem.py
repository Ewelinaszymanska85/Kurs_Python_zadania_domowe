"""
Komunikacja z procesem przy pomocy Queue.
Proces potomny pyta o imię, wysyła je do procesu nadrzędnego przez
multiprocessing.Queue - bezpieczny sposób wymiany danych między
procesami (procesy NIE dzielą pamięci, w przeciwieństwie do wątków).
"""
import multiprocessing


def zapytaj_o_imie(kolejka):
    """Pobiera imię od użytkownika i wysyła je przez kolejkę."""
    imie = input("Podaj swoje imię: ")
    kolejka.put(imie)


if __name__ == "__main__":
    kolejka = multiprocessing.Queue()

    proces = multiprocessing.Process(target=zapytaj_o_imie, args=(kolejka,))
    proces.start()
    proces.join()

    imie = kolejka.get()
    print(f"Witaj, {imie}!")