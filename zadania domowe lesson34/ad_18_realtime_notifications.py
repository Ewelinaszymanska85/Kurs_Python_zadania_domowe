"""
Ad_18. WebSockets i GraphQL
Real-time notifications.

System powiadomień łączący dwa mechanizmy:
1. REST API (zwykłe HTTP POST) do tworzenia nowych powiadomień
2. WebSocket endpoint, który natychmiast "pushuje" (wysyła) każde
   nowo utworzone powiadomienie do wszystkich połączonych klientów

To pokazuje typowy wzorzec: REST do zapisu danych, WebSocket
do powiadamiania klientów o zmianach w czasie rzeczywistym.
"""

import json
from aiohttp import web
from typing import Set

# Aktywne połączenia WebSocket oczekujące na powiadomienia
notification_clients: Set[web.WebSocketResponse] = set()


async def push_notification(notification: dict):
    """
    Wysyła (pushuje) powiadomienie do wszystkich aktualnie
    podłączonych klientów WebSocket, w formacie JSON.
    """
    message = json.dumps(notification, ensure_ascii=False)
    for client in notification_clients:
        if not client.closed:
            try:
                await client.send_str(message)
            except Exception as e:
                print(f"❌ Błąd wysyłania powiadomienia: {e}")


async def create_notification_handler(request):
    """
    Endpoint REST (POST /api/notifications/) do tworzenia nowego
    powiadomienia. Oczekuje JSON w Body, np.:
    {"title": "Nowa wiadomość", "message": "Masz nową wiadomość!"}

    Po utworzeniu, powiadomienie jest NATYCHMIAST rozsyłane przez
    WebSocket do wszystkich podłączonych klientów.
    """
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Nieprawidłowy JSON"}, status=400)

    title = data.get("title")
    message_text = data.get("message")

    if not title or not message_text:
        return web.json_response(
            {"error": "Wymagane pola: title, message"},
            status=400
        )

    notification = {
        "type": "notification",
        "title": title,
        "message": message_text,
    }

    print(f"🔔 Nowe powiadomienie: {title}")

    # Natychmiastowe wysłanie powiadomienia przez WebSocket
    await push_notification(notification)

    return web.json_response({"status": "sent", "notification": notification}, status=201)


async def websocket_notifications_handler(request):
    """
    Endpoint WebSocket (ws://.../ws/notifications), przez który
    klienci nasłuchują nowych powiadomień w czasie rzeczywistym.

    Klient nie musi nic wysyłać - po prostu czeka na powiadomienia
    push, które trafiają do niego automatycznie, gdy ktoś utworzy
    nowe powiadomienie przez REST API.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    notification_clients.add(ws)
    print(f"✅ Klient nasłuchuje powiadomień. Łącznie: {len(notification_clients)}")

    try:
        async for msg in ws:
            # Ten endpoint nie oczekuje wiadomości od klienta,
            # ale musimy nasłuchiwać, żeby wykryć rozłączenie
            if msg.type == web.WSMsgType.ERROR:
                print(f"❌ Błąd WebSocket: {ws.exception()}")

    finally:
        notification_clients.discard(ws)
        print(f"❌ Klient rozłączony. Zostało: {len(notification_clients)}")

    return ws


app = web.Application()
app.router.add_post('/api/notifications/', create_notification_handler)
app.router.add_get('/ws/notifications', websocket_notifications_handler)


if __name__ == '__main__':
    print("🚀 System powiadomień działa na http://localhost:8080")
    print("   REST:      POST http://localhost:8080/api/notifications/")
    print("   WebSocket: ws://localhost:8080/ws/notifications")
    web.run_app(app, host='localhost', port=8080)