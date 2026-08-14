"""
Sumowanie wyników zadań

Cel: pokazać typowy wzorzec "fan-out / fan-in" - odpalamy wiele
niezależnych zadań współbieżnie, a potem agregujemy (sumujemy)
ich wyniki w jedną wartość.
"""

import asyncio
import random
import time


async def losowe_zadanie(id_zadania: int) -> int:
    """
    Symuluje zadanie w tle, które po losowym czasie (2-5s) zwraca
    losową liczbę.
    """
    czas_oczekiwania = random.uniform(2, 5)
    await asyncio.sleep(czas_oczekiwania)
    wynik = random.randint(1, 100)
    print(f"Zadanie {id_zadania}: wynik={wynik} (czekało {czas_oczekiwania:.2f}s)")
    return wynik


async def main():
    start = time.perf_counter()

    # 10 zadań uruchomionych współbieżnie
    wyniki = await asyncio.gather(*(losowe_zadanie(i) for i in range(1, 11)))

    suma = sum(wyniki)

    print(f"\nWszystkie wyniki: {wyniki}")
    print(f"Suma wszystkich wyników: {suma}")
    print(f"Czas całkowity: {time.perf_counter() - start:.2f}s")
    # Czas całkowity będzie zbliżony do NAJDŁUŻSZEGO pojedynczego
    # zadania (max ~5s), a nie sumy wszystkich 10 zadań


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_11_sumowanie_wynikow.py 