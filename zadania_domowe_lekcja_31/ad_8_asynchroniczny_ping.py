"""
Asynchroniczny ping

Cel: ostatnie "proste" zadanie - symulacja pingowania kilku
hostów naraz, z losowym czasem odpowiedzi (realistyczne, bo
prawdziwe serwery też odpowiadają w różnym czasie).
"""

import asyncio
import random
import time


async def ping(host: str) -> str:
    """
    Symuluje "ping" do hosta - losowy czas oczekiwania (0.5-2s),
    imitujący zmienne opóźnienia sieciowe w prawdziwym świecie.
    """
    czas_odpowiedzi = random.uniform(0.5, 2.0)
    await asyncio.sleep(czas_odpowiedzi)
    return f"{host}: odpowiedź w {czas_odpowiedzi:.2f}s"


async def main():
    hosty = [f"serwer{i}.example.com" for i in range(1, 6)]
    start = time.perf_counter()

    wyniki = await asyncio.gather(*(ping(host) for host in hosty))

    for wynik in wyniki:
        print(wynik)

    print(f"Czas całkowity: {time.perf_counter() - start:.2f}s")
    # Czas całkowity będzie zbliżony do NAJWOLNIEJSZEGO pojedynczego
    # pingu (bo wszystkie działają współbieżnie), a nie sumy wszystkich


if __name__ == "__main__":
    asyncio.run(main())
    
    
# Uruchom: python ad_8_asynchroniczny_ping.py 
