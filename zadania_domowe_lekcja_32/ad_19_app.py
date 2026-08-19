"""
Główna aplikacja.
Trasy są importowane z osobnego modułu.
"""
from aiohttp import web

from routes import setup_routes


def create_app():
    """Tworzy i konfiguruje aplikację."""

    app = web.Application()

    setup_routes(app)

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        port=8080
    )