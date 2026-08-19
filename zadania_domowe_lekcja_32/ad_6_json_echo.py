"""
Odczyt JSON.
Handler POST odczytuje JSON z żądania i zwraca go użytkownikowi.
"""
from aiohttp import web


async def echo(request):
    """Odczytuje i zwraca dane JSON."""

    dane = await request.json()

    return web.json_response(dane)


def create_app():
    app = web.Application()

    app.router.add_post(
        "/api/echo",
        echo
    )

    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8080)