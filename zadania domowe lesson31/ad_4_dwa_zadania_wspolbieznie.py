"""
Dwa zadania wykonane współbieżnie (asyncio.gather)

Cel: porównać z Zadaniem 3 - pokazać, że asyncio.gather() uruchamia
korutyny współbieżnie, więc czas całkowity to MAKSIMUM z opóźnień,
a nie ich suma.
"""

import asyncio
import time


async def zadanie1():
    await asyncio.sleep(2)
    print("Zadanie 1 zakończone (spało 2s)")


async def zadanie2():
    await asyncio.sleep(1)
    print("Zadanie 2 zakończone (spało 1s)")


async def main():
    start = time.perf_counter()

    # asyncio.gather() uruchamia obie korutyny RÓWNOCZEŚNIE
    # (dokładniej: współbieżnie - obie "czekają" na sleep w tym
    # samym czasie, zamiast jedna po drugiej)
    await asyncio.gather(zadanie1(), zadanie2())

    czas_calkowity = time.perf_counter() - start
    print(f"Czas całkowity (współbieżnie): {czas_calkowity:.2f}s")
    # Oczekiwany czas: ~2s (maksimum z 2s i 1s), NIE 3s!


if __name__ == "__main__":
    asyncio.run(main())  
    
    
# Uruchom: python ad_4_dwa_zadania_wspolbieznie.py 