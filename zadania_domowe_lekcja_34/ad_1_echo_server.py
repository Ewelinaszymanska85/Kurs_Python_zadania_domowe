"""
Ad_1. WebSockets i GraphQL
Prosty echo server.

Serwer WebSocket, który odbiera wiadomość tekstową od klienta
i odsyła ją z powrotem z dodanym prefixem "Server: ".
"""

from aiohttp import web


async def websocket_handler(request):
    """
    Handler obsługujący połączenia WebSocket.

    Dla każdej otrzymanej wiadomości tekstowej, odsyła ją z powrotem
    do klienta z dodanym prefixem "Server: ".
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("✅ Nowy klient połączony!")

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            print(f"📥 Otrzymano: {msg.data}")

            # Odsyłamy wiadomość z prefixem "Server: "
            await ws.send_str(f"Server: {msg.data}")

        elif msg.type == web.WSMsgType.ERROR:
            print(f"❌ Błąd WebSocket: {ws.exception()}")

    print("❌ Klient rozłączony")
    return ws


# Tworzenie aplikacji aiohttp
app = web.Application()

# Rejestracja route'a dla WebSocket
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    print("🚀 Echo server działa na ws://localhost:8080/ws")
    web.run_app(app, host='localhost', port=8080) 