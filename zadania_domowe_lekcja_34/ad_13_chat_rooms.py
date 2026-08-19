"""
Ad_13. WebSockets i GraphQL
Pokój chatowy z pokojami (chat rooms).

System chat rooms - klient dołącza do konkretnego pokoju komendą
"/join nazwa_pokoju", a wiadomości są rozsyłane TYLKO do klientów
znajdujących się w tym samym pokoju.
"""

from aiohttp import web
from typing import Dict, Set

# Słownik: nazwa pokoju -> zbiór połączeń WebSocket w tym pokoju
rooms: Dict[str, Set[web.WebSocketResponse]] = {}

# Słownik: połączenie WebSocket -> nazwa pokoju, w którym aktualnie jest
client_room: Dict[web.WebSocketResponse, str] = {}


async def broadcast_to_room(room_name: str, message: str):
    """
    Rozsyła wiadomość do wszystkich klientów znajdujących się
    w podanym pokoju.
    """
    if room_name not in rooms:
        return

    for connection in rooms[room_name]:
        if not connection.closed:
            try:
                await connection.send_str(message)
            except Exception as e:
                print(f"❌ Błąd wysyłania: {e}")


async def leave_current_room(ws: web.WebSocketResponse):
    """
    Usuwa klienta z jego obecnego pokoju (jeśli w jakimś jest)
    i powiadamia pozostałych.
    """
    old_room = client_room.get(ws)
    if old_room and old_room in rooms:
        rooms[old_room].discard(ws)
        await broadcast_to_room(old_room, "🔴 Użytkownik opuścił pokój")


async def websocket_handler(request):
    """
    Handler obsługujący system chat rooms.

    Komenda "/join nazwa_pokoju" przenosi klienta do wskazanego
    pokoju (opuszczając poprzedni, jeśli w jakimś był). Każda
    inna wiadomość jest rozsyłana TYLKO do klientów w tym samym
    pokoju co nadawca.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("✅ Nowy klient połączony (bez pokoju)")
    await ws.send_str("Witaj! Użyj '/join nazwa_pokoju' żeby dołączyć do pokoju.")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                text = msg.data

                if text.startswith("/join "):
                    # Komenda dołączenia do pokoju
                    room_name = text[len("/join "):].strip()

                    # Opuszczamy poprzedni pokój, jeśli w jakimś byliśmy
                    await leave_current_room(ws)

                    # Dołączamy do nowego pokoju
                    if room_name not in rooms:
                        rooms[room_name] = set()
                    rooms[room_name].add(ws)
                    client_room[ws] = room_name

                    print(f"👤 Klient dołączył do pokoju: {room_name}")
                    await ws.send_str(f"✅ Dołączono do pokoju: {room_name}")
                    await broadcast_to_room(room_name, f"🟢 Nowy użytkownik dołączył do pokoju {room_name}")

                else:
                    # Zwykła wiadomość czatu - rozsyłamy tylko w obrębie pokoju
                    room_name = client_room.get(ws)
                    if room_name:
                        print(f"💬 [{room_name}] {text}")
                        await broadcast_to_room(room_name, f"💬 {text}")
                    else:
                        await ws.send_str("⚠️ Musisz najpierw dołączyć do pokoju: /join nazwa_pokoju")

            elif msg.type == web.WSMsgType.ERROR:
                print(f"❌ Błąd WebSocket: {ws.exception()}")

    finally:
        await leave_current_room(ws)
        client_room.pop(ws, None)
        print("❌ Klient rozłączony")

    return ws


app = web.Application()
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    print("🚀 Chat rooms server działa na ws://localhost:8080/ws")
    web.run_app(app, host='localhost', port=8080)