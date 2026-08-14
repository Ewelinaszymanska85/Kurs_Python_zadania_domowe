"""
Anulowanie zadania (Task Cancellation)

Cel: pokazać, jak bezpiecznie przerwać działające w tle zadanie
(np. worker, który miałby pracować bez końca) i jak taki task
może "posprzątać po sobie" reagując na CancelledError.
"""

import asyncio


async def pracownik_w_tle():
    """
    Symuluje długo działający proces w tle (np. worker nasłuchujący
    na zdarzenia) - normalnie działałby wiecznie, dopóki nie
    zostanie jawnie anulowany.
    """
    try:
        licznik = 0
        while True:
            licznik += 1
            print(f"Pracuję... (cykl {licznik})")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        # To miejsce wykonuje się, gdy ktoś wywoła task.cancel()
        print("Otrzymałem sygnał anulowania! Sprzątam zasoby...")
        # Tutaj normalnie zamknęlibyśmy połączenia, zapisali stan itd.
        print("Posprzątane, kończę działanie.")
        raise  # Ważne: propagujemy CancelledError dalej


async def main():
    task = asyncio.create_task(pracownik_w_tle())

    # Pozwalamy pracownikowi działać przez 5 sekund
    await asyncio.sleep(5)

    print("\n--- Główny program: czas minął, anuluję zadanie ---")
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Główny program: potwierdzono, że zadanie zostało anulowane.")


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_18_anulowanie_zadania.py 