"""
Odczyt query params.
Odczytuje parametr q z adresu URL i zwraca go jako JSON.
"""
from aiohttp import web


async def search(request):
    """Obsługuje parametr q."""

    wartosc_q = request.query.get("q")

    if wartosc_q:
        return web.json_response({
            "szukana_fraza": wartosc_q
        })

    return web.json_response(
        {"błąd": "Brak parametru q"},
        status=400
    )


def create_app():
    app = web.Application()

    app.router.add_get(
        "/api/search",
        search
    )

    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8080)