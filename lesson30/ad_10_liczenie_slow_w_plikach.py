"""
Równoległe liczenie słów w plikach.
Przeszukuje wszystkie pliki .txt w bieżącym katalogu, licząc wystąpienia
zadanego słowa - każdy plik w osobnym wątku, wynik bezpiecznie sumowany.
"""
import threading
import glob

licznik_calkowity = 0
blokada = threading.Lock()


def policz_w_pliku(sciezka_pliku, szukane_slowo):
    """Liczy wystąpienia słowa w jednym pliku i dodaje do licznika globalnego."""
    global licznik_calkowity

    try:
        with open(sciezka_pliku, "r", encoding="utf-8") as f:
            tresc = f.read()
        liczba_wystapien = tresc.lower().split().count(szukane_slowo.lower())

        with blokada:
            licznik_calkowity += liczba_wystapien

        print(f"{sciezka_pliku}: znaleziono {liczba_wystapien} wystąpień")
    except Exception as e:
        print(f"Błąd przy pliku {sciezka_pliku}: {e}")


if __name__ == "__main__":
    szukane_slowo = "python"

    # Tworzymy przykładowe pliki testowe, żeby zadanie dało się od razu uruchomić
    przykladowe_tresci = [
        "Python to świetny język programowania. Uczę się Python od kilku miesięcy.",
        "Django to framework napisany w Pythonie. Bardzo lubię Python.",
        "To jest plik bez słowa kluczowego wcale.",
    ]
    for i, tresc in enumerate(przykladowe_tresci, start=1):
        with open(f"przyklad_{i}.txt", "w", encoding="utf-8") as f:
            f.write(tresc)

    pliki_txt = glob.glob("*.txt")
    print(f"Znaleziono {len(pliki_txt)} plików .txt\n")

    watki = [threading.Thread(target=policz_w_pliku, args=(plik, szukane_slowo)) for plik in pliki_txt]

    for w in watki:
        w.start()
    for w in watki:
        w.join()

    print(f"\nŁączna liczba wystąpień słowa '{szukane_slowo}': {licznik_calkowity}")