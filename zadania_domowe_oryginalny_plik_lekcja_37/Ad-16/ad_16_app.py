import socket

from aiohttp import web


async def handle(request: web.Request) -> web.Response:
    hostname = socket.gethostname()
    return web.Response(text=f"Odpowiedz z instancji: {hostname}\n")


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", handle)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8000)