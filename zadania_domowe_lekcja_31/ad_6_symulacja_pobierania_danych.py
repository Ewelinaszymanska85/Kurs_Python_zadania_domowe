"""
Symulacja pobierania danych (pogoda)

Cel: przygotowanie do Zadania 7 - stworzenie korutyny symulującej
pojedyncze zapytanie do zewnętrznego API pogodowego.
"""

import asyncio
import random


async def pobierz_pogode(miasto: str) -> dict:
    """
    Symuluje zapytanie do zewnętrznego API pogodowego - 1.5s
    opóźnienia (jak prawdziwe zapytanie sieciowe), a potem zwraca
    słownik z przykładowymi danymi.
    """
    await asyncio.sleep(1.5)
    return {
        "miasto": miasto,
        "temperatura": random.randint(-5, 30),
        "opis": random.choice(["słonecznie", "pochmurno", "deszczowo"]),
    }


async def main():
    wynik = await pobierz_pogode("Warszawa")
    print(wynik)


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchomienia: python ad_6_symulacja_pobierania_danych.py 