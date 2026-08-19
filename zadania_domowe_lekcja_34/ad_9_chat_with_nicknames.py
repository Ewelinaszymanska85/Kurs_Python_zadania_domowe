"""
Ad_9. WebSockets i GraphQL
Chat z nickami.

Chat room, gdzie pierwsza wiadomość od klienta ustala jego nick,
a każda kolejna wiadomość jest rozsyłana do wszystkich w formacie
"Nick: wiadomość".
"""

from aiohttp import web
from typing import Dict

# Słownik: połączenie WebSocket -> nick użytkownika
active_connections: Dict[web.WebSocketResponse, str] = {}


async def broadcast_message(message: str, sender: web.WebSocketResponse = None):
    """
    Rozsyła wiadomość do wszystkich aktywnych połączeń.
    """
    for connection in active_connections:
        if not connection.closed:
            try:
                await connection.send_str(message)
            except Exception as e:
                print(f"❌ Błąd wysyłania do klienta: {e}")


async def websocket_handler(request):
    """
    Handler obsługujący chat room z nickami.

    Pierwsza wiadomość od klienta jest traktowana jako jego nick
    (zapisywana, ale NIE rozsyłana jako wiadomość czatu). Każda
    kolejna wiadomość jest rozsyłana w formacie "Nick: treść".
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("✅ Nowy klient połączony - czeka na nick...")

    try:
        is_first_message = True

        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:

                if is_first_message:
                    # Pierwsza wiadomość = nick użytkownika
                    nickname = msg.data
                    active_connections[ws] = nickname
                    is_first_message = False

                    print(f"👤 Ustalono nick: {nickname}")
                    await broadcast_message(f"🟢 {nickname} dołączył do czatu!")

                else:
                    # Kolejne wiadomości = treść czatu
                    nickname = active_connections.get(ws, "Anonim")
                    formatted_message = f"{nickname}: {msg.data}"
                    print(f"💬 {formatted_message}")
                    await broadcast_message(formatted_message)

            elif msg.type == web.WSMsgType.ERROR:
                print(f"❌ Błąd WebSocket: {ws.exception()}")

    finally:
        nickname = active_connections.pop(ws, "Anonim")
        print(f"❌ {nickname} rozłączony")
        await broadcast_message(f"🔴 {nickname} opuścił czat")

    return ws


app = web.Application()
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    print("🚀 Chat z nickami działa na ws://localhost:8080/ws")
    web.run_app(app, host='localhost', port=8080)