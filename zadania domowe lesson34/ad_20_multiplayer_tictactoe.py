"""
Ad_20. WebSockets i GraphQL
Multiplayer game server (Tic-Tac-Toe).

Prosty serwer gry w kółko i krzyżyk (tic-tac-toe) dla dwóch graczy,
komunikujących się przez WebSocket. Serwer przechowuje stan planszy,
przypisuje symbole graczom (X/O), waliduje ruchy i rozsyła aktualny
stan gry obu graczom po każdym ruchu.
"""

import json
from aiohttp import web
from typing import List, Optional

# Stan gry - plansza 3x3, przechowywana jako lista 9 pól
# (None = puste, "X" lub "O" = zajęte)
board: List[Optional[str]] = [None] * 9
current_turn = "X"
players: dict = {}  # połączenie WebSocket -> symbol gracza ("X" lub "O")
game_over = False


def check_winner() -> Optional[str]:
    """
    Sprawdza planszę pod kątem zwycięskiego układu (3 w rzędzie,
    kolumnie lub przekątnej). Zwraca symbol zwycięzcy ("X"/"O"),
    "draw" przy remisie (plansza pełna, brak zwycięzcy), albo None
    jeśli gra wciąż trwa.
    """
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # wiersze
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # kolumny
        [0, 4, 8], [2, 4, 6],             # przekątne
    ]

    for line in winning_lines:
        a, b, c = line
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if all(cell is not None for cell in board):
        return "draw"

    return None


async def broadcast_state():
    """
    Wysyła aktualny stan gry (planszę, aktualną turę, wynik)
    do obu podłączonych graczy.
    """
    winner = check_winner()
    state = {
        "type": "state",
        "board": board,
        "turn": current_turn,
        "winner": winner,
    }
    message = json.dumps(state)

    for connection in players:
        if not connection.closed:
            await connection.send_str(message)


async def websocket_handler(request):
    """
    Handler obsługujący pojedynczego gracza.

    Pierwszy podłączony gracz dostaje symbol "X", drugi "O".
    Trzeci i kolejni klienci są traktowani jako obserwatorzy
    (nie mogą wykonywać ruchów).
    """
    global current_turn, game_over

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Przypisanie symbolu graczowi
    if "X" not in players.values():
        symbol = "X"
    elif "O" not in players.values():
        symbol = "O"
    else:
        symbol = None  # obserwator - gra jest już pełna

    players[ws] = symbol

    if symbol:
        print(f"✅ Gracz dołączył jako: {symbol}")
        await ws.send_str(json.dumps({"type": "assigned", "symbol": symbol}))
    else:
        print("👀 Nowy obserwator dołączył (gra pełna)")
        await ws.send_str(json.dumps({"type": "assigned", "symbol": None}))

    # Wysyłamy aktualny stan gry nowemu klientowi
    await broadcast_state()

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)

                if data.get("type") == "move" and symbol:
                    position = data.get("position")

                    # Walidacja ruchu
                    winner = check_winner()
                    if (
                        winner is None
                        and symbol == current_turn
                        and 0 <= position <= 8
                        and board[position] is None
                    ):
                        board[position] = symbol
                        current_turn = "O" if current_turn == "X" else "X"
                        print(f"🎮 Ruch: {symbol} na pole {position}")
                        await broadcast_state()
                    else:
                        await ws.send_str(json.dumps({"type": "error", "message": "Nieprawidłowy ruch"}))

            elif msg.type == web.WSMsgType.ERROR:
                print(f"❌ Błąd WebSocket: {ws.exception()}")

    finally:
        players.pop(ws, None)
        print(f"❌ Gracz {symbol} rozłączony")

    return ws


app = web.Application()
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    print("🚀 Serwer tic-tac-toe działa na ws://localhost:8080/ws")
    web.run_app(app, host='localhost', port=8080)