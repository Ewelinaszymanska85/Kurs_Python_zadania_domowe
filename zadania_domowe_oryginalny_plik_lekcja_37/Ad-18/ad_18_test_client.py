import asyncio
import json

import aiohttp


WS_URL = "ws://localhost:8090/ws"


async def client_a() -> None:
    """Klient A: łączy się, wysyła jedną wiadomość, potem nasłuchuje."""
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(WS_URL) as ws:
            print("[Klient A] Polaczony.")

            await asyncio.sleep(1)

            await ws.send_str(json.dumps({"message": "Czesc od Klienta A!"}))
            print("[Klient A] Wyslano wiadomosc.")

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    print(f"[Klient A] Odebrano: {data['message']} (obsluzone przez: {data['served_by']})")
                    break


async def client_b() -> None:
    """Klient B: łączy się i tylko nasłuchuje wiadomości."""
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(WS_URL) as ws:
            print("[Klient B] Polaczony, czekam na wiadomosci...")

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    print(f"[Klient B] Odebrano: {data['message']} (obsluzone przez: {data['served_by']})")
                    break


async def main() -> None:
    print("=== TEST WEBSOCKET CHAT + REDIS PUB/SUB ===\n")

    await asyncio.gather(client_a(), client_b())


if __name__ == "__main__":
    asyncio.run(main())