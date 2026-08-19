"""
Sumowanie z wątkami i blokadą.
Dzieli dużą listę na 4 części, sumuje je w osobnych wątkach, i bezpiecznie
łączy wyniki cząstkowe w jedną, współdzieloną zmienną chronioną Lockiem.
"""
import threading

suma_calkowita = 0
blokada = threading.Lock()


def sumuj_fragment(fragment_listy):
    """Sumuje przekazany fragment listy i bezpiecznie dodaje do sumy globalnej."""
    global suma_calkowita
    suma_fragmentu = sum(fragment_listy)

    with blokada:
        suma_calkowita += suma_fragmentu


if __name__ == "__main__":
    duza_lista = list(range(1, 10_000_001))  # 10 milionów elementów

    liczba_watkow = 4
    rozmiar_fragmentu = len(duza_lista) // liczba_watkow

    watki = []
    for i in range(liczba_watkow):
        start_idx = i * rozmiar_fragmentu
        # ostatni wątek bierze resztę (na wypadek niepodzielności)
        end_idx = None if i == liczba_watkow - 1 else (i + 1) * rozmiar_fragmentu
        fragment = duza_lista[start_idx:end_idx]

        w = threading.Thread(target=sumuj_fragment, args=(fragment,))
        watki.append(w)
        w.start()

    for w in watki:
        w.join()

    print(f"Suma całkowita (wątki): {suma_calkowita}")
    print(f"Suma kontrolna (sum()): {sum(duza_lista)}")
    assert suma_calkowita == sum(duza_lista), "Błąd sumowania!"
    print("Wynik poprawny.")