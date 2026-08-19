"""
Ad_2. WebSockets i GraphQL
Klient wysyłający 3 wiadomości.

Klient WebSocket łączący się z serwerem (echo server z Zadania 1)
i wysyłający 3 kolejne wiadomości, wypisując otrzymane odpowiedzi.
"""

import aiohttp
import asyncio


async def websocket_client():
    """
    Łączy się z serwerem WebSocket i wysyła 3 wiadomości po kolei,
    czekając na odpowiedź serwera po każdej z nich.
    """
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://localhost:8080/ws') as ws:

            print("✅ Połączono z serwerem!")

            messages = ["Cześć", "Jak się masz?", "Do widzenia"]

            for msg in messages:
                await ws.send_str(msg)
                print(f"📤 Wysłano: {msg}")

                response = await ws.receive()

                if response.type == aiohttp.WSMsgType.TEXT:
                    print(f"📥 Otrzymano: {response.data}")

                await asyncio.sleep(1)

            await ws.close()
            print("❌ Połączenie zamknięte")


if __name__ == '__main__':
    asyncio.run(websocket_client())