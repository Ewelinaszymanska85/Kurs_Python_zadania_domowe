"""
Kalkulator opóźnień.
Uruchamia trzy zadania asynchronicznie za pomocą asyncio.gather().
Całkowity czas powinien być zbliżony do najdłuższego opóźnienia.
"""
import asyncio
import time


async def zadanie(opoznienie):
    """Symuluje zadanie trwające określony czas."""

    await asyncio.sleep(opoznienie)


async def main():

    start = time.perf_counter()

    await asyncio.gather(
        zadanie(1),
        zadanie(4),
        zadanie(2)
    )

    czas = time.perf_counter() - start

    print(f"Czas wykonania: {czas:.2f} s")


if __name__ == "__main__":
    asyncio.run(main())