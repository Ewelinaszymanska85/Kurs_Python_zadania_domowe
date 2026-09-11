from aiohttp import web


async def handle(request: web.Request) -> web.Response:
    return web.Response(text="Hello from CI/CD pipeline!\n")


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", handle)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8000)