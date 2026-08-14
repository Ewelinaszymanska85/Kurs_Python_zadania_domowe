"""
Ad_14. WebSockets i GraphQL
WebSocket z autentykacją.

Serwer WebSocket wymagający autentykacji: pierwsza wiadomość od
klienta musi być poprawnym tokenem. Jeśli token jest nieprawidłowy,
połączenie jest natychmiast zamykane. Dopiero po pomyślnej
weryfikacji, serwer akceptuje dalsze wiadomości.

Uwaga: dla uproszczenia (bez pełnego systemu Django/JWT) używamy
prostej, symulowanej listy poprawnych tokenów zamiast prawdziwej
weryfikacji podpisu JWT. Mechanizm autentykacji (pierwsza wiadomość
jako token, odrzucenie przy błędnym tokenie) jest identyczny.
"""

from aiohttp import web

# Symulowana lista poprawnych tokenów (w prawdziwej aplikacji:
# weryfikacja podpisu JWT, sprawdzenie w bazie danych itp.)
VALID_TOKENS = {
    "token-ewelina-123": "Ewelina",
    "token-admin-456": "Admin",
}


async def websocket_handler(request):
    """
    Handler wymagający autentykacji tokenem jako pierwszej
    wiadomości.

    Jeśli token jest nieprawidłowy, wysyła komunikat o błędzie
    i zamyka połączenie. Jeśli token jest poprawny, akceptuje
    dalsze wiadomości i odpowiada echo z podpisem użytkownika.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("✅ Nowy klient - oczekiwanie na token...")

    is_authenticated = False
    username = None

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:

            if not is_authenticated:
                # Pierwsza wiadomość MUSI być tokenem
                token = msg.data

                if token in VALID_TOKENS:
                    is_authenticated = True
                    username = VALID_TOKENS[token]
                    print(f"🔓 Klient uwierzytelniony jako: {username}")
                    await ws.send_str(f"✅ Uwierzytelniono jako {username}")
                else:
                    print(f"🔒 Odrzucono nieprawidłowy token: {token}")
                    await ws.send_str("❌ Nieprawidłowy token - rozłączanie")
                    await ws.close()
                    break

            else:
                # Klient jest już uwierzytelniony - normalna obsługa wiadomości
                print(f"📥 [{username}] {msg.data}")
                await ws.send_str(f"Echo dla {username}: {msg.data}")

        elif msg.type == web.WSMsgType.ERROR:
            print(f"❌ Błąd WebSocket: {ws.exception()}")

    print(f"❌ Klient rozłączony ({username if username else 'nieuwierzytelniony'})")
    return ws


app = web.Application()
app.router.add_get('/ws', websocket_handler)


if __name__ == '__main__':
    print("🚀 Serwer z autentykacją działa na ws://localhost:8080/ws")
    print(f"ℹ️  Poprawne tokeny testowe: {list(VALID_TOKENS.keys())}")
    web.run_app(app, host='localhost', port=8080)