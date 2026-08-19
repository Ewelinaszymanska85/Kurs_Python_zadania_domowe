"""
Aiohttp: Dynamiczne powitanie.
Pobiera imię z adresu URL i zwraca spersonalizowane powitanie.
"""
from aiohttp import web


async def powitanie(request):
    """Zwraca powitanie dla podanego imienia."""

    imie = request.match_info["imie"]

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