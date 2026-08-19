"""
Wiele miast pobieranych współbieżnie

Cel: praktyczne zastosowanie asyncio.gather() - pobranie pogody
dla 3 miast naraz, zamiast czekać 1.5s * 3 = 4.5s sekwencyjnie.
"""

import asyncio
import random
import time


async def pobierz_pogode(miasto: str) -> dict:
    """
    Symuluje zapytanie do zewnętrznego API pogodowego.
    """
    await asyncio.sleep(1.5)
    return {
        "miasto": miasto,
        "temperatura": random.randint(-5, 30),
        "opis": random.choice(["słonecznie", "pochmurno", "deszczowo"]),
    }


async def main():
    miasta = ["Warszawa", "Kraków", "Gdańsk"]
    start = time.perf_counter()

    # gather() z rozpakowaniem listy (*) - uruchamia wszystkie
    # trzy korutyny współbieżnie, zamiast po kolei
    wyniki = await asyncio.gather(*(pobierz_pogode(miasto) for miasto in miasta))

    for pogoda in wyniki:
        print(pogoda)

    print(f"Czas całkowity: {time.perf_counter() - start:.2f}s")
    # Oczekiwany czas: ~1.5s (nie 4.5s!), bo wszystkie 3 zapytania
    # "czekają" na sleep w tym samym czasie


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_7_wiele_miast_wspolbieznie.py