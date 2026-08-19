"""
Ad_3. WebSockets i GraphQL
Licznik połączeń.

Zmodyfikowany echo server, który przy każdym nowym połączeniu
wysyła wiadomość informującą klienta, którym z kolei jest
aktywnym połączeniem.
"""

from aiohttp import web

# Licznik aktywnych połączeń (globalny, współdzielony między
# wszystkimi klientami)
active_connections_count = 0


async def websocket_handler(request):
    """
    Handler obsługujący połączenia WebSocket.

    Przy nawiązaniu połączenia, zwiększa licznik aktywnych
    połączeń i informuje klienta, którym z kolei jest klientem.
    Przy rozłączeniu, zmniejsza licznik.
    """
    global active_connections_count

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Zwiększamy licznik i informujemy klienta
    active_connections_count += 1
    print(f"✅ Nowy klient połączony! Aktywnych: {active_connections_count}")

    await ws.send_str(f"Jesteś klientem numer {active_connections_count}")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                print(f"📥 Otrzymano: {msg.data}")
                await ws.send_str(f"Server: {msg.data}")

            elif msg.type == web.WSMsgType.ERROR:
                print(f"❌ Błąd WebSocket: {ws.exception()}")

    finally:
        # Zmniejszamy licznik, gdy klient się rozłączy
        active_connections_count -= 1
        print(f"❌ Klient rozłączony. Aktywnych: {active_connections_count}")

    return ws


app = web.Application()
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    print("🚀 Serwer z licznikiem połączeń działa na ws://localhost:8080/ws")
    web.run_app(app, host='localhost', port=8080)