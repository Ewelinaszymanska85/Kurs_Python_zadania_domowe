"""
Prosty serwer echa (TCP)

Cel: pokazać niskopoziomowe wsparcie asyncio dla sieci - serwer
TCP, który odsyła klientowi dokładnie to, co od niego otrzymał.

Uruchom ten plik w JEDNYM terminalu, a w DRUGIM, osobnym terminalu
uruchom ad_13_klient_echo.py, żeby przetestować połączenie.
"""

import asyncio


async def obsluz_klienta(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """
    Funkcja wywoływana automatycznie dla KAŻDEGO nowego klienta,
    który się połączy z serwerem.
    """
    adres = writer.get_extra_info("peername")
    print(f"Nowe połączenie od: {adres}")

    while True:
        dane = await reader.read(100)  # czeka na dane od klienta (max 100 bajtów)
        if not dane:
            # Klient zamknął połączenie
            break

        wiadomosc = dane.decode()
        print(f"Otrzymano od {adres}: {wiadomosc!r}")

        # Odsyłamy dokładnie to samo z powrotem ("echo")
        writer.write(dane)
        await writer.drain()  # czeka, aż dane faktycznie zostaną wysłane

    print(f"Zamknięto połączenie z {adres}")
    writer.close()


async def main():
    server = await asyncio.start_server(obsluz_klienta, "localhost", 8888)
    print("Serwer echa nasłuchuje na localhost:8888 (Ctrl+C, żeby zatrzymać)")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())  
    
    
# Uruchom: python ad_13_serwer_echo.py 