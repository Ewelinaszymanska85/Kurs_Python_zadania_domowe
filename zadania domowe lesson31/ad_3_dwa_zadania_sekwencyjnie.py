"""
Dwa zadania wykonane sekwencyjnie

Cel: pokazać, że zwykłe 'await' (bez create_task) czeka na
zakończenie jednej korutyny, zanim przejdzie do następnej -
czasy się SUMUJĄ.
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

    # Zwykłe 'await' - czeka na KAŻDĄ korutynę osobno, po kolei
    await zadanie1()
    await zadanie2()

    czas_calkowity = time.perf_counter() - start
    print(f"Czas całkowity (sekwencyjnie): {czas_calkowity:.2f}s")
    # Oczekiwany czas: ~3s (2s + 1s) - czasy się SUMUJĄ


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_3_dwa_zadania_sekwencyjnie.py 