"""
Obsługa błędu.
Jeśli użytkownik próbuje wejść jako admin,
serwer zwraca błąd HTTP 403 Forbidden.
"""
from aiohttp import web


async def powitanie(request):
    """Zwraca powitanie lub błąd dla użytkownika admin."""

    imie = request.match_info["imie"]

    if imie.lower() == "admin":
        raise web.HTTPForbidden(
            text="Dostęp dla admina zabroniony"
        )

    return web.Response(
        text=f"Witaj, {imie}!"
    )


def create_app():
    app = web.Application()

    app.router.add_get(
        "/witaj/{imie}",
        powitanie
    )

    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8080)