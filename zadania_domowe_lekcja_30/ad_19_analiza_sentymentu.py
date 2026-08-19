"""
Równoległa analiza sentymentu.
Symuluje zapytania do API AI i wykorzystuje ThreadPoolExecutor
do równoległego analizowania opinii.
"""
import random
import time
from concurrent.futures import ThreadPoolExecutor


opinie = [
    "Produkt jest świetny.",
    "Jestem bardzo zadowolony z zakupu.",
    "Produkt spełnił moje oczekiwania.",
    "Bardzo dobra jakość.",
    "Polecam ten produkt.",
    "Produkt działa bez problemów.",
    "Świetny stosunek jakości do ceny.",
    "Produkt wygląda bardzo dobrze.",
    "Jestem zadowolony.",
    "Produkt jest w porządku.",
    "Nie mam zdania.",
    "Produkt jest przeciętny.",
    "Spełnia podstawowe wymagania.",
    "Niczym się nie wyróżnia.",
    "Produkt jest słabej jakości.",
    "Nie jestem zadowolony.",
    "Produkt często się psuje.",
    "Nie polecam tego produktu.",
    "Jakość jest bardzo słaba.",
    "Zakup okazał się rozczarowaniem."
]


def analizuj_sentyment(zdanie):
    """Symuluje analizę sentymentu przez API AI."""

    time.sleep(random.uniform(0.5, 2))

    wynik = random.choice([
        "Pozytywny",
        "Negatywny",
        "Neutralny"
    ])

    return zdanie, wynik


if __name__ == "__main__":
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=5) as executor:
        wyniki = executor.map(
            analizuj_sentyment,
            opinie
        )

    czas = time.perf_counter() - start

    print("=== WYNIKI ANALIZY ===")

    for zdanie, wynik in wyniki:
        print(f"{wynik:10} | {zdanie}")

    print(f"\nCzas wykonania: {czas:.2f} s")