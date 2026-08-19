"""
Asynchroniczny licznik

Cel: pokazać, że await asyncio.sleep() oddaje kontrolę do pętli
zdarzeń, zamiast blokować cały program (w przeciwieństwie do
time.sleep()).
"""

import asyncio


async def licznik(n: int):
    """
    Wypisuje liczby od 1 do n, czekając 1 sekundę między każdą.

    await asyncio.sleep(1) NIE blokuje - w tym czasie inne
    korutyny (gdyby jakieś działały współbieżnie) mogłyby
    normalnie pracować.
    """
    for i in range(1, n + 1):
        print(i)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(licznik(5)) 
    
    
# Uruchom: python ad_2_asychnoniczny_licznik.py