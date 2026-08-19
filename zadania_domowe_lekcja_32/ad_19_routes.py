"""
Organizacja tras.
Wszystkie endpointy są definiowane w osobnym module.
"""
from aiohttp import web


async def home(request):
    """Strona główna."""

    return web.Response(
        text="<h1>Witaj w API!</h1>",
        content_type="text/html"
    )


async def status(request):
    """Zwraca status API."""

    return web.json_response({
        "status": "OK"
    })


def setup_routes(app):
    """Rejestruje wszystkie trasy aplikacji."""

    app.router.add_get(
        "/",
        home
    )

    app.router.add_get(
        "/api/status",
        status
    )