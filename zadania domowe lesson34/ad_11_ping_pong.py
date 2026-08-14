"""
Ad_11. WebSockets i GraphQL
WebSocket Ping-Pong.

Serwer WebSocket, który co 30 sekund wysyła "ping" do klienta.
Klient musi odpowiedzieć "pong". Jeśli serwer nie otrzyma żadnej
wiadomości (w tym "pong") przez 60 sekund, rozłącza klienta.

Uwaga: do celów testowych w zadaniu domowym używamy skróconych
interwałów (5s ping, 10s timeout) zamiast 30s/60s z treści
zadania, żeby test można było wykonać w rozsądnym czasie.
Docelowe wartości (30s/60s) są zakomentowane obok.
"""

import asyncio
from aiohttp import web

# Interwały - SKRÓCONE do testów (docelowo: PING_INTERVAL=30, TIMEOUT=60)
PING_INTERVAL = 5   # sekund między kolejnymi pingami
TIMEOUT = 10         # sekund braku odpowiedzi = rozłączenie


async def send_pings(ws: web.WebSocketResponse):
    """
    Zadanie działające w tle, wysyłające "ping" do klienta
    co PING_INTERVAL sekund, dopóki połączenie jest aktywne.
    """
    while not ws.closed:
        await asyncio.sleep(PING_INTERVAL)
        if not ws.closed:
            print("📤 Wysyłam ping...")
            await ws.send_str("ping")


async def websocket_handler(request):
    """
    Handler obsługujący połączenie WebSocket z mechanizmem
    ping-pong. Jeśli klient nie odpowie w wyznaczonym czasie
    (TIMEOUT), połączenie jest zamykane.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("✅ Nowy klient połączony")

    # Uruchamiamy wysyłanie pingów jako oddzielne, równoległe zadanie
    ping_task = asyncio.create_task(send_pings(ws))

    try:
        while True:
            try:
                # Czekamy na wiadomość, ale maksymalnie TIMEOUT sekund
                msg = await asyncio.wait_for(ws.receive(), timeout=TIMEOUT)
            except asyncio.TimeoutError:
                print(f"⏱️  Brak odpowiedzi przez {TIMEOUT}s - rozłączam klienta")
                await ws.close()
                break

            if msg.type == web.WSMsgType.TEXT:
                if msg.data == "pong":
                    print("📥 Otrzymano: pong")
                else:
                    print(f"📥 Otrzymano: {msg.data}")
                    await ws.send_str(f"Echo: {msg.data}")

            elif msg.type in (web.WSMsgType.CLOSE, web.WSMsgType.CLOSED, web.WSMsgType.ERROR):
                break

    finally:
        ping_task.cancel()
        print("❌ Klient rozłączony")

    return ws


app = web.Application()
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    print("🚀 Serwer ping-pong działa na ws://localhost:8080/ws")
    print(f"ℹ️  Ping co {PING_INTERVAL}s, timeout {TIMEOUT}s (skrócone do testów)")
    web.run_app(app, host='localhost', port=8080)