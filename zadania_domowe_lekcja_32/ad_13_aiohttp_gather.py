"""
Aiohttp Client + asyncio.gather().
Pobiera dane z kilku adresów jednocześnie.
"""
import asyncio
import aiohttp


URL = "https://api.coindesk.com/v1/bpi/currentprice.json"


async def fetch(session, url):
    """Pobiera dane JSON z podanego adresu."""

    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()


async def main():

    urls = [URL, URL, URL]

    async with aiohttp.ClientSession() as session:

        wyniki = await asyncio.gather(
            *(fetch(session, url) for url in urls)
        )

    for numer, dane in enumerate(wyniki, start=1):
        cena = dane["bpi"]["USD"]["rate"]
        print(f"Zapytanie {numer}: {cena} USD")


if __name__ == "__main__":
    asyncio.run(main())