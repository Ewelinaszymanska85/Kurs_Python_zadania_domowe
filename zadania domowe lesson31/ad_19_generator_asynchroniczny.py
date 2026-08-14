"""
Generator asynchroniczny (async for + yield)

Cel: pokazać asynchroniczny odpowiednik zwykłego generatora
Pythona - zamiast zwracać całą listę na raz, "produkuje" dane
jeden element na raz, z możliwością czekania (await) między
kolejnymi elementami.
"""

import asyncio


async def generator_liczb_pierwszych(limit: int):
    """
    Asynchroniczny generator - funkcja z 'async def' i 'yield'
    w środku. Zamiast 'return', używamy 'yield', żeby oddawać
    wartości pojedynczo, w miarę ich generowania.
    """
    def czy_pierwsza(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    liczba = 2
    while liczba <= limit:
        if czy_pierwsza(liczba):
            # Symulujemy, że "wyszukanie" każdej liczby pierwszej
            # zajmuje trochę czasu (np. zapytanie do zewnętrznego
            # źródła danych)
            await asyncio.sleep(0.3)
            yield liczba
        liczba += 1


async def main():
    print("Szukam liczb pierwszych do 30...")

    # 'async for' - specjalna pętla do iterowania po generatorach
    # asynchronicznych (zwykłe 'for' by tu nie zadziałało)
    async for liczba_pierwsza in generator_liczb_pierwszych(30):
        print(f"Znaleziono liczbę pierwszą: {liczba_pierwsza}")

    print("Zakończono generowanie.")


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python ad_19_generator_asynchroniczny.py 