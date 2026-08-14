"""
Kolejka producent-konsument (asyncio.Queue)

Cel: pokazać asynchroniczny odpowiednik wzorca Producer-Consumer
z Lekcji 30 (tam używaliśmy queue.Queue z wątkami, tutaj używamy
asyncio.Queue z korutynami).
"""

import asyncio
import random


async def producent(kolejka: asyncio.Queue, liczba_elementow: int):
    """
    Generuje losowe liczby i wkłada je do kolejki.
    """
    for i in range(liczba_elementow):
        liczba = random.randint(1, 100)
        await kolejka.put(liczba)
        print(f"[PRODUCENT] Dodano do kolejki: {liczba}")
        await asyncio.sleep(0.3)

    # Sygnał końca danych - None informuje konsumenta, że producent skończył
    await kolejka.put(None)


async def konsument(kolejka: asyncio.Queue):
    """
    Pobiera liczby z kolejki i "przetwarza" je (tutaj: podwaja wartość).
    """
    while True:
        liczba = await kolejka.get()

        if liczba is None:
            # Otrzymaliśmy sygnał końca - kończymy pracę
            break

        wynik = liczba * 2
        print(f"[KONSUMENT] Przetworzono: {liczba} -> {wynik}")
        await asyncio.sleep(0.5)  # symulacja przetwarzania


async def main():
    kolejka = asyncio.Queue()

    # Producent i konsument działają WSPÓŁBIEŻNIE - konsument
    # przetwarza elementy "w locie", nie czekając aż producent
    # skończy dodawać wszystkie liczby
    await asyncio.gather(
        producent(kolejka, 5),
        konsument(kolejka),
    )

    print("Zakończono - wszystkie liczby przetworzone.")


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_14_kolejka_producent_konsument.py