"""
Pobieranie statusów HTTP (httpx)

Cel: pierwsze prawdziwe zapytania sieciowe (nie symulacja) przy
użyciu asynchronicznej biblioteki httpx, zamiast synchronicznego
requests.
"""

import asyncio
import httpx


async def sprawdz_status(url: str, client: httpx.AsyncClient) -> tuple:
    """
    Wysyła zapytanie GET i zwraca parę (url, kod_statusu).
    """
    response = await client.get(url)
    return url, response.status_code


async def main():
    urls = [
        "https://httpbingo.org/status/200",
        "https://httpbingo.org/status/201",
        "https://httpbingo.org/status/404",
        "https://httpbingo.org/status/500",
    ]

    # Zawsze definiujemy timeout - żeby "wiszące" zapytanie nie
    # zablokowało programu w nieskończoność (zgodnie z materiałem lekcji)
    async with httpx.AsyncClient(timeout=10.0) as client:
        wyniki = await asyncio.gather(*(sprawdz_status(url, client) for url in urls))

    for url, status in wyniki:
        print(f"{url} -> {status}")


if __name__ == "__main__":
    asyncio.run(main()) 
    
    
# Uruchom: python_ad_9_statusy_http.py 