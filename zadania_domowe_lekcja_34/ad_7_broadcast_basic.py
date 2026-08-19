"""
Ad_7. WebSockets i GraphQL
WebSocket broadcast podstawowy.

Serwer WebSocket, który rozsyła każdą otrzymaną wiadomość do
WSZYSTKICH aktualnie podłączonych klientów (nie tylko odsyła
ją z powrotem do nadawcy, jak echo server).
"""

from aiohttp import web
from typing import Set

# Zbiór wszystkich aktywnych połączeń WebSocket
active_connections: Set[web.WebSocketResponse] = set()


async def broadcast_message(message: str):
    """
    Wysyła podaną wiadomość do wszystkich aktywnych połączeń.

    Args:
        message: Treść wiadomości do rozesłania.
    """
    for connection in active_connections:
        if not connection.closed:
            try:
                await connection.send_str(message)
            except Exception as e:
                print(f"❌ Błąd wysyłania do klienta: {e}")


async def websocket_handler(request):
    """
    Handler obsługujący połączenia WebSocket z funkcją broadcast.

    Każda wiadomość otrzymana od dowolnego klienta jest rozsyłana
    do WSZYSTKICH podłączonych klientów (włącznie z nadawcą).
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    active_connections.add(ws)
    print(f"✅ Nowy klient! Łącznie połączeń: {len(active_connections)}")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                print(f"📥 Otrzymano: {msg.data}")

                # Rozsyłamy wiadomość do WSZYSTKICH podłączonych klientów
                await broadcast_message(msg.data)

            elif msg.type == web.WSMsgType.ERROR:
                print(f"❌ Błąd WebSocket: {ws.exception()}")

    finally:
        active_connections.discard(ws)
        print(f"❌ Klient rozłączony. Zostało: {len(active_connections)}")

    return ws


app = web.Application()
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    print("🚀 Broadcast server działa na ws://localhost:8080/ws")
    web.run_app(app, host='localhost', port=8080)