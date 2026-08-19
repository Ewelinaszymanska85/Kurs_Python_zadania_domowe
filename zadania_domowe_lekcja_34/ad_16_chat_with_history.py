"""
Ad_16. WebSockets i GraphQL
Chat z historią.

Rozszerzenie chat servera (broadcast) o trwałą historię wiadomości
zapisywaną w bazie SQLite. Przy połączeniu nowego klienta, serwer
wysyła mu ostatnie 50 wiadomości z historii, zanim zacznie
przekazywać nowe, na bieżąco.
"""

import sqlite3
from datetime import datetime
from aiohttp import web
from typing import Set

active_connections: Set[web.WebSocketResponse] = set()

DB_NAME = "chat_history.db"


def init_db():
    """
    Tworzy tabelę 'messages' w bazie SQLite, jeśli jeszcze
    nie istnieje. Wywoływane raz, przy starcie serwera.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_message(content: str):
    """
    Zapisuje pojedynczą wiadomość do bazy danych, wraz
    ze znacznikiem czasu utworzenia.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (content, created_at) VALUES (?, ?)",
        (content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_last_messages(limit: int = 50):
    """
    Pobiera ostatnie 'limit' wiadomości z bazy danych,
    posortowane od najstarszej do najnowszej (żeby wyświetlić
    je w naturalnej, chronologicznej kolejności).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT content, created_at FROM messages ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    # Odwracamy kolejność, żeby najstarsza wiadomość była pierwsza
    return list(reversed(rows))


async def broadcast_message(message: str):
    """
    Rozsyła wiadomość do wszystkich aktywnych połączeń.
    """
    for connection in active_connections:
        if not connection.closed:
            try:
                await connection.send_str(message)
            except Exception as e:
                print(f"❌ Błąd wysyłania: {e}")


async def websocket_handler(request):
    """
    Handler chat servera z historią wiadomości.

    Przy połączeniu nowego klienta, wysyła mu ostatnie 50
    wiadomości z bazy danych. Każda nowa wiadomość jest
    zapisywana do bazy ORAZ rozsyłana do wszystkich klientów.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    active_connections.add(ws)
    print(f"✅ Nowy klient! Łącznie: {len(active_connections)}")

    # Wysyłamy historię ostatnich 50 wiadomości TYLKO nowemu klientowi
    history = get_last_messages(50)
    if history:
        await ws.send_str(f"📜 Historia czatu ({len(history)} wiadomości):")
        for content, created_at in history:
            await ws.send_str(f"[{created_at}] {content}")
    else:
        await ws.send_str("📜 Historia czatu jest pusta.")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                print(f"💬 {msg.data}")

                # Zapisujemy wiadomość do bazy danych
                save_message(msg.data)

                # Rozsyłamy do wszystkich aktywnych klientów
                await broadcast_message(f"💬 {msg.data}")

            elif msg.type == web.WSMsgType.ERROR:
                print(f"❌ Błąd WebSocket: {ws.exception()}")

    finally:
        active_connections.discard(ws)
        print(f"❌ Klient rozłączony. Zostało: {len(active_connections)}")

    return ws


app = web.Application()
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    init_db()
    print("🚀 Chat z historią działa na ws://localhost:8080/ws")
    print(f"💾 Baza danych: {DB_NAME}")
    web.run_app(app, host='localhost', port=8080)