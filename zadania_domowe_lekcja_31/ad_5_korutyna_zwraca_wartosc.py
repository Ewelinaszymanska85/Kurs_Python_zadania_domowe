"""
Korutyna zwracająca wartość

Cel: pokazać, że korutyny mogą zwracać wartości (return) dokładnie
tak samo jak zwykłe funkcje - różnica jest tylko w tym, że wynik
odbiera się przez 'await', a nie przez samo wywołanie.
"""

import asyncio


async def oblicz_potege(liczba: float, potega: int) -> float:
    """
    Symuluje "kosztowne" obliczenie (2s opóźnienia) i zwraca
    wynik podniesienia liczby do potęgi.
    """
    await asyncio.sleep(2)
    wynik = liczba ** potega
    return wynik


async def main():
    # Odbieramy wynik korutyny przez await - działa jak zwykłe
    # przypisanie wyniku funkcji, tylko z dodatkowym 'await'
    wynik = await oblicz_potege(2, 10)
    print(f"Wynik obliczeń: {wynik}")


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_5_korutyna_zwraca_wartosc.py 