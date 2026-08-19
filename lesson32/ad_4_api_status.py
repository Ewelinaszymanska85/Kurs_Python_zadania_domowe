"""
Proste API JSON.
Endpoint /api/status zwraca status serwera oraz aktualny czas.
"""
from aiohttp import web
from datetime import datetime


async def status(request):
    """Zwraca status serwera w formacie JSON."""

    return web.json_response({
        "status": "OK",
        "server_time": datetime.now().isoformat()
    })


def create_app():
    app = web.Application()

    app.router.add_get(
        "/api/status",
        status
    )

    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8080)