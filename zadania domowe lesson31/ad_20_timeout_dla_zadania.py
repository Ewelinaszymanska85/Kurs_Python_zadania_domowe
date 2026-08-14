"""
Timeout dla zadania (asyncio.wait_for)

Cel: ostatnie zadanie - pokazać, jak zabezpieczyć się przed
"wiszącym" zadaniem, narzucając maksymalny czas jego wykonania.
Jeśli zadanie nie zdąży się zakończyć w tym czasie, zostaje
przerwane, a my łapiemy TimeoutError zamiast czekać w nieskończoność.
"""

import asyncio
import random


async def zadanie_o_losowym_czasie():
    """
    Zadanie, które losowo trwa od 1 do 5 sekund - czasem zmieści
    się w limicie czasowym, czasem nie (uruchom kilka razy, żeby
    zobaczyć oba scenariusze).
    """
    czas_trwania = random.uniform(1, 5)
    print(f"Zadanie rozpoczęte, potrwa {czas_trwania:.2f}s...")
    await asyncio.sleep(czas_trwania)
    return f"Zadanie zakończone po {czas_trwania:.2f}s"


async def main():
    try:
        # wait_for narzuca maksymalny czas (timeout=3) na wykonanie
        # zadania. Jeśli zadanie nie zdąży się zakończyć, zostaje
        # automatycznie anulowane, a wait_for rzuca TimeoutError
        wynik = await asyncio.wait_for(zadanie_o_losowym_czasie(), timeout=3.0)
        print(f"Sukces: {wynik}")
    except asyncio.TimeoutError:
        print("Zadanie trwało zbyt długo (>3s) i zostało przerwane!")


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_20_timeout_dla_zadania.py 