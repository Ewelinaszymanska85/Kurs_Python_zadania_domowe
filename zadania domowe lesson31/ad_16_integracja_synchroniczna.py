"""
Integracja synchroniczna (asyncio.to_thread)

Cel: pokazać, jak wykonać zwykłe, SYNCHRONICZNE odczytywanie
plików (open()/read() - blokujące operacje) w sposób nieblokujący
dla Event Loop, delegując je do osobnych wątków przez
asyncio.to_thread().
"""

import asyncio
import os
import time


def odczytaj_plik_synchronicznie(sciezka: str) -> str:
    """
    Zwykła, SYNCHRONICZNA funkcja - blokująca operacja odczytu
    pliku z dysku. Nie ma tu żadnego async/await - to celowe,
    bo symuluje "starą", synchroniczną bibliotekę/kod.
    """
    with open(sciezka, "r") as plik:
        return plik.read()


async def odczytaj_asynchronicznie(sciezka: str) -> str:
    """
    Deleguje synchroniczną funkcję do osobnego wątku, żeby nie
    zablokować głównej pętli zdarzeń podczas odczytu z dysku.
    """
    zawartosc = await asyncio.to_thread(odczytaj_plik_synchronicznie, sciezka)
    return zawartosc


async def main():
    folder = "pliki_testowe"
    nazwy_plikow = [f"{folder}/plik_{i}.txt" for i in range(1, 101)]

    start = time.perf_counter()

    # Odczytujemy wszystkie 100 plików współbieżnie, każdy w
    # osobnym wątku roboczym, bez blokowania Event Loop
    zawartosci = await asyncio.gather(
        *(odczytaj_asynchronicznie(sciezka) for sciezka in nazwy_plikow)
    )

    print(f"Odczytano {len(zawartosci)} plików.")
    print(f"Przykładowa zawartość pierwszego pliku: {zawartosci[0]}")
    print(f"Czas całkowity: {time.perf_counter() - start:.4f}s")


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_16_integracja_synchroniczna.py 