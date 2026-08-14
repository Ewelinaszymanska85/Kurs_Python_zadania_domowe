"""
Ad_8. WebSockets i GraphQL
Pomiar czasu połączenia.

Serwer WebSocket (echo), który mierzy, jak długo dany klient
pozostawał połączony - od momentu nawiązania połączenia (connect)
do momentu rozłączenia (disconnect).
"""

import time
from aiohttp import web


async def websocket_handler(request):
    """
    Handler obsługujący połączenia WebSocket z pomiarem czasu.

    Zapisuje znacznik czasu w momencie połączenia, a przy
    rozłączeniu oblicza i wyświetla, jak długo trwało połączenie.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Zapisujemy moment nawiązania połączenia
    connect_time = time.time()
    print(f"✅ Nowy klient połączony o {time.strftime('%H:%M:%S')}")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                print(f"📥 Otrzymano: {msg.data}")
                await ws.send_str(f"Echo: {msg.data}")

            elif msg.type == web.WSMsgType.ERROR:
                print(f"❌ Błąd WebSocket: {ws.exception()}")

    finally:
        # Obliczamy czas trwania połączenia
        disconnect_time = time.time()
        duration = disconnect_time - connect_time
        print(f"❌ Klient rozłączony o {time.strftime('%H:%M:%S')}")
        print(f"⏱️  Czas połączenia: {duration:.2f} sekund")

    return ws


app = web.Application()
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    print("🚀 Serwer z pomiarem czasu połączenia działa na ws://localhost:8080/ws")
    web.run_app(app, host='localhost', port=8080)