"""
Asynchroniczny, bezpieczny zapis do pliku

Cel: pokazać asynchroniczny odpowiednik Lock z Lekcji 30 (tam
threading.Lock chronił dostęp do współdzielonej zmiennej, tutaj
asyncio.Lock chroni dostęp do współdzielonego pliku - bez blokady
zapisy z różnych zadań mogłyby się przeplatać i zniszczyć plik).
"""

import asyncio
import aiofiles

NAZWA_PLIKU = "log_zadania15.txt"


async def zapisz_log(numer_zadania: int, lock: asyncio.Lock):
    """
    Symuluje pracę zadania, a na końcu bezpiecznie dopisuje linijkę
    do wspólnego pliku logów.
    """
    await asyncio.sleep(0.5)  # symulacja jakiejś pracy

    # Sekcja krytyczna - tylko jedno zadanie na raz może pisać do pliku
    async with lock:
        async with aiofiles.open(NAZWA_PLIKU, mode="a") as plik:
            await plik.write(f"Log od zadania {numer_zadania}\n")
        print(f"Zadanie {numer_zadania}: zapisano do pliku")


async def main():
    # Czyścimy plik przed startem, żeby test był powtarzalny
    async with aiofiles.open(NAZWA_PLIKU, mode="w") as plik:
        await plik.write("")

    lock = asyncio.Lock()

    await asyncio.gather(*(zapisz_log(i, lock) for i in range(1, 6)))

    print(f"\nZawartość pliku {NAZWA_PLIKU}:")
    async with aiofiles.open(NAZWA_PLIKU, mode="r") as plik:
        zawartosc = await plik.read()
        print(zawartosc)


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_15_zapis_do_pliku.py 