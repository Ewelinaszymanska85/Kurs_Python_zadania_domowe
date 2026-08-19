"""
Współbieżne odliczanie

Cel: pokazać, że wiele niezależnych korutyn może "przeplatać się"
w czasie - każda odlicza swój własny czas, ale wszystkie działają
jednocześnie (współbieżnie) w jednym wątku.
"""

import asyncio


async def odliczaj(nazwa: str, start: int):
    """
    Odlicza od podanej wartości do zera, wypisując postęp co sekundę.
    """
    for pozostalo in range(start, 0, -1):
        print(f"[{nazwa}] pozostało: {pozostalo}s")
        await asyncio.sleep(1)
    print(f"[{nazwa}] Koniec odliczania!")


async def main():
    # Trzy niezależne odliczania, uruchomione WSPÓŁBIEŻNIE.
    # Zauważ w konsoli, że komunikaty z różnych odliczań będą się
    # przeplatać - to widoczny dowód działania Event Loop
    await asyncio.gather(
        odliczaj("Odliczanie A", 3),
        odliczaj("Odliczanie B", 5),
        odliczaj("Odliczanie C", 2),
    )


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_10_wspolbiezne_odliczanie.py 