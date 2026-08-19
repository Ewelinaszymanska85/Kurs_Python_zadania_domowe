"""
Aiohttp Klient - Publiczne API.

Program korzysta z aiohttp jako klienta HTTP.
Pobiera aktualną cenę Bitcoina w USD z publicznego API
CoinGecko i wyświetla ją w konsoli.
"""

import asyncio
import aiohttp


URL = "https://api.coingecko.com/api/v3/simple/price"


async def main():
    """Pobiera aktualną cenę Bitcoina w USD."""

    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }

    async with aiohttp.ClientSession() as session:

        async with session.get(URL, params=params) as response:

            if response.status != 200:
                print(
                    f"Błąd HTTP: {response.status}"
                )
                return

            dane = await response.json()

            cena_bitcoina = dane["bitcoin"]["usd"]

            print(
                f"Aktualna cena Bitcoina: "
                f"{cena_bitcoina} USD"
            )


if __name__ == "__main__":
    asyncio.run(main())