"""
Kopiowanie plików w tle.
Każdy plik z katalogu źródłowego jest kopiowany w osobnym wątku.
"""
import threading
import shutil
import os


KATALOG_ZRODLOWY = "zrodlo"
KATALOG_DOCELOWY = "kopia"


def kopiuj_plik(sciezka):
    """Kopiuje jeden plik do katalogu docelowego."""

    nazwa = os.path.basename(sciezka)
    cel = os.path.join(KATALOG_DOCELOWY, nazwa)

    print(f"Kopiowanie pliku {nazwa}...")

    try:
        shutil.copy2(sciezka, cel)
        print(f"Ukończono kopiowanie pliku {nazwa}")
    except OSError as blad:
        print(f"Błąd podczas kopiowania {nazwa}: {blad}")


if __name__ == "__main__":
    os.makedirs(KATALOG_DOCELOWY, exist_ok=True)

    pliki = [
        os.path.join(KATALOG_ZRODLOWY, nazwa)
        for nazwa in os.listdir(KATALOG_ZRODLOWY)
        if os.path.isfile(
            os.path.join(KATALOG_ZRODLOWY, nazwa)
        )
    ]

    watki = []

    for plik in pliki:
        watek = threading.Thread(
            target=kopiuj_plik,
            args=(plik,)
        )
        watki.append(watek)
        watek.start()

    for watek in watki:
        watek.join()

    print("Wszystkie pliki zostały skopiowane.")