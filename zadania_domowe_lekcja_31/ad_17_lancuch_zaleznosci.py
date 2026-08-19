"""
Łańcuch zależności

Cel: pokazać realistyczny scenariusz z życia - część operacji MUSI
wykonać się po kolei (bo każda zależy od wyniku poprzedniej), ale
tam gdzie to możliwe (wiele niezależnych komentarzy dla różnych
wpisów), używamy współbieżności przez gather().
"""

import asyncio
import random


async def pobierz_user_id(username: str) -> int:
    """
    Krok 1: pobranie ID użytkownika na podstawie nazwy.
    """
    await asyncio.sleep(1)
    user_id = random.randint(1000, 9999)
    print(f"Krok 1: pobrano user_id={user_id} dla '{username}'")
    return user_id


async def pobierz_wpisy(user_id: int) -> list:
    """
    Krok 2: pobranie listy wpisów danego użytkownika - MUSI
    czekać na wynik Kroku 1 (potrzebuje user_id).
    """
    await asyncio.sleep(1)
    wpisy = [f"wpis_{user_id}_{i}" for i in range(1, 4)]
    print(f"Krok 2: pobrano wpisy: {wpisy}")
    return wpisy


async def pobierz_komentarze(wpis: str) -> list:
    """
    Krok 3: pobranie komentarzy dla JEDNEGO konkretnego wpisu.
    """
    await asyncio.sleep(1)
    komentarze = [f"komentarz_{i}_do_{wpis}" for i in range(1, 3)]
    return komentarze


async def main():
    # Kroki 1 i 2 MUSZĄ być sekwencyjne - każdy zależy od
    # poprzedniego (nie da się pobrać wpisów bez znajomości user_id)
    user_id = await pobierz_user_id("jan_kowalski")
    wpisy = await pobierz_wpisy(user_id)

    # Krok 3 - komentarze dla RÓŻNYCH wpisów są od siebie NIEZALEŻNE,
    # więc możemy je pobrać współbieżnie przez gather()
    print("Krok 3: pobieranie komentarzy dla wszystkich wpisów współbieżnie...")
    wszystkie_komentarze = await asyncio.gather(
        *(pobierz_komentarze(wpis) for wpis in wpisy)
    )

    for wpis, komentarze in zip(wpisy, wszystkie_komentarze):
        print(f"{wpis}: {komentarze}")


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: ad_17_lancuch_zaleznosci.py 