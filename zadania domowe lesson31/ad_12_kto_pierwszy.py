"""
Kto pierwszy, ten lepszy (asyncio.wait)

Cel: pokazać różnicę między gather() (czeka na WSZYSTKIE zadania)
a wait() z FIRST_COMPLETED (reaguje, gdy tylko PIERWSZE zadanie
się zakończy, nie czekając na resztę).
"""

import asyncio
import random


async def zadanie(id_zadania: int):
    """
    Zadanie kończące się po losowym czasie (1-5s).
    """
    czas = random.uniform(1, 5)
    await asyncio.sleep(czas)
    return f"Zadanie {id_zadania} zakończone (czas: {czas:.2f}s)"


async def main():
    taski = [asyncio.create_task(zadanie(i)) for i in range(1, 6)]

    # wait() z FIRST_COMPLETED zwraca kontrolę, gdy tylko JEDNO
    # zadanie się skończy - reszta nadal działa w tle (w 'pending')
    zakonczone, oczekujace = await asyncio.wait(
        taski, return_when=asyncio.FIRST_COMPLETED
    )

    print("--- Pierwsze zakończone zadanie ---")
    for task in zakonczone:
        print(task.result())

    print(f"\nLiczba zadań wciąż oczekujących w tle: {len(oczekujace)}")

    # Dobra praktyka: posprzątać po sobie - poczekać na resztę
    # zadań, żeby program nie zakończył się z "wiszącymi" taskami
    if oczekujace:
        await asyncio.wait(oczekujace)
        print("Pozostałe zadania również zakończone.")


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: ad_12_kto_pierwszy.py 