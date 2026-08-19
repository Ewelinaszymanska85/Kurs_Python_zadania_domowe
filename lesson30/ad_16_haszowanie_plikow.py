"""
Równoległe haszowanie plików.
Oblicza skrót SHA256 dla każdego pliku przy pomocy
multiprocessing.Pool.
"""
import hashlib
import multiprocessing
import os


KATALOG = "pliki"


def oblicz_hash(sciezka):
    """Oblicza SHA256 dla podanego pliku."""

    sha256 = hashlib.sha256()

    with open(sciezka, "rb") as plik:
        while fragment := plik.read(8192):
            sha256.update(fragment)

    return (
        os.path.basename(sciezka),
        sha256.hexdigest()
    )


if __name__ == "__main__":
    pliki = [
        os.path.join(KATALOG, nazwa)
        for nazwa in os.listdir(KATALOG)
        if os.path.isfile(
            os.path.join(KATALOG, nazwa)
        )
    ]

    with multiprocessing.Pool() as pool:
        wyniki = pool.map(oblicz_hash, pliki)

    hashe = dict(wyniki)

    print("=== SHA256 PLIKÓW ===")

    for nazwa, hash_pliku in hashe.items():
        print(f"{nazwa}: {hash_pliku}")