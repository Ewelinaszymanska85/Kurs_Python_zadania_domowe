"""
Aiohttp: Strona powitalna.
Tworzy prosty serwer HTTP z trasą /.
"""
from aiohttp import web


async def strona_powitalna(request):
    """Zwraca stronę powitalną HTML."""

    return web.Response(
        text="<h1>Witaj na mojej stronie!</h1>",
        content_type="text/html"
    )


def create_app():
    """Tworzy aplikację aiohttp."""

    app = web.Application()

    app.router.add_get(
        "/",
        strona_powitalna
    )

    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8080)